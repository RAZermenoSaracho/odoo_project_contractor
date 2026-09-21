from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Preserve existing awarded access without inventing legacy negotiations."""
    cr.execute("""
        SELECT column_name FROM information_schema.columns
         WHERE table_name = 'project_project'
           AND column_name IN ('primary_contractor_id', 'contractor_compensation_amount', 'contractor_compensation_currency_id')
    """)
    columns = {row[0] for row in cr.fetchall()}
    if 'primary_contractor_id' not in columns:
        return
    amount = 'contractor_compensation_amount' if 'contractor_compensation_amount' in columns else '0'
    currency = 'contractor_compensation_currency_id' if 'contractor_compensation_currency_id' in columns else 'NULL'
    cr.execute(f"""
        SELECT id, partner_id, primary_contractor_id, {amount}, {currency}
          FROM project_project
         WHERE primary_contractor_id IS NOT NULL AND contract_id IS NULL
    """)
    env = api.Environment(cr, SUPERUSER_ID, {})
    Contract = env['contract.contract']
    Proposal = env['contract.proposal']
    Project = env['project.project']
    for project_id, partner_id, contractor_id, proposal_amount, currency_id in cr.fetchall():
        project = Project.browse(project_id)
        if not project.exists() or not partner_id:
            continue
        contract = Contract.create({
            'name': project.name, 'partner_id': partner_id, 'state': 'awarded',
        })
        proposal = Proposal.create({
            'contract_id': contract.id, 'contractor_id': contractor_id, 'state': 'accepted',
            'amount': proposal_amount or 0.0, 'currency_id': currency_id or env.company.currency_id.id,
        })
        project.write({'contract_id': contract.id, 'accepted_proposal_id': proposal.id})
        proposal.write({'project_id': project.id})
        contract.write({'accepted_proposal_id': proposal.id, 'project_id': project.id})
