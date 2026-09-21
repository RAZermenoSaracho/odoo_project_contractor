from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import new_test_user, tagged

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestContractorAccessControl(ProjectContractorCommon):

    def _activate_contractor(self):
        user = new_test_user(self.env, login='pc_contractor', groups='base.group_portal')
        partner_id = user.partner_id.id
        user.with_user(user).action_become_contractor()
        return user, partner_id

    def _create_scoped_projects(self, contractor):
        Project = self.env['project.project'].with_context(mail_create_nolog=True)
        open_project = Project.create({'name': 'Open Project', 'privacy_visibility': 'employees'})
        own_project = Project.create({'name': 'Own Project', 'privacy_visibility': 'employees'})
        other_project = Project.create({'name': 'Other Project', 'privacy_visibility': 'employees'})
        open_task = self.create_task('Open Task', open_project, user_ids=[Command.clear()])
        own_task = self.create_task(
            'Own Task', own_project, contractor_id=contractor.partner_id.id, user_ids=[Command.clear()])
        other_task = self.create_task('Other Task', other_project, user_ids=[Command.link(self.project_user.id)])
        return open_project, own_project, other_project, open_task, own_task, other_task

    def test_activation_is_identity_preserving_and_idempotent(self):
        user = new_test_user(self.env, login='pc_activation', groups='base.group_portal')
        user_count = self.env['res.users'].with_context(active_test=False).search_count([])
        partner_count = self.env['res.partner'].with_context(active_test=False).search_count([])
        partner_id = user.partner_id.id

        user.with_user(user).action_become_contractor()
        self.assertEqual(user.partner_id.id, partner_id)
        self.assertTrue(user.is_contractor_user)
        self.assertFalse(user.share)
        self.assertTrue(user.has_group('project_contractor.group_contractor'))
        self.assertTrue(user.has_group('base.group_user'))
        self.assertFalse(user.has_group('project.group_project_user'))
        self.assertFalse(user.has_group('project.group_project_manager'))
        self.assertEqual(user.group_ids, self.env.ref('project_contractor.group_contractor'))
        self.assertEqual(self.env['res.users'].with_context(active_test=False).search_count([]), user_count)
        self.assertEqual(self.env['res.partner'].with_context(active_test=False).search_count([]), partner_count)

        user.with_user(user).action_become_contractor()
        self.assertEqual(user.partner_id.id, partner_id)
        self.assertEqual(self.env['res.users'].with_context(active_test=False).search_count([]), user_count)
        self.assertEqual(self.env['res.partner'].with_context(active_test=False).search_count([]), partner_count)

    def test_activation_cannot_target_another_user(self):
        contractor, _partner_id = self._activate_contractor()
        other_portal = new_test_user(self.env, login='pc_other_portal', groups='base.group_portal')
        with self.assertRaises(AccessError):
            other_portal.with_user(contractor).action_become_contractor()
        self.assertTrue(other_portal.share)
        self.assertFalse(other_portal.is_contractor_user)

    def test_contractor_effective_project_and_task_permissions(self):
        contractor, _partner_id = self._activate_contractor()
        open_project, own_project, other_project, open_task, own_task, other_task = self._create_scoped_projects(contractor)
        Project = self.env['project.project'].with_user(contractor)
        Task = self.env['project.task'].with_user(contractor)

        visible_projects = Project.search([('id', 'in', (open_project | own_project | other_project).ids)])
        self.assertEqual(visible_projects, open_project | own_project)
        visible_tasks = Task.search([('id', 'in', (open_task | own_task | other_task).ids)])
        self.assertEqual(visible_tasks, open_task | own_task)
        with self.assertRaises(AccessError):
            other_project.with_user(contractor).read(['name'])
        with self.assertRaises(AccessError):
            other_task.with_user(contractor).read(['name'])

        open_project.with_user(contractor).write({'name': 'Renamed Open Project'})
        own_task.with_user(contractor).write({'name': 'Renamed Own Task'})
        with self.assertRaises(AccessError):
            Project.create({'name': 'Contractor Project'})
        with self.assertRaises(AccessError):
            open_project.with_user(contractor).unlink()
        with self.assertRaises(AccessError):
            Task.create({'name': 'Contractor Task', 'project_id': open_project.id})
        with self.assertRaises(AccessError):
            own_task.with_user(contractor).unlink()

    def test_contractor_cannot_change_customer_or_assignment_relationships(self):
        contractor, _partner_id = self._activate_contractor()
        open_project, own_project, _other_project, _open_task, own_task, _other_task = self._create_scoped_projects(contractor)
        with self.assertRaises(AccessError):
            open_project.with_user(contractor).write({'partner_id': self.client.id})
        with self.assertRaises(AccessError):
            own_project.with_user(contractor).write({'user_id': self.project_user.id})
        with self.assertRaises(AccessError):
            own_task.with_user(contractor).write({'contractor_id': False})
        with self.assertRaises(AccessError):
            own_task.with_user(contractor).write({'user_ids': [Command.link(self.project_user.id)]})
        with self.assertRaises(AccessError):
            own_task.with_user(contractor).write({'project_id': open_project.id})

    def test_contractor_can_only_access_and_edit_own_partner(self):
        contractor, partner_id = self._activate_contractor()
        own_partner = self.env['res.partner'].with_user(contractor).browse(partner_id)
        own_partner.write({'phone': '555-0100'})
        self.assertEqual(own_partner.phone, '555-0100')
        foreign_partner = self.jane.with_user(contractor)
        with self.assertRaises(AccessError):
            foreign_partner.read(['name'])
        with self.assertRaises(AccessError):
            foreign_partner.write({'name': 'Denied'})
        with self.assertRaises(AccessError):
            self.env['res.partner'].with_user(contractor).create({'name': 'Denied contact'})
        with self.assertRaises(AccessError):
            own_partner.unlink()

    def test_non_contractors_keep_their_existing_access(self):
        self._activate_contractor()
        self.assertEqual(
            self.project_p.with_user(self.project_user).read(['name'])[0]['name'], 'Contractor Project P')
        self.jane.with_user(self.project_user).write({'phone': '555-0200'})
        self.assertEqual(self.jane.phone, '555-0200')
        self.project_p.with_user(self.env.ref('base.user_admin')).write({'name': 'Admin project write'})
        self.assertEqual(self.project_p.name, 'Admin project write')
        self.jane.with_user(self.env.ref('base.user_admin')).write({'phone': '555-0300'})
        self.assertEqual(self.jane.phone, '555-0300')

    def test_non_contractor_portal_rules_remain_unaffected(self):
        project = self.env['project.project'].with_context(mail_create_nolog=True).create({
            'name': 'Portal Project',
            'privacy_visibility': 'portal',
            'collaborator_ids': [Command.create({'partner_id': self.portal_partner.id})],
        })
        project.message_subscribe(partner_ids=self.portal_partner.ids)
        task = self.create_task('Portal Task', project)
        self.assertEqual(project.with_user(self.portal_user).read(['name'])[0]['name'], 'Portal Project')
        self.assertEqual(task.with_user(self.portal_user).read(['name'])[0]['name'], 'Portal Task')

    def test_additive_acls_do_not_restore_create_or_delete(self):
        contractor, _partner_id = self._activate_contractor()
        Project = self.env['project.project'].with_user(contractor)
        Task = self.env['project.task'].with_user(contractor)
        self.assertTrue(Project.has_access('read'))
        self.assertTrue(Project.has_access('write'))
        self.assertFalse(Project.has_access('create'))
        self.assertFalse(Project.has_access('unlink'))
        self.assertTrue(Task.has_access('read'))
        self.assertTrue(Task.has_access('write'))
        # base.group_user grants a task-create ACL, so the narrow model guard
        # must close that additive permission until the lifecycle phase.
        self.assertTrue(Task.has_access('create'))
        with self.assertRaises(AccessError):
            Task.create({'name': 'Bypass attempt'})
        self.assertTrue(Task.has_access('unlink'))
        with self.assertRaises(AccessError):
            Task.unlink()
