from odoo.exceptions import AccessError
from odoo.tests import new_test_user

from .common import ProjectContractorCommon


class TestPrivateCommunication(ProjectContractorCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Partner = cls.env['res.partner']
        cls.customer_company = Partner.create({'name': 'Communication Customer', 'is_company': True})
        cls.other_customer_company = Partner.create({'name': 'Unrelated Customer', 'is_company': True})
        cls.customer = new_test_user(cls.env, login='pc_communication_customer', groups='base.group_portal')
        cls.customer.partner_id.parent_id = cls.customer_company
        cls.other_customer = new_test_user(cls.env, login='pc_communication_other_customer', groups='base.group_portal')
        cls.other_customer.partner_id.parent_id = cls.other_customer_company
        cls.contractor_a = cls._contractor('pc_communication_a')
        cls.contractor_b = cls._contractor('pc_communication_b')
        cls.contractor_c = cls._contractor('pc_communication_c')

    @classmethod
    def _contractor(cls, login):
        user = new_test_user(cls.env, login=login, groups='base.group_portal')
        user.with_user(user).action_become_contractor()
        return user

    def _contract(self, name='Private communication Contract'):
        contract = self.env['contract.contract'].with_user(self.customer).create({
            'name': name,
            'partner_id': self.customer_company.id,
        })
        contract.with_user(self.customer).action_publish()
        return contract

    def _proposal(self, contract, contractor, amount):
        proposal = self.env['contract.proposal'].with_user(contractor).create({
            'contract_id': contract.id,
            'amount': amount,
        })
        proposal.with_user(contractor).action_submit()
        return proposal

    def _message_ids(self, user, record):
        return self.env['mail.message'].with_user(user).search([
            ('model', '=', record._name), ('res_id', '=', record.id),
        ]).ids

    def test_proposal_chatter_uses_record_access_not_followers_or_discuss(self):
        contract = self._contract()
        proposal_a = self._proposal(contract, self.contractor_a, 100)
        proposal_b = self._proposal(contract, self.contractor_b, 200)

        customer_message = proposal_a.with_user(self.customer).message_post(
            body='Customer to A', message_type='comment', subtype_xmlid='mail.mt_comment')
        contractor_message = proposal_a.with_user(self.contractor_a).message_post(
            body='A to customer', message_type='comment', subtype_xmlid='mail.mt_comment')
        proposal_b.with_user(self.customer).message_post(
            body='Customer to B', message_type='comment', subtype_xmlid='mail.mt_comment')

        self.assertIn(customer_message.id, self._message_ids(self.customer, proposal_a))
        self.assertIn(contractor_message.id, self._message_ids(self.contractor_a, proposal_a))
        self.assertIn(customer_message.id, self._message_ids(self.customer, proposal_a))
        self.assertNotIn(customer_message.id, self._message_ids(self.contractor_a, proposal_b))
        self.assertNotIn(customer_message.id, self._message_ids(self.contractor_b, proposal_a))
        self.assertNotIn(customer_message.id, self._message_ids(self.contractor_c, proposal_a))
        self.assertNotIn(customer_message.id, self._message_ids(self.other_customer, proposal_a))
        self.assertTrue(contract.with_user(self.contractor_c).exists())
        self.assertFalse(self.env['contract.proposal'].with_user(self.contractor_c).search([
            ('id', '=', proposal_a.id),
        ]))
        with self.assertRaises(AccessError):
            customer_message.with_user(self.contractor_b).read(['body'])
        with self.assertRaises(AccessError):
            proposal_b.with_user(self.contractor_a).message_post(
                body='Cross-proposal denial', message_type='comment', subtype_xmlid='mail.mt_comment')
        self.assertFalse(proposal_a.with_user(self.contractor_b).message_subscribe([
            self.contractor_b.partner_id.id,
        ]))
        self.assertNotIn(self.contractor_b.partner_id, proposal_a.message_partner_ids)

    def test_proposal_lifecycle_preserves_only_own_history(self):
        contract = self._contract('Lifecycle communication Contract')
        proposal_a = self._proposal(contract, self.contractor_a, 100)
        proposal_b = self._proposal(contract, self.contractor_b, 200)
        proposal_c = self._proposal(contract, self.contractor_c, 300)
        message_a = proposal_a.with_user(self.contractor_a).message_post(
            body='Accepted negotiation history', message_type='comment', subtype_xmlid='mail.mt_comment')
        message_b = proposal_b.with_user(self.contractor_b).message_post(
            body='Rejected negotiation history', message_type='comment', subtype_xmlid='mail.mt_comment')
        message_c = proposal_c.with_user(self.contractor_c).message_post(
            body='Withdrawn negotiation history', message_type='comment', subtype_xmlid='mail.mt_comment')
        proposal_c.with_user(self.contractor_c).action_withdraw()
        project = proposal_a.with_user(self.customer).action_accept()

        self.assertEqual(proposal_a.state, 'accepted')
        self.assertEqual(proposal_b.state, 'rejected')
        self.assertEqual(proposal_c.state, 'withdrawn')
        self.assertIn(message_a.id, self._message_ids(self.contractor_a, proposal_a))
        self.assertIn(message_b.id, self._message_ids(self.contractor_b, proposal_b))
        self.assertIn(message_c.id, self._message_ids(self.contractor_c, proposal_c))
        self.assertNotIn(message_b.id, self._message_ids(self.contractor_a, proposal_b))
        self.assertNotIn(message_c.id, self._message_ids(self.contractor_a, proposal_c))
        self.assertNotIn(message_a.id, self._message_ids(self.contractor_b, proposal_a))
        accepted_followup = proposal_a.with_user(self.contractor_a).message_post(
            body='Accepted proposal follow-up', message_type='comment', subtype_xmlid='mail.mt_comment')
        rejected_followup = proposal_b.with_user(self.contractor_b).message_post(
            body='Rejected proposal follow-up', message_type='comment', subtype_xmlid='mail.mt_comment')
        withdrawn_followup = proposal_c.with_user(self.contractor_c).message_post(
            body='Withdrawn proposal follow-up', message_type='comment', subtype_xmlid='mail.mt_comment')
        self.assertIn(accepted_followup.id, self._message_ids(self.contractor_a, proposal_a))
        self.assertIn(rejected_followup.id, self._message_ids(self.contractor_b, proposal_b))
        self.assertIn(withdrawn_followup.id, self._message_ids(self.contractor_c, proposal_c))
        self.assertTrue(project)

    def test_awarded_project_chatter_is_operational_and_read_only_for_customer(self):
        contract = self._contract('Project communication Contract')
        proposal_a = self._proposal(contract, self.contractor_a, 100)
        proposal_b = self._proposal(contract, self.contractor_b, 200)
        proposal_message = proposal_b.with_user(self.contractor_b).message_post(
            body='Competing proposal secret', message_type='comment', subtype_xmlid='mail.mt_comment')
        project = proposal_a.with_user(self.customer).action_accept()

        customer_message = project.with_user(self.customer).message_post(
            body='Customer operational update', message_type='comment', subtype_xmlid='mail.mt_comment')
        contractor_message = project.with_user(self.contractor_a).message_post(
            body='Assigned contractor update', message_type='comment', subtype_xmlid='mail.mt_comment')
        admin_message = project.message_post(
            body='Internal operational update', message_type='comment', subtype_xmlid='mail.mt_comment')

        self.assertIn(customer_message.id, self._message_ids(self.customer, project))
        self.assertIn(contractor_message.id, self._message_ids(self.contractor_a, project))
        self.assertIn(admin_message.id, self._message_ids(self.env.user, project))
        self.assertNotIn(customer_message.id, self._message_ids(self.contractor_b, project))
        self.assertNotIn(customer_message.id, self._message_ids(self.contractor_c, project))
        self.assertNotIn(proposal_message.id, self._message_ids(self.contractor_a, proposal_b))
        with self.assertRaises(AccessError):
            project.with_user(self.customer).write({'name': 'Customer cannot mutate execution'})
        with self.assertRaises(AccessError):
            project.with_user(self.contractor_b).message_post(
                body='Unauthorized operational update', message_type='comment', subtype_xmlid='mail.mt_comment')
