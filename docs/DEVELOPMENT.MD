## 1. Django Project Foundation - 06/11/26

Purpose - establishes the config and command entry point that
later application modules will use

Created:
- mangage.py: runs project management commands
- config/settings.py: configures applications, database and templates.
- config/urls.py: defines the project's URL routing.
- config/asgi.py and config/wsgi.py: web-server entry points.
- config/__init__.py: identifies the configuration package.

Verification:
- Django's system check reported no issues.
- The local development server displayed the welcome page.
- Database migrations have not yet been applied.

## 2. Application model and admin - 07/11/26

Purpose:
Establishes persisten job application records owned by users

Implementation:
- Registered the applications app in Django settings.
- Applied Django's built-in database migrations.
- Created JobApplication with owner, company, role and created_at.
- Generated and applied the application's initial migration.
- Added a readable string representation.
- Registered the model with Django's admin.

Connections:
- owner references Django's configured user model.
- The migration creates the model's database table.
- The admin provides an interface for creating and editing records.

Verification:
- Initial application migration is applied.
- An application was created, saved and reopened through the admin.
- Saved values persisted.

Limitations:
- User-facing pages and ownership checks are not implemented.
- Recruitment status and application date are the next additions.