from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import ProjectContractorCommon


@tagged('post_install', '-at_install')
class TestContactClassification(ProjectContractorCommon):

    def _identity_counts(self):
        return (
            self.env['res.users'].with_context(active_test=False).search_count([]),
            self.env['res.partner'].with_context(active_test=False).search_count([]),
        )

    def test_mark_individual_as_contractor(self):
        partner = self.env['res.partner'].create({'name': 'Freelance Jane'})
        before = self._identity_counts()
        partner.with_user(self.project_user).is_contractor = True
        self.assertTrue(partner.is_contractor)
        self.assertEqual(self._identity_counts(), before)
        self.assertFalse(partner.user_ids)

    def test_mark_company_as_contractor(self):
        company = self.env['res.partner'].create({'name': 'New Contractor Co', 'is_company': True})
        company.with_user(self.project_user).is_contractor = True
        self.assertTrue(company.is_contractor)

    def test_new_contacts_are_not_contractors(self):
        partner = self.env['res.partner'].create({'name': 'Somebody'})
        self.assertFalse(partner.is_contractor)

    def test_employee_of_contractor_company_is_eligible(self):
        self.assertFalse(self.bob.is_contractor)
        self.assertTrue(self.bob._is_contractor_eligible())
        eligible = self.env['res.partner'].search(self.env['res.partner']._get_contractor_eligible_domain())
        self.assertIn(self.bob, eligible)

    def test_contact_of_non_contractor_company_is_not_eligible(self):
        self.assertFalse(self.carol._is_contractor_eligible())
        eligible = self.env['res.partner'].search(self.env['res.partner']._get_contractor_eligible_domain())
        self.assertNotIn(self.carol, eligible)

    def test_individually_marked_contact_under_non_contractor_company(self):
        self.assertTrue(self.dan._is_contractor_eligible())
        self.assertFalse(self.client.is_contractor)
        self.assertFalse(self.client._is_contractor_eligible())

    def test_company_flag_does_not_change_contacts_classification(self):
        self.acme.is_contractor = False
        self.assertFalse(self.bob.is_contractor)
        self.assertFalse(self.bob._is_contractor_eligible())
        self.acme.is_contractor = True
        self.assertFalse(self.bob.is_contractor)
        self.assertTrue(self.bob._is_contractor_eligible())

    def test_contractor_filter(self):
        domain = self.get_search_filter_domain('res.partner', 'contractors')
        fixtures = self.jane | self.acme | self.bob | self.client | self.carol | self.dan
        result = self.env['res.partner'].with_user(self.project_user).search(domain)
        self.assertEqual(result & fixtures, self.jane | self.acme | self.bob | self.dan)

    def test_customer_can_also_be_contractor(self):
        self.project_p.partner_id = self.acme
        task = self.create_task('Work for project Q', self.project_q, contractor_id=self.acme.id)
        self.assertEqual(self.project_p.partner_id, self.acme)
        self.assertEqual(task.contractor_id, self.acme)

    def test_unmarking_preserves_history(self):
        tasks = self.env['project.task']
        for index in range(3):
            tasks |= self.create_task(f'Jane task {index}', self.project_p, contractor_id=self.jane.id)
        self.jane.is_contractor = False
        self.assertEqual(tasks.contractor_id, self.jane)
        self.assertEqual(len(tasks.filtered(lambda t: t.contractor_id == self.jane)), 3)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.create_task('Jane task 4', self.project_p, contractor_id=self.jane.id)

    def test_archiving_preserves_history(self):
        task = self.create_task('Jane task', self.project_p, contractor_id=self.jane.id)
        self.jane.action_archive()
        self.assertEqual(task.contractor_id, self.jane)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.create_task('Another Jane task', self.project_p, contractor_id=self.jane.id)
