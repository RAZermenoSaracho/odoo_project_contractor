# Part of project_contractor. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.fields import Domain


class ProjectProject(models.Model):
    _inherit = 'project.project'

    contractor_user_ids = fields.Many2many('res.users', compute='_compute_contractor_assignment', store=True)
    has_contractor_assignment = fields.Boolean(compute='_compute_contractor_assignment', store=True)

    @api.depends('task_ids.user_ids', 'task_ids.contractor_id', 'task_ids.contractor_id.user_ids')
    def _compute_contractor_assignment(self):
        for project in self:
            users = project.task_ids.user_ids | project.task_ids.contractor_id.user_ids
            project.contractor_user_ids = users
            project.has_contractor_assignment = bool(users)

    contractor_ids = fields.Many2many(
        'res.partner', string="Contractors", compute='_compute_contractor_ids', search='_search_contractor_ids',
        groups='project.group_project_user', export_string_translation=False,
        help="Contractors of this project's tasks (open or closed), excluding archived and template tasks.")
    contractor_count = fields.Integer(
        string="Contractors Count", compute='_compute_contractor_ids',
        groups='project.group_project_user', export_string_translation=False)

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
