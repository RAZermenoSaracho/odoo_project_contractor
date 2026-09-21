from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError


class ContractContract(models.Model):
    _name = 'contract.contract'
    _description = 'Contract Opportunity'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True, index=True)
    state = fields.Selection([('draft', 'Draft'), ('published', 'Published'), ('awarded', 'Awarded'), ('cancelled', 'Cancelled')], default='draft', required=True, tracking=True, copy=False)
    proposal_ids = fields.One2many('contract.proposal', 'contract_id', string='Proposals')
    accepted_proposal_id = fields.Many2one('contract.proposal', string='Accepted Proposal', readonly=True, copy=False)
    project_id = fields.Many2one('project.project', string='Execution Project', readonly=True, copy=False)

    def _is_customer_owner(self):
        self.ensure_one()
        return bool(self.partner_id and self.partner_id.commercial_partner_id == self.env.user.partner_id.commercial_partner_id)

    def _is_internal_authority(self):
        return self.env.is_superuser() or self.env.user.has_group('project.group_project_manager')

    def _check_customer_or_internal_authority(self):
        if any(not (contract._is_customer_owner() or contract._is_internal_authority()) for contract in self):
            raise AccessError(_("Only the customer owner or authorized internal staff can manage this Contract."))

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.is_superuser() and not self.env.user.has_group('project.group_project_manager'):
            user_commercial = self.env.user.partner_id.commercial_partner_id
            for vals in vals_list:
                partner = self.env['res.partner'].browse(vals.get('partner_id')).exists()
                if not partner or partner.commercial_partner_id != user_commercial:
                    raise AccessError(_("Contracts must belong to your commercial entity."))
        return super().create(vals_list)

    def write(self, vals):
        self._check_customer_or_internal_authority()
        if 'partner_id' in vals and not self._is_internal_authority():
            partner = self.env['res.partner'].browse(vals['partner_id']).exists()
            if not partner or partner.commercial_partner_id != self.env.user.partner_id.commercial_partner_id:
                raise AccessError(_("Contracts must belong to your commercial entity."))
        if {'accepted_proposal_id', 'project_id'} & vals.keys() and not self.env.su:
            raise AccessError(_("Contract awards must be made through Proposal acceptance."))
        return super().write(vals)

    def action_publish(self):
        self._check_customer_or_internal_authority()
        if any(contract.state != 'draft' for contract in self):
            raise UserError(_("Only draft Contracts can be published."))
        self.write({'state': 'published'})
        return True

    def action_cancel(self):
        self._check_customer_or_internal_authority()
        if any(contract.state not in ('draft', 'published') for contract in self):
            raise UserError(_("Only draft or published Contracts can be cancelled."))
        self.write({'state': 'cancelled'})
        return True

    def action_invite_contractor(self, contractor_id):
        self.ensure_one()
        self._check_customer_or_internal_authority()
        if self.state != 'published':
            raise UserError(_("Contractors can be invited only to a published Contract."))
        contractor = self.env['res.partner'].sudo().browse(contractor_id).exists()
        if not contractor or not contractor._is_contractor_eligible():
            raise UserError(_("Only an active eligible Contractor can be invited."))
        proposal = self.env['contract.proposal'].sudo().search([('contract_id', '=', self.id), ('contractor_id', '=', contractor.id), ('state', 'in', ('draft', 'submitted'))], limit=1)
        return proposal or self.env['contract.proposal'].sudo().create({'contract_id': self.id, 'contractor_id': contractor.id})

    def _accept_proposal(self, proposal):
        self.ensure_one()
        self._check_customer_or_internal_authority()
        if proposal.contract_id != self:
            raise UserError(_("The Proposal does not belong to this Contract."))
        self.env.cr.execute('SELECT id FROM contract_contract WHERE id = %s FOR UPDATE', [self.id])
        self.invalidate_recordset()
        contract = self.sudo().browse(self.id)
        proposal = proposal.sudo()
        if contract.accepted_proposal_id:
            if contract.accepted_proposal_id != proposal:
                raise UserError(_("This Contract already has an accepted Proposal."))
            return contract.project_id or self.env['project.project'].sudo().search([('contract_id', '=', contract.id)], limit=1)
        if contract.state != 'published' or proposal.state != 'submitted':
            raise UserError(_("Only a submitted Proposal on a published Contract can be accepted."))
        project = self.env['project.project'].sudo().create({
            'name': contract.name, 'partner_id': contract.partner_id.id, 'privacy_visibility': 'employees',
            'primary_contractor_id': proposal.contractor_id.id, 'contract_id': contract.id, 'accepted_proposal_id': proposal.id,
        })
        proposal.write({'state': 'accepted', 'project_id': project.id})
        contract.proposal_ids.filtered(lambda p: p != proposal and p.state == 'submitted').sudo().write({'state': 'rejected'})
        contract.write({'accepted_proposal_id': proposal.id, 'project_id': project.id, 'state': 'awarded'})
        return project
