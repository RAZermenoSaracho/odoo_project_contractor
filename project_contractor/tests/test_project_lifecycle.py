from odoo.exceptions import AccessError
from odoo.tests import new_test_user, tagged

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestContractProposalWorkflow(ProjectContractorCommon):
    def _contractor(self, login):
        user = new_test_user(self.env, login=login, groups='base.group_portal')
        user.with_user(user).action_become_contractor()
        self.env.invalidate_all()
        return self.env['res.users'].browse(user.id)

    def _customer(self, login, partner):
        user = new_test_user(self.env, login=login, groups='base.group_portal')
        user.partner_id.parent_id = partner
        return user

    def _published_contract(self, customer):
        contract = self.env['contract.contract'].with_user(customer).create({'name': 'Roof repair', 'partner_id': self.client.id})
        contract.with_user(customer).action_publish()
        return contract

    def test_commercial_customer_contract_authority(self):
        customer = self._customer('pc_contract_customer', self.client)
        colleague = self._customer('pc_contract_colleague', self.client)
        outsider = self._customer('pc_contract_outsider', self.jane)
        contract = self._published_contract(customer)
        contract.with_user(colleague).write({'name': 'Updated roof repair'})
        self.assertEqual(contract.name, 'Updated roof repair')
        with self.assertRaises(AccessError):
            contract.with_user(outsider).write({'name': 'Denied'})

    def test_contract_and_proposal_contractor_isolation(self):
        customer = self._customer('pc_isolation_customer', self.client)
        contractor_a = self._contractor('pc_proposal_a')
        contractor_b = self._contractor('pc_proposal_b')
        draft = self.env['contract.contract'].with_user(customer).create({'name': 'Private', 'partner_id': self.client.id})
        contract = self._published_contract(customer)
        ContractA = self.env['contract.contract'].with_user(contractor_a)
        self.assertEqual(ContractA.search([('id', 'in', (draft | contract).ids)]), contract)
        with self.assertRaises(AccessError):
            draft.with_user(contractor_a).read(['name'])
        with self.assertRaises(AccessError):
            contract.with_user(contractor_a).write({'name': 'Denied'})
        with self.assertRaises(AccessError):
            ContractA.create({'name': 'Denied', 'partner_id': self.client.id})
        proposal_a = self.env['contract.proposal'].with_user(contractor_a).create({'contract_id': contract.id, 'amount': 1200})
        proposal_b = self.env['contract.proposal'].with_user(contractor_b).create({'contract_id': contract.id, 'amount': 1400})
        proposal_a.with_user(contractor_a).action_submit()
        proposal_b.with_user(contractor_b).action_submit()
        self.assertEqual(proposal_a.currency_id, self.env.company.currency_id)
        self.assertEqual(self.env['contract.proposal'].with_user(contractor_a).search([]), proposal_a)
        with self.assertRaises(AccessError):
            proposal_b.with_user(contractor_a).read(['amount'])
        with self.assertRaises(AccessError):
            proposal_a.with_user(contractor_b).unlink()

    def test_acceptance_is_authorized_atomic_and_idempotent(self):
        customer = self._customer('pc_accept_customer', self.client)
        outsider = self._customer('pc_accept_outsider', self.jane)
        contractor_a = self._contractor('pc_accept_a')
        contractor_b = self._contractor('pc_accept_b')
        contract = self._published_contract(customer)
        proposal_a = self.env['contract.proposal'].with_user(contractor_a).create({'contract_id': contract.id, 'amount': 1200})
        proposal_b = self.env['contract.proposal'].with_user(contractor_b).create({'contract_id': contract.id, 'amount': 1300})
        proposal_a.with_user(contractor_a).action_submit()
        proposal_b.with_user(contractor_b).action_submit()
        with self.assertRaises(AccessError):
            proposal_a.with_user(outsider).action_accept()
        project = proposal_a.with_user(customer).action_accept()
        self.assertEqual(contract.state, 'awarded')
        self.assertEqual(contract.accepted_proposal_id, proposal_a)
        self.assertEqual(proposal_a.state, 'accepted')
        self.assertEqual(proposal_b.state, 'rejected')
        self.assertEqual(project.contract_id, contract)
        self.assertEqual(project.accepted_proposal_id, proposal_a)
        self.assertEqual(project.primary_contractor_id, contractor_a.partner_id)
        self.assertEqual(project.agreed_amount, proposal_a.amount)
        self.assertEqual(project.agreed_currency_id, proposal_a.currency_id)
        self.assertEqual(proposal_a.with_user(customer).action_accept(), project)
        self.assertEqual(self.env['project.project'].search_count([('contract_id', '=', contract.id)]), 1)

    def test_awarded_project_is_assigned_contractor_only(self):
        customer = self._customer('pc_project_customer', self.client)
        contractor_a = self._contractor('pc_project_a')
        contractor_b = self._contractor('pc_project_b')
        contract = self._published_contract(customer)
        proposal = self.env['contract.proposal'].with_user(contractor_a).create({'contract_id': contract.id, 'amount': 100})
        proposal.with_user(contractor_a).action_submit()
        project = proposal.with_user(customer).action_accept()
        unassigned = self.env['project.project'].create({'name': 'Unassigned', 'privacy_visibility': 'employees'})
        ProjectA = self.env['project.project'].with_user(contractor_a)
        self.assertTrue(self.env['project.task'].with_user(contractor_a).has_access('create'))
        self.assertEqual(ProjectA.search([('id', 'in', (project | unassigned).ids)]), project)
        self.assertFalse(self.env['project.project'].with_user(contractor_b).search([('id', '=', project.id)]))
        project.with_user(contractor_a).write({'name': 'Contractor update'})
        task = self.env['project.task'].with_user(contractor_a).create({'name': 'Execution task', 'project_id': project.id})
        task.with_user(contractor_a).write({'name': 'Updated execution task'})
        task.with_user(contractor_a).unlink()
        with self.assertRaises(AccessError):
            project.with_user(contractor_a).write({'primary_contractor_id': contractor_b.partner_id.id})
        with self.assertRaises(AccessError):
            self.env['project.task'].with_user(contractor_b).create({'name': 'Denied', 'project_id': project.id})

    def test_contract_navigation_actions_and_won_contracts(self):
        customer = self._customer('pc_navigation_customer', self.client)
        contractor_a = self._contractor('pc_navigation_a')
        contractor_b = self._contractor('pc_navigation_b')
        won_contract = self._published_contract(customer)
        won_proposal = self.env['contract.proposal'].with_user(contractor_a).create({
            'contract_id': won_contract.id, 'amount': 100,
        })
        losing_proposal = self.env['contract.proposal'].with_user(contractor_b).create({
            'contract_id': won_contract.id, 'amount': 200,
        })
        won_proposal.with_user(contractor_a).action_submit()
        losing_proposal.with_user(contractor_b).action_submit()
        project = won_proposal.with_user(customer).action_accept()
        other_contract = self._published_contract(customer)
        other_proposal = self.env['contract.proposal'].with_user(contractor_a).create({
            'contract_id': other_contract.id, 'amount': 300,
        })

        self.assertEqual(won_contract.proposal_count, 2)
        proposal_action = won_contract.action_view_proposals()
        self.assertEqual(proposal_action['domain'], [('contract_id', '=', won_contract.id)])
        self.assertEqual(
            self.env['contract.proposal'].search(proposal_action['domain']), won_proposal | losing_proposal,
        )
        self.assertEqual(won_contract.action_view_project()['res_id'], project.id)
        self.assertEqual(project.action_view_contract()['res_id'], won_contract.id)
        self.assertFalse(other_contract.action_view_project())

        partner = contractor_a.partner_id
        self.assertEqual(partner.contractor_won_contract_count, 1)
        won_action = partner.action_view_contractor_won_contracts()
        self.assertEqual(won_action['domain'], [('accepted_proposal_id.contractor_id', '=', partner.id)])
        self.assertEqual(self.env['contract.contract'].search(won_action['domain']), won_contract)
        self.assertNotIn(other_contract, self.env['contract.contract'].search(won_action['domain']))
        self.assertEqual(other_proposal.state, 'draft')
