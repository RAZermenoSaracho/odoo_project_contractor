from odoo import _, http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from werkzeug.exceptions import Forbidden, NotFound


class ContractorPortal(CustomerPortal):
    """Portal presentation only; ordinary ORM checks remain authoritative."""
    def _record(self, model, record_id):
        record = request.env[model].browse(record_id).exists()
        if not record:
            raise NotFound()
        try:
            record.check_access('read')
        except AccessError as exc:
            raise NotFound() from exc
        return record

    def _customer_contract(self, contract_id):
        contract = self._record('contract.contract', contract_id)
        if not contract._is_customer_owner():
            raise NotFound()
        return contract

    def _render(self, template, **values):
        values.update(self._prepare_portal_layout_values())
        return request.render(template, values)

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'contractor_contract_count' in counters:
            values['contractor_contract_count'] = request.env['contract.contract'].search_count([])
        if 'customer_contract_count' in counters:
            values['customer_contract_count'] = request.env['contract.contract'].search_count([])
        if 'contractor_project_count' in counters:
            values['contractor_project_count'] = request.env['project.project'].search_count([])
        return values

    @http.route('/my/contractor', type='http', auth='user', website=True)
    def contractor_home(self):
        return self._render('project_contractor.contractor_portal_home', user=request.env.user)

    @http.route('/my/contracts', type='http', auth='user', website=True)
    def customer_contracts(self):
        return self._render('project_contractor.portal_customer_contracts', contracts=request.env['contract.contract'].search([]), page_name='contracts')

    @http.route('/my/contracts/new', type='http', auth='user', website=True)
    def customer_contract_new(self):
        return self._render('project_contractor.portal_customer_contract_form', page_name='contract_new')

    @http.route('/my/contracts/create', type='http', auth='user', website=True, methods=['POST'])
    def customer_contract_create(self, name=None, **post):
        name = (name or '').strip()
        if not name:
            return self._render('project_contractor.portal_customer_contract_form', error=_('A Contract name is required.'), page_name='contract_new')
        contract = request.env['contract.contract'].create({'name': name, 'partner_id': request.env.user.partner_id.commercial_partner_id.id})
        return request.redirect(f'/my/contracts/{contract.id}')

    @http.route('/my/contracts/<int:contract_id>', type='http', auth='user', website=True)
    def customer_contract(self, contract_id):
        return self._render('project_contractor.portal_customer_contract', contract=self._customer_contract(contract_id), page_name='contract')

    @http.route('/my/contracts/<int:contract_id>/update', type='http', auth='user', website=True, methods=['POST'])
    def customer_contract_update(self, contract_id, name=None, **post):
        contract = self._customer_contract(contract_id)
        if contract.state != 'draft' or not (name or '').strip():
            raise Forbidden()
        contract.write({'name': name.strip()})
        return request.redirect(f'/my/contracts/{contract.id}')

    @http.route('/my/contracts/<int:contract_id>/<string:action>', type='http', auth='user', website=True, methods=['POST'])
    def customer_contract_action(self, contract_id, action, **post):
        contract = self._customer_contract(contract_id)
        if action == 'publish': contract.action_publish()
        elif action == 'cancel': contract.action_cancel()
        else: raise NotFound()
        return request.redirect(f'/my/contracts/{contract.id}')

    @http.route('/my/contracts/<int:contract_id>/proposals/<int:proposal_id>', type='http', auth='user', website=True)
    def customer_proposal(self, contract_id, proposal_id):
        contract, proposal = self._customer_contract(contract_id), self._record('contract.proposal', proposal_id)
        if proposal.contract_id != contract: raise NotFound()
        return self._proposal_page(proposal, True, f'/my/contracts/{contract.id}/proposals/{proposal.id}')

    @http.route('/my/contracts/<int:contract_id>/proposals/<int:proposal_id>/<string:action>', type='http', auth='user', website=True, methods=['POST'])
    def customer_proposal_action(self, contract_id, proposal_id, action, **post):
        contract, proposal = self._customer_contract(contract_id), self._record('contract.proposal', proposal_id)
        if proposal.contract_id != contract: raise NotFound()
        if action == 'accept':
            project = proposal.action_accept()
            return request.redirect(f'/my/contracts/{contract.id}/projects/{project.id}')
        if action == 'reject': proposal.action_reject()
        elif action != 'reject': raise NotFound()
        return request.redirect(f'/my/contracts/{contract.id}/proposals/{proposal.id}')

    @http.route('/my/contracts/<int:contract_id>/contractors', type='http', auth='user', website=True)
    def customer_contractors(self, contract_id):
        contract = self._customer_contract(contract_id)
        contractors = request.env['res.partner'].sudo().search(request.env['res.partner']._get_contractor_eligible_domain())
        return self._render('project_contractor.portal_contractors', contract=contract, contractors=contractors, page_name='contractors')

    @http.route('/my/contracts/<int:contract_id>/contractors/<int:partner_id>/invite', type='http', auth='user', website=True, methods=['POST'])
    def customer_invite(self, contract_id, partner_id, **post):
        contract = self._customer_contract(contract_id)
        contract.action_invite_contractor(partner_id)
        return request.redirect(f'/my/contracts/{contract.id}')

    @http.route('/my/contracts/<int:contract_id>/projects/<int:project_id>', type='http', auth='user', website=True)
    def customer_project(self, contract_id, project_id):
        contract, project = self._customer_contract(contract_id), self._record('project.project', project_id)
        if project.contract_id != contract: raise NotFound()
        return self._project_page(project, True, f'/my/contracts/{contract.id}/projects/{project.id}')

    @http.route('/my/contractor/activate', type='http', auth='user', website=True, methods=['POST'])
    def activate(self, **post):
        request.env.user.action_become_contractor()
        return request.redirect('/my/contractor/contracts')

    def _contractor(self):
        if not request.env.user.is_contractor_user: raise NotFound()

    @http.route('/my/contractor/contracts', type='http', auth='user', website=True)
    def contracts(self):
        self._contractor()
        return self._render('project_contractor.contractor_portal_contracts', contracts=request.env['contract.contract'].search([]), page_name='contractor_contracts')

    @http.route('/my/contractor/contracts/<int:contract_id>', type='http', auth='user', website=True)
    def contractor_contract(self, contract_id):
        self._contractor(); contract = self._record('contract.contract', contract_id)
        proposal = request.env['contract.proposal'].search([('contract_id', '=', contract.id)], limit=1)
        return self._render('project_contractor.portal_contractor_contract', contract=contract, proposal=proposal, page_name='contractor_contract')

    @http.route('/my/contractor/contracts/<int:contract_id>/proposal/create', type='http', auth='user', website=True, methods=['POST'])
    def contractor_proposal_create(self, contract_id, amount=None, **post):
        self._contractor(); contract = self._record('contract.contract', contract_id)
        try: amount = float(amount)
        except (TypeError, ValueError) as exc: raise Forbidden() from exc
        proposal = request.env['contract.proposal'].create({'contract_id': contract.id, 'amount': amount})
        return request.redirect(f'/my/contractor/proposals/{proposal.id}')

    @http.route('/my/contractor/proposals', type='http', auth='user', website=True)
    def contractor_proposals(self):
        self._contractor()
        return self._render('project_contractor.portal_contractor_proposals', proposals=request.env['contract.proposal'].search([]), page_name='contractor_proposals')

    @http.route('/my/contractor/proposals/<int:proposal_id>', type='http', auth='user', website=True)
    def contractor_proposal(self, proposal_id):
        self._contractor(); proposal = self._record('contract.proposal', proposal_id)
        return self._proposal_page(proposal, False, f'/my/contractor/proposals/{proposal.id}')

    @http.route('/my/contractor/proposals/<int:proposal_id>/<string:action>', type='http', auth='user', website=True, methods=['POST'])
    def contractor_proposal_action(self, proposal_id, action, amount=None, **post):
        self._contractor(); proposal = self._record('contract.proposal', proposal_id)
        if action == 'submit': proposal.action_submit()
        elif action == 'withdraw': proposal.action_withdraw()
        elif action == 'update' and proposal.state == 'draft':
            try: proposal.write({'amount': float(amount)})
            except (TypeError, ValueError) as exc: raise Forbidden() from exc
        else: raise NotFound()
        return request.redirect(f'/my/contractor/proposals/{proposal.id}')

    @http.route(['/my/contractor/proposals/<int:proposal_id>/message', '/my/contracts/<int:contract_id>/proposals/<int:proposal_id>/message'], type='http', auth='user', website=True, methods=['POST'])
    def proposal_message(self, proposal_id, contract_id=None, body=None, **post):
        proposal = self._record('contract.proposal', proposal_id)
        url = f'/my/contractor/proposals/{proposal.id}'
        if contract_id:
            contract = self._customer_contract(contract_id)
            if proposal.contract_id != contract: raise NotFound()
            url = f'/my/contracts/{contract.id}/proposals/{proposal.id}'
        if not (body or '').strip(): raise Forbidden()
        proposal.message_post(body=body.strip(), message_type='comment', subtype_xmlid='mail.mt_comment')
        return request.redirect(url)

    @http.route('/my/contractor/projects', type='http', auth='user', website=True)
    def contractor_projects(self):
        self._contractor()
        return self._render('project_contractor.portal_contractor_projects', projects=request.env['project.project'].search([]), page_name='contractor_projects')

    @http.route('/my/contractor/projects/<int:project_id>', type='http', auth='user', website=True)
    def contractor_project(self, project_id):
        self._contractor(); project = self._record('project.project', project_id)
        return self._project_page(project, False, f'/my/contractor/projects/{project.id}')

    @http.route(['/my/contractor/projects/<int:project_id>/message', '/my/contracts/<int:contract_id>/projects/<int:project_id>/message'], type='http', auth='user', website=True, methods=['POST'])
    def project_message(self, project_id, contract_id=None, body=None, **post):
        project = self._record('project.project', project_id)
        url = f'/my/contractor/projects/{project.id}'
        if contract_id:
            contract = self._customer_contract(contract_id)
            if project.contract_id != contract: raise NotFound()
            url = f'/my/contracts/{contract.id}/projects/{project.id}'
        if not (body or '').strip(): raise Forbidden()
        project.message_post(body=body.strip(), message_type='comment', subtype_xmlid='mail.mt_comment')
        return request.redirect(url)

    def _proposal_page(self, proposal, customer, url):
        messages = request.env['mail.message'].search([('model', '=', 'contract.proposal'), ('res_id', '=', proposal.id)])
        return self._render('project_contractor.portal_proposal', proposal=proposal, messages=messages, customer=customer, post_url=f'{url}/message', page_name='proposal')

    def _project_page(self, project, customer, url):
        messages = request.env['mail.message'].search([('model', '=', 'project.project'), ('res_id', '=', project.id)])
        tasks = request.env['project.task'].search([('project_id', '=', project.id)]) if not customer else request.env['project.task']
        return self._render('project_contractor.portal_project', project=project, messages=messages, tasks=tasks, customer=customer, post_url=f'{url}/message', page_name='project')
