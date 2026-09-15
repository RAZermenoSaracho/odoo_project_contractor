from odoo import Command
from odoo.tests import HttpCase, tagged

WAIT_FOR_JS = """
const waitFor = async (selector) => {
    for (let attempt = 0; attempt < 150; attempt++) {
        const element = document.querySelector(selector);
        if (element) {
            return element;
        }
        await new Promise((resolve) => setTimeout(resolve, 100));
    }
    throw new Error(`Element not found: ${selector}`);
};
"""


@tagged('post_install', '-at_install')
class TestContractorUi(HttpCase):
    """Smoke tests rendering the inherited views in the real web client (no JS errors allowed)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Partner = cls.env['res.partner']
        cls.acme = Partner.create({'name': 'UI Acme Consulting', 'is_company': True, 'is_contractor': True})
        cls.bob = Partner.create({'name': 'UI Bob', 'parent_id': cls.acme.id})
        cls.customer = Partner.create({'name': 'UI Client', 'is_company': True})
        cls.project = cls.env['project.project'].create({'name': 'UI Contractor Project', 'partner_id': cls.customer.id})
        cls.task = cls.env['project.task'].create({
            'name': 'UI Contracted Task',
            'project_id': cls.project.id,
            'contractor_id': cls.bob.id,
            'user_ids': [Command.set(cls.env.ref('base.user_admin').ids)],
        })

    def _assert_renders(self, url, selectors):
        checks = "".join(f"await waitFor({selector!r});" for selector in selectors)
        code = WAIT_FOR_JS + f"(async () => {{ {checks} console.log('test successful'); }})();"
        self.browser_js(url, code, login='admin')

    def test_partner_form_shows_classification_and_work_history(self):
        self._assert_renders(f'/odoo/action-base.action_partner_form/{self.acme.id}', [
            "div[name='is_contractor']",
            "button[name='action_view_contractor_tasks']",
            "button[name='action_view_contractor_done_tasks']",
            "button[name='action_view_contractor_projects']",
        ])

    def test_task_form_shows_contractor(self):
        self._assert_renders(f'/odoo/action-project.action_view_all_task/{self.task.id}', [
            "div[name='user_ids']",
            "div[name='contractor_id']",
        ])

    def test_task_kanban_card_shows_contractor(self):
        self._assert_renders('/odoo/action-project.action_view_all_task?view_type=kanban', [
            ".o_kanban_record .o_task_contractor",
        ])

    def test_project_form_shows_contractor_button(self):
        self._assert_renders(f'/odoo/action-project.open_view_project_all/{self.project.id}', [
            "button[name='action_view_contractor_tasks']",
        ])
