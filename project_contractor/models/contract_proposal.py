from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class ContractProposal(models.Model):
    _name = 'contract.proposal'
    _description = 'Contract Proposal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    contract_id = fields.Many2one('contract.contract', required=True, ondelete='cascade', index=True)
    contractor_id = fields.Many2one('res.partner', required=True, string='Contractor', readonly=True, index=True)
    state = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='draft', required=True, tracking=True, copy=False)
    amount = fields.Monetary(required=True, default=0.0, tracking=True)
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)
    project_id = fields.Many2one('project.project', string='Execution Project', readonly=True, copy=False)
    _proposal_project_unique = models.UniqueIndex('(project_id) WHERE project_id IS NOT NULL', 'A Proposal can have only one execution Project.')

    def _is_own_contractor(self):
        self.ensure_one()
        return self.contractor_id == self.env.user.partner_id

    def _check_customer_or_internal_authority(self):
        if any(not (proposal.contract_id._is_customer_owner() or proposal.contract_id._is_internal_authority()) for proposal in self):
            raise AccessError(_("Only the customer owner or authorized internal staff can manage this Proposal."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            contract = self.env['contract.contract'].browse(vals.get('contract_id')).exists()
            if not contract:
                raise ValidationError(_("A Proposal requires a Contract."))
            if self.env.user.is_contractor_user:
                vals['contractor_id'] = self.env.user.partner_id.id
                if contract.state != 'published':
                    raise AccessError(_("Proposals can be created only for published Contracts."))
            elif not (contract._is_customer_owner() or contract._is_internal_authority() or self.env.is_superuser()):
                raise AccessError(_("You cannot create a Proposal for this Contract."))
            contractor_id = vals.get('contractor_id')
            if contractor_id and self.search_count([('contract_id', '=', contract.id), ('contractor_id', '=', contractor_id), ('state', 'in', ('draft', 'submitted'))]):
                raise ValidationError(_("A Contractor already has an active Proposal for this Contract."))
        return super().create(vals_list)

    def write(self, vals):
        if self.env.user.is_contractor_user and not self.env.su:
            if any(not proposal._is_own_contractor() or proposal.state != 'draft' for proposal in self):
                raise AccessError(_("Contractors can edit only their draft Proposals."))
            if {'contract_id', 'contractor_id', 'state', 'project_id'} & vals.keys():
                raise AccessError(_("Use Proposal actions to change its relationship or state."))
        elif not self.env.su:
            self._check_customer_or_internal_authority()
        if 'project_id' in vals and not self.env.su:
            raise AccessError(_("Proposal execution links are set by acceptance only."))
        return super().write(vals)

    def action_submit(self):
        if any(not proposal._is_own_contractor() for proposal in self):
            raise AccessError(_("Only the Proposal's Contractor can submit it."))
        if any(proposal.state != 'draft' or proposal.contract_id.state != 'published' for proposal in self):
            raise UserError(_("Only draft Proposals for published Contracts can be submitted."))
        self.sudo().write({'state': 'submitted'})
        return True

    def action_withdraw(self):
        if any(not proposal._is_own_contractor() or proposal.state not in ('draft', 'submitted') for proposal in self):
            raise AccessError(_("Only the Proposal's Contractor can withdraw an active Proposal."))
        self.sudo().write({'state': 'withdrawn'})
        return True

    def action_reject(self):
        self._check_customer_or_internal_authority()
        if any(proposal.state not in ('draft', 'submitted') for proposal in self):
            raise UserError(_("Only active Proposals can be rejected."))
        self.write({'state': 'rejected'})
        return True

    def action_accept(self):
        self.ensure_one()
        return self.contract_id._accept_proposal(self)
