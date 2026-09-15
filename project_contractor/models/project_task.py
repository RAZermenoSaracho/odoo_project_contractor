# Part of project_contractor. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class ProjectTask(models.Model):
    _inherit = 'project.task'

    contractor_id = fields.Many2one(
        'res.partner',
        string="Contractor",
        index='btree_not_null',
        tracking=True,
        copy=False,
        domain="['|', ('is_contractor', '=', True), ('commercial_partner_id.is_contractor', '=', True), "
               "'|', ('company_id', '=?', company_id), ('company_id', '=', False)]",
        help="External person or company performing this task. A contractor does not need an Odoo user "
             "and is independent from the task's assignees and customer.",
    )

    @api.model
    def _get_contractor_work_domain(self):
        """Tasks that count as contractor work: archived tasks, task templates and project-template tasks excluded."""
        return (
            Domain('active', '=', True)
            & Domain('has_template_ancestor', '=', False)
            & Domain('has_project_template', '=', False)
        )

    @api.constrains('contractor_id')
    def _check_contractor_eligibility(self):
        # Only triggered when the contractor itself changes: later changes to the partner's
        # classification never invalidate contractors already recorded on tasks.
        for task in self.sudo().filtered('contractor_id'):
            if not task.contractor_id._is_contractor_eligible():
                raise ValidationError(_(
                    "%(contractor)s cannot be the contractor of “%(task)s”: only active contacts marked as "
                    "contractors, or contacts of a contractor company, can be set as contractors.",
                    contractor=task.contractor_id.display_name, task=task.display_name,
                ))

    @api.constrains('contractor_id', 'company_id')
    def _check_contractor_company(self):
        for task in self.sudo().filtered('contractor_id'):
            contractor_company = task.contractor_id.company_id
            if contractor_company and task.company_id and contractor_company != task.company_id:
                raise ValidationError(_(
                    "The contractor %(contractor)s belongs to company %(contractor_company)s and cannot work on "
                    "“%(task)s”, which belongs to company %(task_company)s.",
                    contractor=task.contractor_id.display_name, contractor_company=contractor_company.display_name,
                    task=task.display_name, task_company=task.company_id.display_name,
                ))
