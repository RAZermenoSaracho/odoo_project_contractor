# Part of project_contractor. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.fields import Domain

from odoo.addons.project.models.project_task import CLOSED_STATES


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def unlink(self):
        if self.env.user.is_contractor_user:
            from odoo.exceptions import AccessError
            raise AccessError(_("Contractors cannot delete contacts."))
        return super().unlink()

    is_contractor = fields.Boolean(
        string="Contractor",
        index=True,
        default=False,
        copy=False,
        help="External person or company that performs project work without being an Odoo user. "
             "Contacts belonging to a contractor company can also be set as task contractors.",
    )
    contractor_task_ids = fields.One2many(
        'project.task', 'contractor_id', string="Contractor Tasks", compute='_compute_contractor_work_history',
        groups='project.group_project_user', export_string_translation=False)
    contractor_task_count = fields.Integer(
        string="Contractor Tasks Count", compute='_compute_contractor_work_history',
        groups='project.group_project_user', export_string_translation=False)
    contractor_open_task_count = fields.Integer(
        string="Current Contractor Work", compute='_compute_contractor_work_history',
        groups='project.group_project_user', export_string_translation=False)
    contractor_done_task_count = fields.Integer(
        string="Completed Contractor Work", compute='_compute_contractor_work_history',
        groups='project.group_project_user', export_string_translation=False)
    contractor_project_count = fields.Integer(
        string="Contractor Projects Count", compute='_compute_contractor_work_history',
        groups='project.group_project_user', export_string_translation=False)

    @api.model
    def _get_contractor_eligible_domain(self):
        """Contacts marked as contractors, or belonging to a contractor company."""
        return Domain('is_contractor', '=', True) | Domain('commercial_partner_id.is_contractor', '=', True)

    def _is_contractor_eligible(self):
        self.ensure_one()
        return self.active and (self.is_contractor or self.commercial_partner_id.is_contractor)

    def _get_contractor_work_partners(self):
        """Partners in self and all their (possibly archived) child contacts."""
        return self.with_context(active_test=False).search_fetch([('id', 'child_of', self.ids)], ['parent_id'])

    @api.depends_context('uid', 'allowed_company_ids')
    def _compute_contractor_work_history(self):
        stats = {
            partner.id: {'all': 0, 'open': 0, 'done': 0, 'projects': set()}
            for partner in self
        }
        real_partners = self.filtered('id')._origin
        if real_partners:
            work_partners = real_partners._get_contractor_work_partners()
            parent_by_id = {partner.id: partner.parent_id.id for partner in work_partners}
            Task = self.env['project.task']
            # Not sudo: record rules and allowed companies of the viewer apply.
            task_groups = Task._read_group(
                Domain('contractor_id', 'in', work_partners.ids) & Task._get_contractor_work_domain(),
                groupby=['contractor_id', 'state', 'project_id'],
                aggregates=['__count'],
            )
            readable_project_ids = set(self.env['project.project'].search(
                Domain('id', 'in', [project.id for _, _, project, _ in task_groups if project])
            ).ids)
            target_ids = set(real_partners.ids)
            for contractor, state, project, count in task_groups:
                partner_id = contractor.id
                while partner_id:
                    if partner_id in target_ids:
                        partner_stats = stats[partner_id]
                        partner_stats['all'] += count
                        if state == '1_done':
                            partner_stats['done'] += count
                        elif state not in CLOSED_STATES:
                            partner_stats['open'] += count
                        if project and project.id in readable_project_ids:
                            partner_stats['projects'].add(project.id)
                    partner_id = parent_by_id.get(partner_id)
        for partner in self:
            partner_stats = stats.get(partner._origin.id) or stats[partner.id]
            partner.contractor_task_count = partner_stats['all']
            partner.contractor_task_ids = self.env['project.task'].search(partner._get_contractor_work_task_domain())
            partner.contractor_open_task_count = partner_stats['open']
            partner.contractor_done_task_count = partner_stats['done']
            partner.contractor_project_count = len(partner_stats['projects'])

    def _contractor_invalidate_work_history(self):
        """Invalidate derived history after a partner hierarchy change.

        Task changes are handled by ``project.task``.  A parent change has no
        native field dependency from the task inverse relation, so invalidate
        the affected contacts and both parent chains explicitly.
        """
        partners = self.with_context(active_test=False)
        ancestors = partners.search([('id', 'parent_of', partners.ids)])
        (partners | ancestors).invalidate_recordset([
            'contractor_task_ids', 'contractor_task_count',
            'contractor_open_task_count', 'contractor_done_task_count',
            'contractor_project_count',
        ])

    def write(self, vals):
        old_parents = self.with_context(active_test=False).mapped('parent_id') if 'parent_id' in vals else self.browse()
        result = super().write(vals)
        if 'parent_id' in vals:
            (self | old_parents)._contractor_invalidate_work_history()
        return result

    def _get_contractor_work_task_domain(self):
        self.ensure_one()
        return (
            Domain('contractor_id', 'in', self._get_contractor_work_partners().ids)
            & self.env['project.task']._get_contractor_work_domain()
        )

    def _get_contractor_task_action(self, name, domain=None, context=None):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('project.project_task_action_from_partner')
        action_context = {}
        if self._is_contractor_eligible():
            action_context['default_contractor_id'] = self.id
        action_context.update(context or {})
        action.update({
            'display_name': name,
            'domain': list(self._get_contractor_work_task_domain() & Domain(domain or [])),
            'context': action_context,
        })
        return action

    def action_view_contractor_tasks(self):
        """All contractor tasks, with the "Open" filter preselected (current work)."""
        return self._get_contractor_task_action(
            _("%(partner_name)s's Contractor Work", partner_name=self.name),
            context={'search_default_open_tasks': 1},
        )

    def action_view_contractor_done_tasks(self):
        return self._get_contractor_task_action(
            _("%(partner_name)s's Completed Contractor Work", partner_name=self.name),
            domain=[('state', '=', '1_done')],
        )

    def action_view_contractor_projects(self):
        self.ensure_one()
        project_groups = self.env['project.task']._read_group(
            self._get_contractor_work_task_domain() & Domain('project_id', '!=', False),
            groupby=['project_id'],
        )
        projects = self.env['project.project'].search(
            Domain('id', 'in', [project.id for [project] in project_groups])
        )
        action = self.env['ir.actions.act_window']._for_xml_id('project.open_view_project_all')
        action.update({
            'display_name': _("%(partner_name)s's Contractor Projects", partner_name=self.name),
            'domain': [('id', 'in', projects.ids)],
            'context': {},
        })
        return action
