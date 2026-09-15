from odoo.exceptions import AccessError
from odoo.tests import tagged

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestWorkHistory(ProjectContractorCommon):

    def test_individual_contractor_tasks(self):
        task_1 = self.create_task('T1', self.project_p, contractor_id=self.jane.id)
        task_2 = self.create_task('T2', self.project_q, contractor_id=self.jane.id)
        jane = self.jane.with_user(self.project_user)
        self.assertEqual(jane.contractor_task_ids, task_1 | task_2)
        self.assertEqual(jane.contractor_task_count, 2)

    def test_company_includes_its_contacts_work(self):
        task_3 = self.create_task('T3', self.project_p, contractor_id=self.acme.id)
        task_4 = self.create_task('T4', self.project_p, contractor_id=self.bob.id)
        acme = self.acme.with_user(self.project_user)
        bob = self.bob.with_user(self.project_user)
        self.assertEqual(acme.contractor_task_count, 2)
        self.assertEqual(bob.contractor_task_count, 1)
        self.assertEqual(bob.contractor_task_ids, task_4)
        Task = self.env['project.task'].with_user(self.project_user)
        self.assertEqual(Task.search(acme.action_view_contractor_tasks()['domain']), task_3 | task_4)
        self.assertEqual(Task.search(bob.action_view_contractor_tasks()['domain']), task_4)

    def _create_tasks_in_states(self):
        states = ['01_in_progress', '02_changes_requested', '1_done', '1_done', '1_canceled']
        return [self.create_task(f'Task {state} {i}', self.project_p, contractor_id=self.jane.id, state=state)
                for i, state in enumerate(states)]

    def test_counts_by_state(self):
        tasks = self._create_tasks_in_states()
        jane = self.jane.with_user(self.project_user)
        self.assertEqual(jane.contractor_open_task_count, 2)
        self.assertEqual(jane.contractor_done_task_count, 2)
        self.assertEqual(jane.contractor_task_count, 5)

        Task = self.env['project.task'].with_user(self.project_user)
        all_action = jane.action_view_contractor_tasks()
        self.assertEqual(all_action['context'].get('search_default_open_tasks'), 1)
        self.assertEqual(len(Task.search(all_action['domain'])), 5)
        done_tasks = Task.search(jane.action_view_contractor_done_tasks()['domain'])
        self.assertEqual(done_tasks, tasks[2] | tasks[3])

    def test_reopened_task_returns_to_current_work(self):
        tasks = self._create_tasks_in_states()
        tasks[2].state = '01_in_progress'
        self.env.invalidate_all()
        jane = self.jane.with_user(self.project_user)
        self.assertEqual(jane.contractor_open_task_count, 3)
        self.assertEqual(jane.contractor_done_task_count, 1)

    def test_projects_from_tasks(self):
        self.create_task('P1', self.project_p, contractor_id=self.jane.id)
        self.create_task('P2', self.project_p, contractor_id=self.jane.id)
        self.create_task('Q1', self.project_q, contractor_id=self.jane.id)
        jane = self.jane.with_user(self.project_user)
        self.assertEqual(jane.contractor_project_count, 2)
        action = jane.action_view_contractor_projects()
        self.assertEqual(action['res_model'], 'project.project')
        projects = self.env['project.project'].with_user(self.project_user).search(action['domain'])
        self.assertEqual(projects, self.project_p | self.project_q)

    def test_history_follows_task_changes(self):
        task = self.create_task('Done task', self.project_p, contractor_id=self.jane.id, state='1_done')
        self.assertEqual(self.jane.with_user(self.project_user).contractor_done_task_count, 1)
        self.assertEqual(self.dan.with_user(self.project_user).contractor_done_task_count, 0)
        task.contractor_id = self.dan
        self.env.invalidate_all()
        self.assertEqual(self.jane.with_user(self.project_user).contractor_done_task_count, 0)
        self.assertEqual(self.dan.with_user(self.project_user).contractor_done_task_count, 1)

    def test_history_fields_are_not_editable(self):
        for name in ('contractor_task_count', 'contractor_open_task_count', 'contractor_done_task_count',
                     'contractor_project_count'):
            field = self.env['res.partner']._fields[name]
            self.assertFalse(field.store)
            self.assertTrue(field.readonly)

    def test_restricted_project_hidden_from_count(self):
        self.create_task('Restricted', self.project_restricted, contractor_id=self.jane.id)
        self.create_task('Visible', self.project_p, contractor_id=self.jane.id)
        self.assertEqual(self.jane.with_user(self.project_user).contractor_task_count, 1)
        self.assertEqual(self.jane.sudo().contractor_task_count, 2)

    def test_user_without_project_access(self):
        self.create_task('Visible', self.project_p, contractor_id=self.jane.id)
        with self.assertRaises(AccessError):
            self.jane.with_user(self.internal_user).read(['contractor_task_count'])
        internal_arch = self.env['res.partner'].with_user(self.internal_user).get_views(
            [(False, 'form')])['views']['form']['arch']
        self.assertNotIn('action_view_contractor_tasks', internal_arch)
        project_user_arch = self.env['res.partner'].with_user(self.project_user).get_views(
            [(False, 'form')])['views']['form']['arch']
        self.assertIn('action_view_contractor_tasks', project_user_arch)
