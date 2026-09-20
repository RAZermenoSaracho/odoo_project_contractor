from odoo import Command, _, fields, models
from odoo.exceptions import AccessError


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_contractor_user = fields.Boolean(copy=False, readonly=True)

    def action_become_contractor(self):
        self.ensure_one()
        if self != self.env.user or not self.share:
            raise AccessError(_("Only your portal account can become a Contractor."))
        self.partner_id.sudo().write({'is_contractor': True})
        group = self.env.ref('project_contractor.group_contractor')
        self.sudo().write({'is_contractor_user': True, 'group_ids': [Command.set(group.ids)]})
        return True
