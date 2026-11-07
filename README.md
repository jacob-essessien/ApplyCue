# ApplyCue

A graduate job-search planner intended to turn recruitment emails into reviewable application updates, deadlines, and next actions.

## Current state

The repository contains project documentation and a local Python/Django development environment. Application features and the Django project scaffold have not been implemented yet.

- Python: 3.14 (setup verified with 3.14.1)
- Django: 5.2 LTS, exact dependencies recorded in `Pipfile.lock`
- Environment and dependency management: Pipenv
- Development method: collaborative, module by module; see [AGENTS.md](AGENTS.md)

The [current project brief](APPLYCUE_PROJECT_BRIEF.md) takes precedence over conflicting choices in the older [project plan](PROJECT_PLAN.md). The [research library](RESOURCE_RESEARCH.md) contains references to evaluate as modules are developed.

## Windows setup

Run these commands in PowerShell inside the cloned ApplyCue repository. Use a Python 3.14 installation; a separate Python installation is not needed when that version is already available.

```powershell
py -3.14 -m pip install --user pipenv
$env:PIPENV_VENV_IN_PROJECT = "1"
py -3.14 -m pipenv sync
py -3.14 -m pipenv run python --version
py -3.14 -m pipenv run python -m django --version
```

`pipenv sync` installs the versions already recorded in the lockfile. `pipenv run` runs a command inside the project's isolated environment without requiring shell activation. Using `py -3.14 -m pipenv` also works when the `pipenv` shortcut is not on PATH.

Open this repository folder in VS Code. Its Python interpreter setting points to `.venv/Scripts/python.exe`. The `.venv` folder stays local and is excluded from Git.

There is no `manage.py` or development server yet. Creating the starter Django project is the next module.

## Development notes

See [the development log](docs/DEVELOPMENT.md) for the setup decisions, folder map, verification commands, and first Git exercise.
