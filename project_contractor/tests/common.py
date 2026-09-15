import ast

from lxml import etree

from odoo import Command
from odoo.tests import TransactionCase, new_test_user


class ProjectContractorCommon(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env.company
        cls.company_b = cls.env['res.company'].create({'name': 'Contractor Test Company B'})

        cls.project_user = new_test_user(
            cls.env, login='pc_project_user',
            groups='base.group_user,base.group_partner_manager,project.group_project_user',
            company_id=cls.company_a.id,
            company_ids=[Command.set((cls.company_a | cls.company_b).ids)],
        )
        # Internal user without Project rights: may read tasks (upstream ACL) but not edit them.
        cls.internal_user = new_test_user(cls.env, login='pc_internal_user', groups='base.group_user')
        cls.portal_user = new_test_user(cls.env, login='pc_portal_user', groups='base.group_portal')

        Partner = cls.env['res.partner']
        cls.jane = Partner.create({'name': 'Jane Doe', 'is_contractor': True})
        cls.acme = Partner.create({'name': 'Acme Consulting', 'is_company': True, 'is_contractor': True})
        cls.bob = Partner.create({'name': 'Bob', 'parent_id': cls.acme.id})
        cls.client = Partner.create({'name': 'Client Corp', 'is_company': True})
        cls.carol = Partner.create({'name': 'Carol', 'parent_id': cls.client.id})
        cls.dan = Partner.create({'name': 'Dan', 'parent_id': cls.client.id, 'is_contractor': True})
        cls.company_b_contractor = Partner.create({
            'name': 'Company B Contractor', 'is_contractor': True, 'company_id': cls.company_b.id,
        })
        cls.portal_partner = cls.portal_user.partner_id
        cls.portal_partner.is_contractor = True

        Project = cls.env['project.project'].with_context(mail_create_nolog=True)
        cls.project_p = Project.create({
            'name': 'Contractor Project P', 'privacy_visibility': 'employees', 'company_id': cls.company_a.id,
        })
        cls.project_q = Project.create({
            'name': 'Contractor Project Q', 'privacy_visibility': 'employees', 'company_id': cls.company_a.id,
        })
        cls.project_restricted = Project.create({
            'name': 'Restricted Project', 'privacy_visibility': 'followers', 'company_id': cls.company_a.id,
        })
        cls.project_b = Project.create({
            'name': 'Company B Project', 'privacy_visibility': 'employees', 'company_id': cls.company_b.id,
        })

    @classmethod
    def create_task(cls, name, project, **values):
        return cls.env['project.task'].with_context(mail_create_nolog=True).create({
            'name': name, 'project_id': project.id, **values,
        })

    def get_search_filter(self, model, filter_name, view_xmlid=None):
        view_id = self.env.ref(view_xmlid).id if view_xmlid else False
        arch = self.env[model].get_views([(view_id, 'search')])['views']['search']['arch']
        node = etree.fromstring(arch).find(f".//filter[@name='{filter_name}']")
        self.assertIsNotNone(node, f"Search filter {filter_name} not found on {model}")
        return node

    def get_search_filter_domain(self, model, filter_name, view_xmlid=None):
        return ast.literal_eval(self.get_search_filter(model, filter_name, view_xmlid).get('domain'))

    def flush_tracking(self):
        self.env.flush_all()
        self.env.cr.precommit.run()
