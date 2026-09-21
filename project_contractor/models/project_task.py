# Part of project_contractor. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
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

    def _contractor_invalidate_derived_values(self, contractors=None, projects=None):
        contractors = (contractors or self.env['res.partner']).with_context(active_test=False)
        if contractors:
            contractors._contractor_invalidate_work_history()
        projects = projects or self.env['project.project']
        if projects:
            projects.invalidate_recordset(['contractor_ids', 'contractor_count'])

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.user.is_contractor_user:
            project_ids = [vals.get('project_id') for vals in vals_list]
            projects = self.env['project.project'].browse([project_id for project_id in project_ids if project_id])
            if not all(project_ids) or any(not project._is_assigned_contractor() for project in projects):
                raise AccessError(_("Only the Assigned Contractor can create Tasks in their Project."))
        # Project's mail-enabled create path rechecks its broad ACL after the
        # narrow assigned-Project guard above.  Create as sudo only after that
        # exact scope check, then return to the caller's environment.
        tasks = (super(ProjectTask, self.sudo()).create(vals_list).with_env(self.env)
                 if self.env.user.is_contractor_user else super().create(vals_list))
        tasks._contractor_invalidate_derived_values(tasks.mapped('contractor_id'), tasks.mapped('project_id'))
        return tasks

    def write(self, vals):
        if self.env.user.is_contractor_user:
            if 'project_id' in vals:
                raise AccessError(_("Contractors cannot move Tasks between Projects."))
            if any(not task.project_id._is_assigned_contractor() for task in self):
                raise AccessError(_("Only the Assigned Contractor can update Tasks in their Project."))
        contractors = self.mapped('contractor_id')
        projects = self.mapped('project_id')
        result = super().write(vals)
        if {'contractor_id', 'project_id', 'active', 'is_template', 'has_template_ancestor', 'has_project_template', 'state'} & vals.keys():
            self._contractor_invalidate_derived_values(
                contractors | self.mapped('contractor_id'), projects | self.mapped('project_id'),
            )
        return result

    def unlink(self):
        if self.env.user.is_contractor_user:
            if any(not task.project_id._is_assigned_contractor() for task in self):
                raise AccessError(_("Only the Assigned Contractor can delete Tasks in their Project."))
        contractors = self.mapped('contractor_id')
        projects = self.mapped('project_id')
        result = super().unlink()
        self._contractor_invalidate_derived_values(contractors, projects)
        return result
