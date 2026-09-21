# Part of project_contractor. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
from odoo.fields import Domain


class ProjectProject(models.Model):
    _inherit = 'project.project'

    primary_contractor_id = fields.Many2one(
        'res.partner', string="Assigned Contractor", copy=False, tracking=True,
        domain="['|', ('is_contractor', '=', True), ('commercial_partner_id.is_contractor', '=', True)]",
    )
    candidate_contractor_ids = fields.Many2many(
        'res.partner', 'project_contractor_candidate_rel', 'project_id', 'partner_id',
        string="Candidate Contractors", copy=False, groups='project.group_project_manager',
        domain="['|', ('is_contractor', '=', True), ('commercial_partner_id.is_contractor', '=', True)]",
    )
    contractor_lifecycle = fields.Selection([
        ('discoverable', "Discoverable"),
        ('candidate', "Candidate Recruitment"),
        ('assigned', "Assigned"),
        ('closed', "Closed"),
    ], compute='_compute_contractor_lifecycle', store=True, readonly=True, copy=False)
    contractor_compensation_amount = fields.Monetary(
        string="Contract Compensation", currency_field='contractor_compensation_currency_id', copy=False, tracking=True)
    contractor_compensation_currency_id = fields.Many2one(
        'res.currency', string="Contract Compensation Currency", default=lambda self: self.env.company.currency_id,
        required=True, copy=False, tracking=True)

    contractor_ids = fields.Many2many(
        'res.partner', string="Contractors", compute='_compute_contractor_ids', search='_search_contractor_ids',
        groups='project.group_project_user', export_string_translation=False,
        help="Contractors of this project's tasks (open or closed), excluding archived and template tasks.")
    contractor_count = fields.Integer(
        string="Contractors Count", compute='_compute_contractor_ids',
        groups='project.group_project_user', export_string_translation=False)

    @api.depends('active', 'primary_contractor_id', 'candidate_contractor_ids')
    def _compute_contractor_lifecycle(self):
        for project in self:
            if not project.active:
                project.contractor_lifecycle = 'closed'
            elif project.primary_contractor_id:
                project.contractor_lifecycle = 'assigned'
            elif project.candidate_contractor_ids:
                project.contractor_lifecycle = 'candidate'
            else:
                project.contractor_lifecycle = 'discoverable'

    @api.constrains('primary_contractor_id', 'candidate_contractor_ids')
    def _check_contractor_lifecycle_membership(self):
        for project in self:
            contractors = project.primary_contractor_id | project.candidate_contractor_ids
            if project.primary_contractor_id and project.primary_contractor_id not in project.candidate_contractor_ids:
                raise ValidationError(_("The Assigned Contractor must first be a Candidate Contractor."))
            if not all(contractor._is_contractor_eligible() for contractor in contractors):
                raise ValidationError(_("Only active eligible contractor contacts can participate in a Project Contract."))

    def _is_assigned_contractor(self):
        self.ensure_one()
        return (
            self.contractor_lifecycle == 'assigned'
            and self.primary_contractor_id == self.env.user.partner_id
        )

    def _is_customer_owner(self):
        self.ensure_one()
        return bool(
            self.partner_id
            and self.partner_id.commercial_partner_id == self.env.user.partner_id.commercial_partner_id
        )

    def _check_customer_or_internal_lifecycle_authority(self):
        for project in self:
            if not (
                self.env.is_superuser()
                or self.env.user.has_group('project.group_project_manager')
                or project._is_customer_owner()
            ):
                raise AccessError(_("Only the customer owner or authorized internal staff can change this Project Contract."))

    def action_admit_contractor_candidate(self, contractor):
        self.ensure_one()
        self._check_customer_or_internal_lifecycle_authority()
        contractor = self.env['res.partner'].sudo().browse(contractor).exists()
        if not contractor or not contractor._is_contractor_eligible():
            raise ValidationError(_("Only an active eligible contractor can become a Candidate."))
        self.sudo().write({'candidate_contractor_ids': [fields.Command.link(contractor.id)]})
        return True

    def action_assign_primary_contractor(self, contractor):
        self.ensure_one()
        self._check_customer_or_internal_lifecycle_authority()
        contractor = self.env['res.partner'].sudo().browse(contractor).exists()
        if not contractor or not contractor._is_contractor_eligible():
            raise ValidationError(_("Only an active eligible contractor can be assigned."))
        self.sudo().write({
            'candidate_contractor_ids': [fields.Command.link(contractor.id)],
            'primary_contractor_id': contractor.id,
        })
        return True

    def action_close_contract(self):
        self._check_customer_or_internal_lifecycle_authority()
        self.sudo().write({'active': False})
        return True

    def write(self, vals):
        if self.env.user.is_contractor_user:
            protected_fields = {
                'partner_id', 'user_id', 'primary_contractor_id', 'candidate_contractor_ids',
                'active', 'privacy_visibility', 'stage_id',
                'contractor_compensation_amount', 'contractor_compensation_currency_id',
            }
            if protected_fields & vals.keys():
                raise AccessError(_("Contractors cannot change a Project's commercial relationship or lifecycle."))
            if any(not project._is_assigned_contractor() for project in self):
                raise AccessError(_("Only the Assigned Contractor can update this Project."))
        return super().write(vals)

    @api.depends_context('uid', 'allowed_company_ids')
    def _compute_contractor_ids(self):
        Task = self.env['project.task']
        contractors_by_project = {}
        real_project_ids = self.filtered('id')._origin.ids
        if real_project_ids:
            # Not sudo: the viewer's record rules apply to the tasks participation is derived from.
            task_groups = Task._read_group(
                Domain('project_id', 'in', real_project_ids)
                & Domain('contractor_id', '!=', False)
                & Task._get_contractor_work_domain(),
                groupby=['project_id', 'contractor_id'],
            )
            for project, contractor in task_groups:
                contractors_by_project[project.id] = contractors_by_project.get(project.id, contractor.browse()) | contractor
        for project in self:
            contractors = contractors_by_project.get(project._origin.id, self.env['res.partner'])
            project.contractor_ids = contractors
            project.contractor_count = len(contractors)

    def _search_contractor_ids(self, operator, value):
        Task = self.env['project.task']
        positive_operator = Domain.NEGATIVE_OPERATORS.get(operator, operator)
        task_query = Task._search(
            Domain('contractor_id', positive_operator, value)
            & Domain('project_id', '!=', False)
            & Task._get_contractor_work_domain()
        )
        domain = Domain('id', 'in', task_query.subselect('project_id'))
        return ~domain if operator in Domain.NEGATIVE_OPERATORS else domain

    def action_view_contractor_tasks(self):
        self.ensure_one()
        action = self.action_view_tasks()
        context = dict(action['context'])
        context.pop('search_default_open_tasks', None)
        context['search_default_groupby_contractor'] = 1
        action.update({
            'display_name': _("%(project_name)s's Contractor Work", project_name=self.name),
            'domain': list(
                Domain('project_id', '=', self.id)
                & Domain('contractor_id', '!=', False)
                & self.env['project.task']._get_contractor_work_domain()
            ),
            'context': context,
        })
        return action
