import ast
import os
import re

from lxml import etree

from odoo import Command
from odoo.tests import tagged

from .common import ProjectContractorCommon

ADDON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@tagged('post_install', '-at_install')
class TestDistribution(ProjectContractorCommon):

    @classmethod
    def _manifest(cls):
        with open(os.path.join(ADDON_DIR, '__manifest__.py'), encoding='utf-8') as manifest_file:
            return ast.literal_eval(manifest_file.read())

    def test_declared_dependencies(self):
        self.assertEqual(self._manifest()['depends'], ['project', 'portal', 'website', 'mail'])

    def test_no_hooks_routes_or_assets(self):
        manifest = self._manifest()
        for key in ('pre_init_hook', 'post_init_hook', 'uninstall_hook', 'post_load', 'assets', 'external_dependencies'):
            self.assertNotIn(key, manifest)
        self.assertFalse(manifest.get('application'))

    def test_license_consistency(self):
        self.assertEqual(self._manifest()['license'], 'LGPL-3')
        license_path = os.path.join(os.path.dirname(ADDON_DIR), 'LICENSE')
        if not os.path.exists(license_path):
            self.skipTest("Repository LICENSE file not shipped alongside the addon")
        with open(license_path, encoding='utf-8') as license_file:
            text = license_file.read()
        self.assertIn('GNU LESSER GENERAL PUBLIC LICENSE', text)
        self.assertIn('Version 3, 29 June 2007', text)

    def test_labels_say_contractor(self):
        for model, field_name in (('res.partner', 'is_contractor'), ('project.task', 'contractor_id'),
                                  ('project.project', 'contractor_ids')):
            self.assertIn('Contractor', self.env[model]._fields[field_name].string)
        view_ids = self.env['ir.model.data'].search([
            ('module', '=', 'project_contractor'), ('model', '=', 'ir.ui.view'),
        ]).mapped('res_id')
        labels = []
        for view in self.env['ir.ui.view'].browse(view_ids):
            root = etree.fromstring(view.arch_db)
            labels += [node.get(attr) for node in root.iter() for attr in ('string', 'title', 'aria-label')
                       if node.get(attr)]
        self.assertTrue(labels)
        self.assertTrue(any('Contract' in label for label in labels))

    def test_defaults_leave_standard_data_unchanged(self):
        partner = self.env['res.partner'].create({'name': 'Plain contact'})
        task = self.create_task(
            'Plain task', self.project_p, user_ids=[Command.set(self.project_user.ids)], partner_id=self.client.id,
        )
        self.assertFalse(partner.is_contractor)
        self.assertFalse(task.contractor_id)
        self.assertEqual(task.user_ids, self.project_user)
        self.assertEqual(task.partner_id, self.client)
        self.assertEqual(task.state, '01_in_progress')
        self.assertEqual(self.project_p.with_user(self.project_user).contractor_count, 0)
