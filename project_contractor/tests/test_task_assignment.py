from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import new_test_user, tagged

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestTaskAssignment(ProjectContractorCommon):

    def test_assign_contractor(self):
        task = self.create_task('Task T', self.project_p)
        self.assertFalse(task.contractor_id)
        task.with_user(self.project_user).contractor_id = self.jane
        self.assertEqual(task.contractor_id, self.jane)

    def test_clear_contractor(self):
        task = self.create_task(
            'Task T', self.project_p, contractor_id=self.jane.id,
            user_ids=[Command.set(self.project_user.ids)], partner_id=self.client.id,
        )
        task.with_user(self.project_user).contractor_id = False
        self.assertFalse(task.contractor_id)
        self.assertEqual(task.user_ids, self.project_user)
        self.assertEqual(task.partner_id, self.client)

    def test_non_contractor_rejected(self):
        task = self.create_task('Task T', self.project_p, contractor_id=self.jane.id)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            task.with_user(self.project_user).contractor_id = self.carol
        self.env.invalidate_all()
        self.assertEqual(task.contractor_id, self.jane)

    def test_contractor_from_another_company_rejected(self):
        task = self.create_task('Task T', self.project_p)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            task.with_user(self.project_user).contractor_id = self.company_b_contractor
        self.env.invalidate_all()
        self.assertFalse(task.contractor_id)

    def test_existing_assignment_survives_unmarking(self):
        task = self.create_task('Task T', self.project_p, contractor_id=self.jane.id)
        self.jane.is_contractor = False
        task.with_user(self.project_user).write({'name': 'Task T renamed', 'priority': '1'})
        self.assertEqual(task.name, 'Task T renamed')
        self.assertEqual(task.contractor_id, self.jane)

    def test_assignees_and_customer_are_independent(self):
        other_user = new_test_user(self.env, login='pc_other_assignee', groups='base.group_user,project.group_project_user')
        assignees = self.project_user | other_user
        task = self.create_task(
            'Task T', self.project_p, user_ids=[Command.set(assignees.ids)], partner_id=self.client.id,
        )
        task.contractor_id = self.acme
        self.assertEqual(task.user_ids, assignees)
        self.assertEqual(task.partner_id, self.client)
        task.user_ids = [Command.set(other_user.ids)]
        task.partner_id = self.carol
        self.assertEqual(task.contractor_id, self.acme)

    def test_contractor_without_user_account(self):
        users_before = self.env['res.users'].with_context(active_test=False).search_count([])
        task = self.create_task('Task T', self.project_p)
        task.contractor_id = self.jane
        self.assertEqual(task.contractor_id, self.jane)
        self.assertFalse(self.jane.user_ids)
        self.assertEqual(self.env['res.users'].with_context(active_test=False).search_count([]), users_before)

    def test_contractor_with_user_account_is_not_added_as_assignee(self):
        task = self.create_task('Task T', self.project_p, user_ids=[Command.set(self.project_user.ids)])
        task.contractor_id = self.portal_partner
        self.assertEqual(task.user_ids, self.project_user)
        self.assertNotIn(self.portal_user, task.user_ids)

    def test_subtasks_have_independent_contractors(self):
        parent = self.create_task('Parent', self.project_p)
        subtask_1 = self.create_task('T1', self.project_p, parent_id=parent.id, contractor_id=self.jane.id)
        subtask_2 = self.create_task('T2', self.project_p, parent_id=parent.id, contractor_id=self.acme.id)
        self.assertFalse(parent.contractor_id)
        parent.contractor_id = self.dan
        self.assertEqual(subtask_1.contractor_id, self.jane)
        self.assertEqual(subtask_2.contractor_id, self.acme)
        self.assertEqual(parent.contractor_id, self.dan)

    def test_filter_contracted_work(self):
        domain = self.get_search_filter_domain('project.task', 'with_contractor', 'project.view_task_search_form')
        with_contractor = self.create_task('With contractor', self.project_p, contractor_id=self.jane.id)
        self.create_task('Without contractor', self.project_p)
        Task = self.env['project.task'].with_user(self.project_user)
        self.assertEqual(Task.search(domain + [('project_id', '=', self.project_p.id)]), with_contractor)
        self.assertEqual(
            Task.search([('contractor_id', '=', self.jane.id), ('project_id', '=', self.project_p.id)]),
            with_contractor,
        )

    def test_group_by_contractor(self):
        node = self.get_search_filter('project.task', 'groupby_contractor', 'project.view_task_search_form')
        self.assertIn("'group_by': 'contractor_id'", node.get('context'))
        self.create_task('With contractor', self.project_p, contractor_id=self.jane.id)
        self.create_task('Without contractor', self.project_p)
        groups = self.env['project.task'].with_user(self.project_user)._read_group(
            [('project_id', '=', self.project_p.id)], ['contractor_id'], ['__count'])
        counts = {contractor.id: count for contractor, count in groups}
        self.assertEqual(counts, {self.jane.id: 1, False: 1})

    def test_assignment_is_tracked_without_notifying_contractors(self):
        task = self.create_task('Tracked task', self.project_p)
        self.flush_tracking()
        contractors = self.jane | self.acme
        notifications_before = self.env['mail.notification'].search_count([('res_partner_id', 'in', contractors.ids)])
        mails_before = self.env['mail.mail'].search_count([('recipient_ids', 'in', contractors.ids)])

        task.with_user(self.project_user).contractor_id = self.jane
        self.flush_tracking()
        task.with_user(self.project_user).contractor_id = self.acme
        self.flush_tracking()

        trackings = task.message_ids.sudo().tracking_value_ids.filtered(lambda v: v.field_id.name == 'contractor_id')
        self.assertEqual(len(trackings), 2)
        self.assertEqual(set(trackings.mapped('new_value_char')), {'Jane Doe', 'Acme Consulting'})
        self.assertEqual(trackings.mail_message_id.author_id, self.project_user.partner_id)
        self.assertFalse(contractors & task.message_partner_ids)
        self.assertEqual(
            self.env['mail.notification'].search_count([('res_partner_id', 'in', contractors.ids)]), notifications_before)
        self.assertEqual(self.env['mail.mail'].search_count([('recipient_ids', 'in', contractors.ids)]), mails_before)

    def test_duplicated_task_has_no_contractor(self):
        task = self.create_task('Original', self.project_p, contractor_id=self.jane.id)
        duplicate = task.copy()
        self.assertFalse(duplicate.contractor_id)
        self.assertEqual(task.contractor_id, self.jane)

    def test_task_created_from_template_has_no_contractor(self):
        template = self.create_task('Template task', self.project_p, is_template=True, contractor_id=self.jane.id)
        new_task = self.env['project.task'].browse(template.action_create_from_template())
        self.assertFalse(new_task.is_template)
        self.assertFalse(new_task.contractor_id)

    def test_recurring_occurrence_has_no_contractor(self):
        self.env.user.group_ids += self.env.ref('project.group_project_recurring_tasks')
        self.project_p.allow_recurring_tasks = True
        task = self.create_task(
            'Recurring task', self.project_p, contractor_id=self.jane.id,
            recurring_task=True, repeat_interval=1, repeat_unit='week', repeat_type='forever',
        )
        self.assertTrue(task.recurrence_id)
        values_list = self.env['project.task.recurrence']._create_next_occurrences_values({task: task.recurrence_id})
        self.assertTrue(values_list)
        self.assertFalse(values_list[0].get('contractor_id'))
