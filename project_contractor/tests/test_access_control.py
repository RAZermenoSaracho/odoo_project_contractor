from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import HttpCase, new_test_user, tagged
from odoo.tests.common import JsonRpcException
from odoo.tools import mute_logger

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestAccessControl(ProjectContractorCommon):

    def _create_shared_project(self, partner):
        project = self.env['project.project'].with_context(mail_create_nolog=True).create({
            'name': 'Shared Project',
            'privacy_visibility': 'portal',
            'collaborator_ids': [Command.create({'partner_id': partner.id})],
        })
        project.message_subscribe(partner_ids=partner.ids)
        return project

    def test_read_only_user_cannot_change_contractor(self):
        task = self.create_task('Read-only task', self.project_p, contractor_id=self.jane.id)
        self.assertEqual(task.with_user(self.internal_user).read(['name'])[0]['name'], 'Read-only task')
        with self.assertRaises(AccessError):
            task.with_user(self.internal_user).write({'contractor_id': self.acme.id})

    def test_no_new_security_objects(self):
        count = self.env['ir.model.data'].search_count([
            ('module', '=', 'project_contractor'),
            ('model', 'in', ('res.groups', 'res.groups.privilege', 'ir.model.access', 'ir.rule')),
        ])
        self.assertEqual(count, 0)

    def test_classification_and_assignment_grant_nothing(self):
        partner = self.env['res.partner'].create({'name': 'No Access Contractor', 'email': 'no-access@example.com'})
        users_before = self.env['res.users'].with_context(active_test=False).search_count([])
        partner.is_contractor = True
        task = self.create_task('Task', self.project_p, contractor_id=partner.id)
        self.flush_tracking()
        self.assertEqual(self.env['res.users'].with_context(active_test=False).search_count([]), users_before)
        self.assertNotIn(partner, task.message_partner_ids)
        self.assertNotIn(partner, self.project_p.message_partner_ids)
        self.assertNotIn(partner, self.project_p.collaborator_ids.partner_id)
        self.assertFalse(self.env['mail.notification'].search_count([('res_partner_id', '=', partner.id)]))

    def test_portal_user_assigned_as_contractor_gains_no_access(self):
        task = self.create_task('Internal task', self.project_p, contractor_id=self.portal_partner.id)
        with self.assertRaises(AccessError):
            task.with_user(self.portal_user).check_access('read')
        with self.assertRaises(AccessError):
            self.project_p.with_user(self.portal_user).check_access('read')
        self.assertNotIn(self.portal_partner, self.project_p.collaborator_ids.partner_id)

    def test_project_sharing_collaborator_cannot_read_contractor(self):
        project = self._create_shared_project(self.portal_partner)
        task = self.create_task('Shared task', project, contractor_id=self.jane.id)
        portal_task = task.with_user(self.portal_user)
        self.assertEqual(portal_task.read(['name'])[0]['name'], 'Shared task')
        with self.assertRaises(AccessError):
            portal_task.read(['contractor_id'])
        with self.assertRaises(AccessError):
            project.with_user(self.portal_user).read(['contractor_ids'])

    def test_other_company_work_not_counted(self):
        self.create_task('Company A work', self.project_p, contractor_id=self.jane.id)
        self.create_task('Company B work', self.project_b, contractor_id=self.jane.id)
        jane = self.jane.with_user(self.project_user)
        self.assertEqual(jane.with_context(allowed_company_ids=self.company_a.ids).contractor_task_count, 1)
        self.assertEqual(
            jane.with_context(allowed_company_ids=(self.company_a | self.company_b).ids).contractor_task_count, 2)


@tagged('post_install', '-at_install')
class TestContractorPortalRpc(HttpCase):

    def test_portal_rpc_cannot_read_contractor(self):
        portal_user = new_test_user(self.env, login='pc_rpc_portal', groups='base.group_portal')
        contractor = self.env['res.partner'].create({'name': 'RPC Contractor', 'is_contractor': True})
        project = self.env['project.project'].with_context(mail_create_nolog=True).create({
            'name': 'RPC Shared Project',
            'privacy_visibility': 'portal',
            'collaborator_ids': [Command.create({'partner_id': portal_user.partner_id.id})],
        })
        project.message_subscribe(partner_ids=portal_user.partner_id.ids)
        task = self.env['project.task'].create({
            'name': 'RPC Task', 'project_id': project.id, 'contractor_id': contractor.id,
        })

        def read_params(fields):
            return {'model': 'project.task', 'method': 'read', 'args': [[task.id], fields], 'kwargs': {}}

        self.authenticate('pc_rpc_portal', 'pc_rpc_portal')
        result = self.make_jsonrpc_request('/web/dataset/call_kw/project.task/read', read_params(['name']))
        self.assertEqual(result[0]['name'], 'RPC Task')
        with mute_logger('odoo.http'), self.assertRaises(JsonRpcException):
            self.make_jsonrpc_request('/web/dataset/call_kw/project.task/read', read_params(['contractor_id']))
