from odoo.tests import tagged

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestProjectParticipation(ProjectContractorCommon):

    def test_contractors_from_open_and_closed_tasks(self):
        self.create_task('Open task', self.project_p, contractor_id=self.jane.id)
        self.create_task('Done task', self.project_p, contractor_id=self.acme.id, state='1_done')
        self.create_task('No contractor', self.project_p)
        project = self.project_p.with_user(self.project_user)
        self.assertEqual(project.contractor_ids, self.jane | self.acme)
        self.assertEqual(project.contractor_count, 2)

    def test_participation_ends_when_last_assignment_is_removed(self):
        task = self.create_task('Only Jane task', self.project_p, contractor_id=self.jane.id)
        self.assertEqual(self.project_p.with_user(self.project_user).contractor_ids, self.jane)
        task.contractor_id = False
        self.assertFalse(self.project_p.with_user(self.project_user).contractor_ids)

    def test_archived_and_template_tasks_are_excluded(self):
        archived = self.create_task('Bob task', self.project_p, contractor_id=self.bob.id)
        archived.action_archive()
        self.create_task('Template', self.project_p, is_template=True, contractor_id=self.dan.id)
        project = self.project_p.with_user(self.project_user)
        self.assertFalse(project.contractor_ids)
        self.assertEqual(project.contractor_count, 0)

    def test_project_has_no_editable_contractor_field(self):
        contractor_fields = {
            name: field for name, field in self.env['project.project']._fields.items() if 'contractor' in name
        }
        self.assertEqual(set(contractor_fields), {'contractor_ids', 'contractor_count'})
        for field in contractor_fields.values():
            self.assertFalse(field.store)
            self.assertTrue(field.readonly)

    def test_contractor_count_and_navigation(self):
        open_task = self.create_task('Open', self.project_p, contractor_id=self.jane.id)
        done_task = self.create_task('Done', self.project_p, contractor_id=self.acme.id, state='1_done')
        self.create_task('No contractor', self.project_p)
        project = self.project_p.with_user(self.project_user)
        self.assertEqual(project.contractor_count, 2)

        action = project.action_view_contractor_tasks()
        self.assertEqual(action['res_model'], 'project.task')
        self.assertEqual(action['context'].get('search_default_groupby_contractor'), 1)
        self.assertNotIn('search_default_open_tasks', action['context'])
        listed = self.env['project.task'].with_user(self.project_user).search(action['domain'])
        self.assertEqual(listed, open_task | done_task)

    def test_participation_refreshes_without_manual_cache_invalidation(self):
        task = self.create_task('Only Jane task', self.project_p, contractor_id=self.jane.id)
        project = self.project_p.with_user(self.project_user)
        self.assertEqual(project.contractor_ids, self.jane)
        task.contractor_id = self.acme
        self.assertEqual(project.contractor_ids, self.acme)

    def test_search_projects_by_contractor(self):
        self.create_task('Acme in P', self.project_p, contractor_id=self.acme.id)
        self.create_task('Jane in Q', self.project_q, contractor_id=self.jane.id)
        projects = self.project_p | self.project_q
        Project = self.env['project.project'].with_user(self.project_user)
        self.assertEqual(Project.search([('contractor_ids', 'in', self.acme.ids)]) & projects, self.project_p)
        self.assertEqual(Project.search([('contractor_ids', 'ilike', 'Acme Consulting')]) & projects, self.project_p)
        self.assertEqual(Project.search([('contractor_ids', 'not in', self.acme.ids)]) & projects, self.project_q)
