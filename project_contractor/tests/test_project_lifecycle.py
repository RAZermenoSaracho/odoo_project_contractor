from odoo import Command
from odoo.exceptions import AccessError, ValidationError
from odoo.tests import new_test_user, tagged

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestContractorProjectLifecycle(ProjectContractorCommon):

    def _contractor_user(self, login):
        user = new_test_user(self.env, login=login, groups='base.group_portal')
        user.with_user(user).action_become_contractor()
        return user

    def _project(self, name, **values):
        return self.env['project.project'].with_context(mail_create_nolog=True).create({
            'name': name,
            'partner_id': self.client.id,
            'privacy_visibility': 'employees',
            **values,
        })

    def _candidate_project(self, project, contractor):
        project.action_admit_contractor_candidate(contractor.partner_id.id)
        return project

    def _assigned_project(self, project, contractor):
        project.action_assign_primary_contractor(contractor.partner_id.id)
        return project

    def test_project_contract_data_and_lifecycle_transitions(self):
        contractor_a = self._contractor_user('pc_lifecycle_a')
        contractor_b = self._contractor_user('pc_lifecycle_b')
        project = self._project('Lifecycle Contract')
        self.assertEqual(project.contractor_lifecycle, 'discoverable')
        self.assertFalse(project.primary_contractor_id)
        self.assertFalse(project.candidate_contractor_ids)
        self.assertEqual(project.contractor_compensation_amount, 0)
        self.assertEqual(project.contractor_compensation_currency_id, self.env.company.currency_id)

        self._candidate_project(project, contractor_a)
        self._candidate_project(project, contractor_b)
        self.assertEqual(project.contractor_lifecycle, 'candidate')
        self.assertEqual(project.candidate_contractor_ids, contractor_a.partner_id | contractor_b.partner_id)
        self.assertFalse(project.primary_contractor_id)

        self._assigned_project(project, contractor_a)
        self.assertEqual(project.contractor_lifecycle, 'assigned')
        self.assertEqual(project.primary_contractor_id, contractor_a.partner_id)
        self.assertIn(contractor_b.partner_id, project.candidate_contractor_ids)
        with self.assertRaises(ValidationError):
            project.write({'primary_contractor_id': self.jane.id})

        project.write({
            'contractor_compensation_amount': 1250,
            'contractor_compensation_currency_id': self.env.company.currency_id.id,
        })
        self.assertEqual(project.contractor_compensation_amount, 1250)

    def test_lifecycle_visibility_and_candidate_privacy(self):
        contractor_a = self._contractor_user('pc_visibility_a')
        contractor_b = self._contractor_user('pc_visibility_b')
        open_project = self._project('Discoverable Contract')
        candidate_project = self._candidate_project(self._project('Candidate Contract'), contractor_a)
        assigned_a = self._assigned_project(self._project('Assigned A Contract'), contractor_a)
        assigned_b = self._assigned_project(self._project('Assigned B Contract'), contractor_b)
        open_task = self.create_task('Discoverable Task', open_project, user_ids=[Command.clear()])
        candidate_task = self.create_task('Candidate Task', candidate_project, user_ids=[Command.clear()])
        assigned_a_task = self.create_task('Assigned A Task', assigned_a, user_ids=[Command.clear()])
        assigned_b_task = self.create_task('Assigned B Task', assigned_b, user_ids=[Command.clear()])

        ProjectA = self.env['project.project'].with_user(contractor_a)
        TaskA = self.env['project.task'].with_user(contractor_a)
        self.assertEqual(
            ProjectA.search([('id', 'in', (open_project | candidate_project | assigned_a | assigned_b).ids)]),
            open_project | candidate_project | assigned_a,
        )
        self.assertEqual(
            TaskA.search([('id', 'in', (open_task | candidate_task | assigned_a_task | assigned_b_task).ids)]),
            open_task | candidate_task | assigned_a_task,
        )
        with self.assertRaises(AccessError):
            assigned_b.with_user(contractor_a).read(['name'])
        self.assertNotIn(
            'candidate_contractor_ids', candidate_project.with_user(contractor_a).read(['candidate_contractor_ids'])[0])

    def test_discoverable_and_candidate_work_is_read_only(self):
        contractor = self._contractor_user('pc_read_only')
        discoverable = self._project('Discoverable Contract')
        candidate = self._candidate_project(self._project('Candidate Contract'), contractor)
        discoverable_task = self.create_task('Discoverable Task', discoverable, user_ids=[Command.clear()])
        candidate_task = self.create_task('Candidate Task', candidate, user_ids=[Command.clear()])

        for project in (discoverable, candidate):
            with self.assertRaises(AccessError):
                project.with_user(contractor).write({'name': 'Denied'})
        for task in (discoverable_task, candidate_task):
            with self.assertRaises(AccessError):
                task.with_user(contractor).write({'name': 'Denied'})
            with self.assertRaises(AccessError):
                task.with_user(contractor).unlink()
        for project in (discoverable, candidate):
            with self.assertRaises(AccessError):
                self.env['project.task'].with_user(contractor).create({
                    'name': 'Denied Task', 'project_id': project.id,
                })

    def test_assigned_contractor_has_project_operations_and_task_crud(self):
        contractor = self._contractor_user('pc_assigned_crud')
        project = self._assigned_project(self._project('Assigned Contract'), contractor)
        project.with_user(contractor).write({'name': 'Contractor Updated'})
        self.assertEqual(project.name, 'Contractor Updated')
        task, second_task = self.env['project.task'].with_user(contractor).create([
            {'name': 'Contractor Task', 'project_id': project.id},
            {'name': 'Second Contractor Task', 'project_id': project.id},
        ])
        task.write({'name': 'Contractor Updated Task'})
        self.assertEqual(task.name, 'Contractor Updated Task')
        (task | second_task).unlink()
        self.assertFalse(task.exists())

    def test_assigned_contractor_cannot_change_commercial_lifecycle_or_other_project(self):
        contractor_a = self._contractor_user('pc_restricted_a')
        contractor_b = self._contractor_user('pc_restricted_b')
        own_project = self._assigned_project(self._project('Assigned A Contract'), contractor_a)
        other_project = self._assigned_project(self._project('Assigned B Contract'), contractor_b)
        own_task = self.create_task('Assigned A Task', own_project)
        other_task = self.create_task('Assigned B Task', other_project)
        protected_values = (
            {'partner_id': self.jane.id},
            {'primary_contractor_id': contractor_b.partner_id.id},
            {'candidate_contractor_ids': [Command.link(contractor_b.partner_id.id)]},
            {'active': False},
            {'privacy_visibility': 'followers'},
            {'contractor_compensation_amount': 999},
            {'contractor_compensation_currency_id': self.env.company.currency_id.id},
        )
        for values in protected_values:
            with self.assertRaises(AccessError):
                own_project.with_user(contractor_a).write(values)
        with self.assertRaises(AccessError):
            own_task.with_user(contractor_a).write({'project_id': other_project.id})
        with self.assertRaises(AccessError):
            other_task.with_user(contractor_a).write({'name': 'Denied'})
        with self.assertRaises(AccessError):
            other_task.with_user(contractor_a).unlink()
        with self.assertRaises(AccessError):
            self.env['project.task'].with_user(contractor_a).create({
                'name': 'Denied', 'project_id': other_project.id,
            })

    def test_customer_commercial_partner_authorizes_lifecycle_actions(self):
        contractor = self._contractor_user('pc_customer_target')
        customer_user = new_test_user(self.env, login='pc_customer_owner', groups='base.group_portal')
        colleague_user = new_test_user(self.env, login='pc_customer_colleague', groups='base.group_portal')
        outsider = new_test_user(self.env, login='pc_customer_outsider', groups='base.group_portal')
        customer_user.partner_id.parent_id = self.client
        colleague_user.partner_id.parent_id = self.client
        project = self._project('Customer Owned Contract', privacy_visibility='portal')
        project.message_subscribe(partner_ids=self.client.ids)

        self.assertTrue(project.with_user(customer_user)._is_customer_owner())
        self.assertTrue(project.with_user(colleague_user)._is_customer_owner())
        self.assertFalse(project.with_user(outsider)._is_customer_owner())
        project.with_user(colleague_user).action_admit_contractor_candidate(contractor.partner_id.id)
        self.assertIn(contractor.partner_id, project.candidate_contractor_ids)
        with self.assertRaises(AccessError):
            project.with_user(outsider).action_close_contract()

    def test_primary_assignment_does_not_replace_task_history(self):
        contractor = self._contractor_user('pc_history_primary')
        project = self._assigned_project(self._project('History Contract'), contractor)
        self.assertFalse(project.contractor_ids)
        task = self.create_task('Historical Task', project, contractor_id=self.jane.id)
        self.assertEqual(project.contractor_ids, self.jane)
        self.assertEqual(project.primary_contractor_id, contractor.partner_id)
        task.contractor_id = False
        self.assertFalse(project.contractor_ids)
        self.assertEqual(project.primary_contractor_id, contractor.partner_id)

    def test_internal_administrator_retains_lifecycle_authority(self):
        contractor = self._contractor_user('pc_admin_target')
        project = self._project('Admin Contract')
        admin_project = project.with_user(self.env.ref('base.user_admin'))
        admin_project.action_admit_contractor_candidate(contractor.partner_id.id)
        admin_project.action_assign_primary_contractor(contractor.partner_id.id)
        admin_project.write({'contractor_compensation_amount': 100})
        self.assertEqual(project.primary_contractor_id, contractor.partner_id)
        self.assertEqual(project.contractor_compensation_amount, 100)
