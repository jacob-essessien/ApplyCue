# Research Library: Inbox-to-Action Job Tracker

Curated on 6 September 2026 for the two-week Django build. This is a learning/reference library, not a list of code to copy. Read the architecture and tests of open-source projects, then implement the scoped design in this repository yourself.

## Use this in order

1. Learn enough Django to complete the **manual planning tracker**.
2. Learn secure Gmail web-server OAuth—not a command-line OAuth shortcut.
3. Implement imports, deduplication and deterministic classification.
4. Read similar projects/products for ideas, then explicitly select only one or two ideas to build.
5. Use community posts for problems and trade-offs, but prefer official documentation for security/API decisions.

---

## A. Essential build resources

| Priority | Resource | Use it for | When |
|---|---|---|---|
| Must | [Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/) | Project setup, models, views, templates and admin | Days 1–4 |
| Must | [Django model documentation](https://docs.djangoproject.com/en/stable/topics/db/models/) | Foreign keys, indexes, model constraints and migrations | Day 2 |
| Must | [Django forms](https://docs.djangoproject.com/en/stable/topics/forms/) | Safe create/edit/task forms and validation | Days 3–4 |
| Must | [Django testing overview](https://docs.djangoproject.com/en/stable/topics/testing/overview/) | Model, view, service and security tests | Days 6, 10, 13 |
| Must | [Django deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/) | Production `DEBUG`, cookies, HTTPS, secrets and database checks | Days 7, 13 |
| Must | [Gmail API: server-side authorization](https://developers.google.com/workspace/gmail/api/auth/web-server) | The correct OAuth pattern for a web application | Day 8 |
| Must | [Gmail API Python quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python) | Client library setup and basic API calls | Day 8; do not copy its local token-file design into production |
| Must | [Gmail search and filtering](https://developers.google.com/workspace/gmail/api/guides/filtering) | Bounded job-email queries and historical import | Day 9 |
| Must | [OWASP OAuth 2.0 cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html) | `state`, PKCE, scopes and token threats | Day 8 |
| Must | [OWASP session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | Secure HttpOnly session cookies; why not to store tokens in `localStorage` | Day 13 |
| Must | [OWASP secrets management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | `.env`, host secret storage and secret rotation | Days 1, 13 |
| Useful | [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html) | Data modelling and querying fundamentals | Day 2 |
| Useful | [WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/) | Form labels, focus states, contrast and keyboard checks | Days 6, 13 |
| Later | [Gmail push notifications](https://developers.google.com/workspace/gmail/api/guides/push) | Event-based resync after MVP; Gmail watch renewal and fallbacks | Post-launch |
| Later | [Celery documentation](https://docs.celeryq.dev/en/stable/) | Queued/scheduled imports after a user-triggered import works | Post-launch |
| Later | [Microsoft Graph Python tutorial](https://learn.microsoft.com/en-us/graph/tutorials/python) | Outlook connector | Post-launch |

### Recommended learning video

- [Django Crash Course — freeCodeCamp](https://www.youtube.com/watch?v=0roB7wZMLqI): a current beginner-to-first-project walkthrough covering the Django request/model/template/admin fundamentals. Watch selectively: setup, apps, models, forms, templates and project sections. Pause often and type the equivalent in your own project.

Avoid investing time in generic “build a full SaaS in 20 minutes” videos. They tend to flatten security, data modelling and testing—the parts that make this portfolio project compelling.

---

## B. Open-source project references

These are valuable because they solve some of the same problems. They use different stacks and scopes, so use them for comparison, not as a blueprint.

| Repository | Why it is useful | Study specifically | Do not import wholesale |
|---|---|---|---|
| [JustAJobApp / jobseeker-analytics](https://github.com/JustAJobApp/jobseeker-analytics) | The closest substantial open-source product reference: Gmail inbox → dashboard; includes backend, frontend, deployment and a security document. | README, `SECURITY.md`, deployment, privacy decisions and how a real project separates layers. | Its full-stack/container complexity; it is far beyond two weeks. |
| [Devashish-Pisal / job-application-tracker](https://github.com/Devashish-Pisal/job-application-tracker) | Small Python pipeline using Gmail, Sheets, OAuth, Gemini, tests and separate backfill/sync modes. | Search query design, distinction between historical backfill and later sync, fixture/tests and duplicate concerns. | Desktop `token.json` handling; use server-side encrypted token storage in the web app. |
| [Pranav-here / job-email-tracker](https://github.com/Pranav-here/job-email-tracker) | Gmail → structured application data; uses an LLM and filtering layers. | Input/output schema ideas; filtering newsletters vs real recruiting mail; category progression. | Automatic updates with no review gate; your MVP should propose then ask the user. |
| [habinrahman / AI-Job-Application-Tracker](https://github.com/habinrahman/AI-Job-Application-Tracker) | A well-scoped Gmail read-only tracker with heuristics, PostgreSQL and background sync—implemented in Phoenix/LiveView. | Product choices: searchable pipeline, incremental syncing, heuristics before AI. | The Elixir framework; learn its product architecture, not its syntax. |
| [coolbrother / apply-potato](https://github.com/coolbrother/apply-potato) | Self-hosted automation combining job discovery, eligibility filters, Gmail status tracking and Sheets. | Rich graduate-stage status set and multi-account / idempotency considerations. | Scraping, Discord, job discovery and multi-account support—explicitly out of MVP scope. |
| [AkhilDhawan22 / job-track-os](https://github.com/AkhilDhawan22/job-track-os) | Gmail/Google Sheets-oriented automation with messaging extras. | Its `.env.example` and external integration boundary. | Node stack and Slack/WhatsApp features. |

### How to study a repository efficiently

1. Read its README and diagram first.
2. Locate its data model/schema, tests and environment sample—these teach more than the homepage.
3. Write down one idea to adapt and one decision to reject.
4. Never add a dependency only because another project uses it; state the need it satisfies in your decision log.

---

## C. Community/forums: useful lessons and reality checks

These are opinion/experience sources, not authority for security or provider behaviour.

| Thread | Value | Practical lesson for this project |
|---|---|---|
| [Django Forum: receive emails in Django](https://forum.djangoproject.com/t/receive-emails-in-django/36983) | Explores Gmail API versus mailbox-receiving approaches. | Use the Gmail API for the Gmail connector. Consider a forwarding-address strategy later for broad provider support. |
| [Django Forum: Google OAuth + Gmail API](https://forum.djangoproject.com/t/sending-email-using-django-allauth-google-gmail-api-and-oauth-post-less-secure-apps/38113) | Useful symptoms and package/OAuth discussion. | Provider OAuth evolves; avoid old out-of-band flow tutorials and check official docs first. |
| [Reddit: application tracker that pulls from Gmail](https://www.reddit.com/r/GoogleAppsScript/comments/1kerdv1/job_application_tracker_that_automatically_pulls/) | A maker describes an email-to-Google-Sheets tracker and limitations in extracting company/title/status. | Extraction is imperfect: build manual correction and “needs review” from day one. |
| [Reddit: automated job tracker / jobWrangler](https://www.reddit.com/r/webdev/comments/1brf9bc) | Builder discussion of Gmail classification, task tracking and dashboard insights. | The sensible progression is tracker → task/follow-up planning → analytics, not everything at once. |
| [Reddit: inconsistent email keywords](https://www.reddit.com/r/codingplus/comments/1iewic6) | A concrete account of the keyword-matching problem. | Make rules configurable, collect false positives/negatives as fixtures, and use confidence + review. |
| [Django project-structure discussion](https://www.reddit.com/r/django/comments/1prgz0j/confused_about_django_project_structure/) | Current practitioner discussion on traditional Django vs service/repository layers. | Keep the modular Django structure pragmatic; do not add repositories/DTOs/CQRS to prove sophistication. |

### Communities worth following during the build

- [Django Forum](https://forum.djangoproject.com/) — framework/OAuth/deployment questions; post a minimal reproducible example, never credentials.
- [r/django](https://www.reddit.com/r/django/) — project structure, testing and deployment discussion; treat answers as opinions to evaluate.
- [r/learnpython](https://www.reddit.com/r/learnpython/) — beginner Python debugging and conceptual help.
- [Stack Overflow: django](https://stackoverflow.com/questions/tagged/django) — use for specific error messages after checking official docs.

Never paste real emails, OAuth callback URLs containing codes, access tokens, refresh tokens, `.env` contents, or production database records into a public post.

---

## D. Existing products to inspect for inspiration

Product pages are self-reported marketing sources. Use them to study user experience, positioning and feature choices—not to assume their claims are independently verified.

| Product | What it currently offers | Inspiration to take | Opportunity/difference for your project |
|---|---|---|---|
| [Trakd](https://www.trakd.co/) | Gmail/Outlook inbox tracking, Chrome autofill, task creation and company/role-specific interview questions for students/new grads. | “Next action” visibility and graduate-specific recruitment stages. | Your MVP can make every automation explainable/reviewable and focus on a clean planning timeline before a prep-question database. |
| [JobOps](https://jobops.io/) | Gmail, IMAP or forwarding intake; living application timeline, dashboard, pipeline, calendar and analytics. | Choice of privacy model: OAuth, IMAP or forwarding; clear dashboard/pipeline/calendar view split. | Start Gmail-only, then consider forwarding as a safer universal-provider differentiator—not IMAP in two weeks. |
| [JobFlow](https://jobflow-ai.com/) | Inbox-built pipeline for Gmail/Outlook/IMAP, interview datetime extraction, quiet/ghosted applications and a “Today” briefing; claims encrypted tokens and one-click disconnect. | Strong “what should I do today?” framing, follow-up detection, explicit privacy language. | Your differentiator should be the planning workspace, evidence/rationale and manual review rather than only automation. |
| [Prowl](https://prowljobtracker.app/) / [App Store listing](https://apps.apple.com/us/app/prowl-job-application-tracker/id6760794893) | Mobile tracker with Gmail/Outlook sync, manual tracking, timeline, status/ghost warnings and application statistics. | A simple, approachable timeline and manual fallback. | Web-first design, graduate stages and planner-oriented dashboard provide a different portfolio/product direction. |
| [Careeroc](https://www.careeroc.com/) | Gmail job-email tracker with a visible review gate and application detail workflow. | Review-gate UX is a useful direct reference for your human-in-the-loop design. | Be clearer about rationale/confidence and minimal data retention. |
| [Simplify](https://help.simplify.jobs/articles/0236686-email-integration) | Gmail recruiting-email synchronisation within an established job search platform. | Integrating tracking into a wider workflow rather than treating it as an isolated spreadsheet replacement. | Do not try to match its entire ecosystem; solve planning and inbox clarity exceptionally well. |
| [Jobless Smart Inbox](https://jobless.dev/smart-inbox) | Gmail/Outlook connection; automatic email updates as an optional premium/AI feature. | Progressive enhancement: a useful tracker before inbox automation. | This reinforces the chosen manual-first MVP sequencing. |

### UI research exercise (60–90 minutes)

For Trakd, JobOps and JobFlow, use their public product pages and write a comparison in `docs/decision-log.md`:

1. What is their first screen/promise?
2. Which three statuses do they make most visible?
3. How do they explain inbox access and privacy?
4. How would a user correct a wrong classification?
5. Which **one** interaction should your Dashboard borrow in principle (not copy visually)?

The expected conclusion: build a calm, action-first dashboard, an application timeline and an evidence-backed review queue. Avoid a generic feature-packed kanban clone.

---

## E. Practical research tasks by build day

| Day | Read/watch | Output to add to your repository |
|---|---|---|
| 1 | Django tutorial + freeCodeCamp setup/models segment | `README.md` problem, scope and local setup |
| 2 | Django models + PostgreSQL tutorial | `docs/data-model.md` or a diagram; first migration |
| 3–4 | Django forms/templates | First manual create/edit/detail flow |
| 5–6 | Trakd/JobOps/JobFlow UI exercise + Django tests | Wireframe decisions and dashboard tests |
| 7 | Django deployment checklist | Deployment checklist with evidence |
| 8 | Gmail server OAuth + OWASP OAuth | OAuth sequence diagram and required scopes table |
| 9 | Gmail filtering docs + Devashish project | A bounded query plan and idempotency test |
| 10–11 | Pranav/habinrahman repos + Reddit keyword thread | At least 12 synthetic email fixtures with expected classification |
| 12 | LLM structured-output documentation from your chosen provider | Prompt/schema/evaluation note; feature flag default off |
| 13–14 | OWASP session/secrets + product privacy sections | `docs/security.md`, demo script and limitations |

---

## F. Resource decisions: what not to do yet

- Do not build direct Yahoo/IMAP access based on an unverified tutorial; it expands credential/security/support responsibilities.
- Do not use browser `localStorage` for Gmail or user-session credentials.
- Do not add an LLM orchestration framework only to make the project sound AI-based. A small provider client plus schema validation is easier to learn and test.
- Do not clone a competitor UI, scrape job boards, add browser autofill, write calendar events or send follow-up emails in this release.
- Do not rely on copied production OAuth configuration. Create your own Google Cloud test project and registered redirect URLs.

## G. Best five references if time is limited

1. [Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
2. [Gmail server-side OAuth](https://developers.google.com/workspace/gmail/api/auth/web-server)
3. [OWASP OAuth cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html)
4. [JustAJobApp open-source repository](https://github.com/JustAJobApp/jobseeker-analytics)
5. [JobFlow product site](https://jobflow-ai.com/)

These cover framework fundamentals, the hardest integration, security, a real implementation reference and product/UX inspiration.
