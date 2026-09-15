{
    "name": "Project Contractors",
    "version": "19.0.1.0.0",
    "category": "Services/Project",
    "summary": "Assign external contractors to project tasks without making them Odoo users",
    "description": """
Project Contractors
===================

Extends standard Contacts and Project so external contractors (people or
companies who perform project work) can be classified and associated with
projects and tasks without becoming Odoo users.

* Mark contacts (persons or companies) as contractors.
* Set the external contractor performing a task, separately from its
  internal assignees and its customer.
* See the contractors participating in a project, derived from its tasks.
* Open a contractor's current work, completed work and projects.

This addon is about contractors performing project work. It is not about
legal contracts, subscriptions, or employment contracts.
    """,
    "author": "Ricardo Zermeño",
    "website": "https://github.com/RAZermenoSaracho/odoo_project_contractor",
    "license": "LGPL-3",
    "depends": ["project"],
    "data": [
        "views/res_partner_views.xml",
        "views/project_task_views.xml",
        "views/project_project_views.xml",
    ],
    "installable": True,
    "application": False,
}
