## 1. Django Project Foundation

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