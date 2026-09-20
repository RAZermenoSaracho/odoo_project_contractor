from odoo import http
from odoo.http import request


class ContractorPortal(http.Controller):
    @http.route('/my/contractor', type='http', auth='user', website=True)
    def home(self):
        return request.render('project_contractor.contractor_portal_home', {'user': request.env.user})

    @http.route('/my/contractor/activate', type='http', auth='user', website=True, methods=['POST'])
    def activate(self):
        request.env.user.action_become_contractor()
        return request.redirect('/my/contractor/contracts')

    @http.route('/my/contractor/contracts', type='http', auth='user', website=True)
    def contracts(self):
        return request.render('project_contractor.contractor_portal_contracts', {
            'user': request.env.user, 'projects': request.env['project.project'].search([]),
        })
