from odoo.exceptions import AccessError
from odoo.tests import new_test_user

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
