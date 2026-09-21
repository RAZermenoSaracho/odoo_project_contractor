# Part of project_contractor. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import AccessError
from odoo.fields import Domain


class ProjectProject(models.Model):
    _inherit = 'project.project'

    primary_contractor_id = fields.Many2one(
        'res.partner', string="Assigned Contractor", copy=False, tracking=True, readonly=True,
        domain="['|', ('is_contractor', '=', True), ('commercial_partner_id.is_contractor', '=', True)]",
    )
    contract_id = fields.Many2one('contract.contract', string="Contract", readonly=True, copy=False, index=True)
    accepted_proposal_id = fields.Many2one('contract.proposal', string="Accepted Proposal", readonly=True, copy=False, index=True)
    agreed_amount = fields.Monetary(related='accepted_proposal_id.amount', readonly=True)
    agreed_currency_id = fields.Many2one(related='accepted_proposal_id.currency_id', string='Agreed Currency', readonly=True)

    _contract_unique = models.UniqueIndex('(contract_id) WHERE contract_id IS NOT NULL', 'A Contract can have only one execution Project.')
    _proposal_unique = models.UniqueIndex('(accepted_proposal_id) WHERE accepted_proposal_id IS NOT NULL', 'An accepted Proposal can have only one execution Project.')

    def _is_assigned_contractor(self):
        self.ensure_one()
        return self.primary_contractor_id == self.env.user.partner_id

    def write(self, vals):
        if self.env.user.is_contractor_user and not self.env.su:
            protected_fields = {
                'partner_id', 'user_id', 'primary_contractor_id', 'contract_id', 'accepted_proposal_id',
                'active', 'privacy_visibility', 'stage_id', 'agreed_amount', 'agreed_currency_id',
            }
            if protected_fields & vals.keys():
                raise AccessError(_("Contractors cannot change a Project's commercial relationship or lifecycle."))
            if any(not project._is_assigned_contractor() for project in self):
                raise AccessError(_("Only the Assigned Contractor can update this Project."))
        return super().write(vals)

    contractor_ids = fields.Many2many('res.partner', string="Contractors", compute='_compute_contractor_ids', search='_search_contractor_ids', groups='project.group_project_user', help="Contractors of this project's tasks, excluding archived and template tasks.")
    contractor_count = fields.Integer(string="Contractors Count", compute='_compute_contractor_ids', groups='project.group_project_user')

    @api.depends_context('uid', 'allowed_company_ids')
    def _compute_contractor_ids(self):
        Task = self.env['project.task']
        contractors_by_project = {}
        project_ids = self.filtered('id')._origin.ids
        if project_ids:
            for project, contractor in Task._read_group(
                Domain('project_id', 'in', project_ids) & Domain('contractor_id', '!=', False) & Task._get_contractor_work_domain(),
                groupby=['project_id', 'contractor_id'],
            ):
                contractors_by_project[project.id] = contractors_by_project.get(project.id, contractor.browse()) | contractor
        for project in self:
            contractors = contractors_by_project.get(project._origin.id, self.env['res.partner'])
            project.contractor_ids = contractors
            project.contractor_count = len(contractors)

    def _search_contractor_ids(self, operator, value):
        Task = self.env['project.task']
        positive_operator = Domain.NEGATIVE_OPERATORS.get(operator, operator)
        query = Task._search(Domain('contractor_id', positive_operator, value) & Domain('project_id', '!=', False) & Task._get_contractor_work_domain())
        domain = Domain('id', 'in', query.subselect('project_id'))
        return ~domain if operator in Domain.NEGATIVE_OPERATORS else domain

    def action_view_contractor_tasks(self):
        self.ensure_one()
        action = self.action_view_tasks()
        context = dict(action['context'])
        context.pop('search_default_open_tasks', None)
        context['search_default_groupby_contractor'] = 1
        action.update({
            'display_name': _("%(project_name)s's Contractor Work", project_name=self.name),
            'domain': list(Domain('project_id', '=', self.id) & Domain('contractor_id', '!=', False) & self.env['project.task']._get_contractor_work_domain()),
            'context': context,
        })
        return action
