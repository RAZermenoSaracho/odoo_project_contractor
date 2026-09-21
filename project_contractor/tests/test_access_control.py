from odoo.exceptions import AccessError
from odoo.tests import new_test_user, tagged

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestContractorAccessControl(ProjectContractorCommon):
    def _activate_contractor(self, login='pc_contractor'):
        user = new_test_user(self.env, login=login, groups='base.group_portal')
        partner_id = user.partner_id.id
        user.with_user(user).action_become_contractor()
        return user, partner_id

    def test_activation_is_identity_preserving_and_idempotent(self):
        user = new_test_user(self.env, login='pc_activation', groups='base.group_portal')
        partner_id = user.partner_id.id
        user.with_user(user).action_become_contractor()
        self.assertEqual(user.partner_id.id, partner_id)
        self.assertTrue(user.is_contractor_user)
        self.assertFalse(user.share)
        self.assertTrue(user.has_group('project_contractor.group_contractor'))
        user.with_user(user).action_become_contractor()
        self.assertEqual(user.partner_id.id, partner_id)

    def test_contractor_can_only_access_own_partner(self):
        contractor, partner_id = self._activate_contractor()
        own_partner = self.env['res.partner'].with_user(contractor).browse(partner_id)
        own_partner.write({'phone': '555-0100'})
        with self.assertRaises(AccessError):
            self.jane.with_user(contractor).read(['name'])
        with self.assertRaises(AccessError):
            self.env['res.partner'].with_user(contractor).create({'name': 'Denied'})
        with self.assertRaises(AccessError):
            own_partner.unlink()

    def test_internal_users_keep_ordinary_access(self):
        self.assertEqual(self.project_p.with_user(self.project_user).read(['name'])[0]['name'], self.project_p.name)
        self.project_p.with_user(self.env.ref('base.user_admin')).write({'name': 'Admin write'})
        self.assertEqual(self.project_p.name, 'Admin write')
