from odoo.exceptions import AccessError
from odoo.tests import HttpCase, new_test_user

from .common import ProjectContractorCommon


class TestPortalWorkflow(ProjectContractorCommon):
    """Route tests exercise the same request-user ORM boundary as controllers."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = new_test_user(cls.env, login='pc_portal_customer', groups='base.group_portal')
        cls.customer_sibling = new_test_user(cls.env, login='pc_portal_customer_sibling', groups='base.group_portal')
        cls.other_customer = new_test_user(cls.env, login='pc_portal_other_customer', groups='base.group_portal')
        cls.customer_company = cls.env['res.partner'].create({'name': 'Portal Customer', 'is_company': True})
        cls.other_company = cls.env['res.partner'].create({'name': 'Portal Other', 'is_company': True})
        cls.customer.partner_id.parent_id = cls.customer_company
        cls.customer_sibling.partner_id.parent_id = cls.customer_company
        cls.other_customer.partner_id.parent_id = cls.other_company

    def _contractor(self, login):
        user = new_test_user(self.env, login=login, groups='base.group_portal')
        user.with_user(user).action_become_contractor()
        return user

    def test_portal_home_routes_survive_contractor_controller(self):
        routes = {rule.rule for rule in self.env['ir.http'].routing_map().iter_rules()}
        for route in (
            '/my', '/my/home', '/my/contractor', '/my/contractor/contracts',
            '/my/contractor/proposals', '/my/contractor/projects',
        ):
            self.assertIn(route, routes)

    def test_customer_commercial_contract_and_award_journey(self):
        contract = self.env['contract.contract'].with_user(self.customer).create({
            'name': 'Portal Contract', 'partner_id': self.customer_company.id,
        })
        self.assertTrue(self.env['contract.contract'].with_user(self.customer_sibling).search([('id', '=', contract.id)]))
        self.assertFalse(self.env['contract.contract'].with_user(self.other_customer).search([('id', '=', contract.id)]))
        contract.with_user(self.customer_sibling).action_publish()
        contractor = self._contractor('pc_portal_proposer')
        proposal = self.env['contract.proposal'].with_user(contractor).create({'contract_id': contract.id, 'amount': 42})
        proposal.with_user(contractor).action_submit()
        project = proposal.with_user(self.customer).action_accept()
        self.assertEqual(project.contract_id, contract)
        self.assertEqual(project.primary_contractor_id, contractor.partner_id)
        with self.assertRaises(AccessError):
            proposal.with_user(contractor).action_reject()

    def test_contractors_only_get_published_contracts_and_own_work(self):
        contractor_a = self._contractor('pc_portal_contract_a')
        contractor_b = self._contractor('pc_portal_contract_b')
        draft = self.env['contract.contract'].with_user(self.customer).create({'name': 'Private', 'partner_id': self.customer_company.id})
        published = self.env['contract.contract'].with_user(self.customer).create({'name': 'Published', 'partner_id': self.customer_company.id})
        published.with_user(self.customer).action_publish()
        self.assertFalse(self.env['contract.contract'].with_user(contractor_a).search([('id', '=', draft.id)]))
        proposal_a = self.env['contract.proposal'].with_user(contractor_a).create({'contract_id': published.id, 'amount': 10})
        proposal_b = self.env['contract.proposal'].with_user(contractor_b).create({'contract_id': published.id, 'amount': 20})
        proposal_a.with_user(contractor_a).action_submit()
        proposal_b.with_user(contractor_b).action_submit()
        self.assertFalse(self.env['contract.proposal'].with_user(contractor_a).search([('id', '=', proposal_b.id)]))

    def test_award_preserves_only_winner_contract_access_and_routes(self):
        winner = self._contractor('pc_award_winner')
        competitor = self._contractor('pc_award_competitor')
        unrelated = self._contractor('pc_award_unrelated')
        contract = self.env['contract.contract'].with_user(self.customer).create({
            'name': 'Awarded Contract', 'partner_id': self.customer_company.id,
        })
        contract.with_user(self.customer).action_publish()
        self.assertTrue(self.env['contract.contract'].with_user(winner).search([('id', '=', contract.id)]))
        winner_proposal = self.env['contract.proposal'].with_user(winner).create({'contract_id': contract.id, 'amount': 10})
        competitor_proposal = self.env['contract.proposal'].with_user(competitor).create({'contract_id': contract.id, 'amount': 20})
        winner_proposal.with_user(winner).action_submit()
        competitor_proposal.with_user(competitor).action_submit()
        project = winner_proposal.with_user(self.customer).action_accept()
        self.assertEqual(contract.state, 'awarded')
        self.assertTrue(self.env['contract.contract'].with_user(winner).search([('id', '=', contract.id)]))
        self.assertFalse(self.env['contract.contract'].with_user(competitor).search([('id', '=', contract.id)]))
        self.assertFalse(self.env['contract.contract'].with_user(unrelated).search([('id', '=', contract.id)]))
        self.assertTrue(winner_proposal.with_user(winner).exists())
        self.assertTrue(project.with_user(winner).exists())
        self.assertEqual(project.with_user(winner).contract_id, contract.with_user(winner))
        self.assertTrue(self.env['contract.contract'].with_user(self.customer_sibling).search([('id', '=', contract.id)]))

    def test_customer_contract_pages_use_minimal_contractor_identity_projection(self):
        contractor = self._contractor('pc_portal_independent_identity')
        contractor.partner_id.write({'name': 'Independent Contractor', 'email': 'private@example.test'})
        contract = self.env['contract.contract'].with_user(self.customer).create({
            'name': 'Identity Contract', 'partner_id': self.customer_company.id,
        })
        contract.with_user(self.customer).action_publish()
        proposal = self.env['contract.proposal'].with_user(contractor).create({'contract_id': contract.id, 'amount': 11})
        proposal.with_user(contractor).action_submit()
        project = proposal.with_user(self.customer).action_accept()
        with self.assertRaises(AccessError):
            contractor.partner_id.with_user(self.customer).read(['name'])
        identity = contractor.partner_id.sudo().read(['id', 'name'])[0]
        self.assertEqual(identity, {'id': contractor.partner_id.id, 'name': 'Independent Contractor'})
        self.assertTrue(self.env['contract.proposal'].with_user(self.customer).search([('id', '=', proposal.id)]))
        self.assertTrue(self.env['project.project'].with_user(self.customer).search([('id', '=', project.id)]))
        self.assertNotIn('email', identity)
        views = self.env.ref('project_contractor.portal_customer_contract') | self.env.ref('project_contractor.portal_proposal') | self.env.ref('project_contractor.portal_project')
        self.assertNotIn('contractor_id.name', ''.join(views.mapped('arch_db')))
        self.assertNotIn('primary_contractor_id.name', ''.join(views.mapped('arch_db')))


class TestPortalIdentityRenderingHttp(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = new_test_user(cls.env, login='pc_identity_customer', groups='base.group_portal')
        cls.other_customer = new_test_user(cls.env, login='pc_identity_other', groups='base.group_portal')
        customer_company = cls.env['res.partner'].create({'name': 'Identity Customer', 'is_company': True})
        other_company = cls.env['res.partner'].create({'name': 'Identity Other', 'is_company': True})
        cls.customer.partner_id.parent_id = customer_company
        cls.other_customer.partner_id.parent_id = other_company
        cls.contract = cls.env['contract.contract'].with_user(cls.customer).create({
            'name': 'Independent identity rendering', 'partner_id': customer_company.id,
        })
        cls.contract.with_user(cls.customer).action_publish()
        cls.contractor = new_test_user(cls.env, login='pc_identity_contractor', groups='base.group_portal')
        cls.contractor.with_user(cls.contractor).action_become_contractor()
        cls.contractor.partner_id.write({'name': 'Independent Contractor', 'email': 'private@example.test'})
        cls.proposal = cls.env['contract.proposal'].with_user(cls.contractor).create({
            'contract_id': cls.contract.id, 'amount': 11,
        })
        cls.proposal.with_user(cls.contractor).action_submit()
        cls.project = cls.proposal.with_user(cls.customer).action_accept()

    def test_authorized_pages_render_only_contractor_display_identity(self):
        self.authenticate(self.customer.login, self.customer.login)
        for url in (
            f'/my/contracts/{self.contract.id}',
            f'/my/contracts/{self.contract.id}/proposals/{self.proposal.id}',
            f'/my/contracts/{self.contract.id}/projects/{self.project.id}',
        ):
            response = self.url_open(url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Independent Contractor', response.content)
            self.assertNotIn(b'private@example.test', response.content)
        self.authenticate(self.other_customer.login, self.other_customer.login)
        self.assertEqual(self.url_open(f'/my/contracts/{self.contract.id}').status_code, 404)
        self.authenticate(self.contractor.login, self.contractor.login)
        self.assertEqual(self.url_open(f'/my/contractor/proposals/{self.proposal.id}').status_code, 200)
        self.assertEqual(self.url_open(f'/my/contractor/projects/{self.project.id}').status_code, 200)
