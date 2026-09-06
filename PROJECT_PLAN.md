# Inbox-to-Action Job Tracker — Two-Week Delivery Plan

## 1. Outcome and scope

**Goal:** ship a deployed, portfolio-ready web application in 14 days. It helps an early-career job seeker manually plan each application and optionally imports relevant Gmail messages to create explainable status updates.

**Product promise:** *Your inbox records what happened; your tracker tells you what to do next.*

### Definition of done (end of day 14)

A new user can:

1. Create, edit, archive and search applications.
2. Add a time-ordered event, task, deadline or note to an application.
3. See a dashboard of overdue and upcoming actions.
4. Connect **one Gmail test account** with read-only OAuth access, run an import, and review detected job-email updates before applying them.
5. See why an imported email was classified and reverse the proposed update.
6. Use the deployed app over HTTPS, with a concise README, seed/demo data, tests, screenshots and a short demo video.

### Deliberate non-goals

- Outlook, Yahoo, IMAP, mobile apps, calendar write-access, notifications, CV generation and payment.
- Fully automatic status changes: every imported update is reviewed in this version.
- Training a custom ML model. Use deterministic rules first; use an LLM only for uncertain messages.
- Building a React SPA. Server-rendered Django pages are faster to complete and demonstrate full-stack fundamentals.

### Scope guard

If time becomes tight, preserve manual planning and dashboard functionality. Make Gmail import a review-only demo flow or use pre-loaded sample emails. Do **not** trade the finished core product for more integrations.

---

## 2. Technical decisions

| Concern | Choice | Reason |
|---|---|---|
| Web framework | Python 3.12, Django 5.x, Django templates | Batteries included: ORM, sessions, auth, forms, admin and CSRF protection. |
| Styling | Tailwind CSS or clean custom CSS | Build a responsive, professional dashboard without a separate frontend app. |
| Database | PostgreSQL in production; PostgreSQL locally if possible | Relationships and transaction safety fit this domain. |
| Background work | Django management command first; Celery + Redis only if time remains | A user-triggered import is enough for the MVP. Avoid queue infrastructure until it solves a real need. |
| Authentication | Django accounts; email/password for demo | Keeps app authentication independent from mail-provider consent. |
| Gmail | Google OAuth 2.0, `gmail.readonly` scope | Least privilege: read data, never send/delete/change mail. |
| Classification | Keyword/regex rules, then optional structured LLM fallback | Learns fundamentals; keeps decisions explainable and predictable. |
| Hosting | Render/Railway/Fly.io + managed PostgreSQL | HTTPS and deployment without operating servers. |
| Observability | Structured application logging plus Sentry optional | Debug import failures without logging email bodies. |

### Core apps/modules

```text
config/             Django settings, routes, environment configuration
accounts/           registration, login, account deletion
applications/       applications, events, tasks, dashboard, exports
mailbox/             OAuth callback, Gmail API client, import/audit pipeline
templates/          shared layout and page templates
static/              CSS, icons, small JavaScript enhancements
```

---

## 3. System and architectural design

```text
Browser
  └─ HTTPS ─► Django application
                 ├─ server-rendered UI / session authentication
                 ├─ Application service (create, plan, search)
                 ├─ Mailbox service (OAuth, fetch, normalize)
                 ├─ Classification service (rules → optional LLM)
                 └─ Audit/review service
                         │
                         ├─ PostgreSQL
                         │    users, applications, tasks, events,
                         │    imported-message metadata, encrypted tokens
                         └─ Gmail API (read-only, only after user consent)
```

### Key flows

#### A. Manual planning

1. User creates an application with company, role and current stage.
2. They add a deadline, interview or next action as an `ApplicationEvent` or `Task`.
3. Dashboard queries tasks due today/next seven days and events in the future.
4. Application detail page is the source of truth for the event timeline.

#### B. Gmail import and review

1. User chooses **Connect Gmail**; Django starts OAuth Authorization Code flow with a `state` value and PKCE where supported.
2. Google returns to a strict, registered callback URL. The server validates `state`, exchanges the code, encrypts the refresh token, and stores no Gmail password.
3. User selects **Scan job emails**. The server fetches only a bounded, search-filtered sample (e.g. last 90 days / max 100 results).
4. Normalize sender, subject, date, Gmail message ID and plain-text body. Keep the full body only temporarily while classifying; delete it after the review record is built.
5. Rules classify the message and extract candidate company/role/deadline. Low-confidence messages can optionally go to an LLM with only the minimal text excerpt needed.
6. Deduplicate by `(mailbox_connection, provider_message_id)`.
7. Create a `ProposedUpdate`, never mutate an application automatically.
8. User accepts, edits or rejects it. Acceptance creates the application/event/task in one database transaction and records an audit entry.

### Mail classification rules for the first build

| Category | Initial signals | Proposed action |
|---|---|---|
| Application received | `thank you for applying`, `application received`, `we received` | Create/update as **Applied** |
| Assessment | `online assessment`, `coding test`, `complete by`, `psychometric` | Add Assessment event and deadline task |
| Interview | `interview`, `schedule a call`, `assessment centre` | Add Interview event; extract date if clear |
| Offer | `offer of employment`, `pleased to offer` | Propose **Offer** |
| Rejection | `unfortunately`, `not moving forward`, `decided not to proceed` | Propose **Rejected** |
| Unknown | none/contradictory | Keep in Review; do nothing automatically |

Every proposal displays the matching phrase or a short rationale. This is both a trust feature and evidence of responsible AI engineering.

---

## 4. Database design

Use Django migrations. Every record that belongs to a user must be filtered by the authenticated owner in the service/query layer.

```text
User
 ├── Application (1..*)
 │     ├── ApplicationEvent (0..*)
 │     ├── Task (0..*)
 │     ├── Note (0..*)
 │     └── StatusChangeAudit (0..*)
 └── MailboxConnection (0..*)
       └── ImportedMessage (0..*)
             └── ProposedUpdate (0..*) ──► Application? (optional)
```

### Model specification

| Model | Essential fields | Constraints/indexes |
|---|---|---|
| `User` | Django user; `created_at` | Start with Django’s default user; migrate to custom user only if needed before first migration. |
| `Application` | `user`, `company_name`, `role_title`, `status`, `applied_on`, `source`, `url`, `last_activity_at`, timestamps | Index `(user, status)`, `(user, last_activity_at)`; company/role required. |
| `ApplicationEvent` | `application`, `type`, `occurred_at`, `title`, `details`, `source` (`manual`/`email`), `source_message` nullable | Index `(application, occurred_at)`; no arbitrary user ID—ownership comes through application. |
| `Task` | `application`, `title`, `due_at`, `completed_at`, `priority`, `created_from_event` nullable | Index on `due_at`, `completed_at`; no duplicate active task from the same event. |
| `Note` | `application`, `body`, timestamps | Simple, owner via application. |
| `MailboxConnection` | `user`, `provider`, `provider_account_email`, `encrypted_refresh_token`, `scopes`, `revoked_at`, timestamps | Unique `(user, provider, provider_account_email)`. Never store provider password. |
| `ImportedMessage` | `connection`, `provider_message_id`, `thread_id`, `sender_domain`, `subject`, `received_at`, `classification`, `confidence`, `body_excerpt`, `body_retention_expires_at`, `processed_at` | Unique `(connection, provider_message_id)` for idempotency. Avoid full raw-message storage. |
| `ProposedUpdate` | `imported_message`, `application` nullable, `proposal_type`, `payload` JSON, `rationale`, `state`, `reviewed_at` | Unique `(imported_message, proposal_type)`; state: pending/accepted/edited/rejected. |
| `StatusChangeAudit` | `application`, `actor_user` nullable, `before_status`, `after_status`, `reason`, `source_message` nullable, timestamp | Append-only in application code. |

### Status and event enums

```text
Application status: DRAFT, APPLIED, ASSESSMENT, INTERVIEW, OFFER,
REJECTED, WITHDRAWN, CLOSED

Event type: APPLICATION_SUBMITTED, CONFIRMATION, ASSESSMENT,
INTERVIEW, FOLLOW_UP, OFFER, REJECTION, NOTE
```

### Important data rules

- `Application.user` is immutable after creation.
- Application status may change only through one service function that writes `StatusChangeAudit`.
- Imported messages are immutable after processing except retention/deletion fields.
- A proposed update never writes production data until user acceptance.
- Store timestamps in UTC; render them in the user’s local browser timezone later.
- Use Django’s ORM, parameterized queries and migrations—never concatenate SQL.

---

## 5. Security and privacy design

This product processes highly sensitive inbox data. Treat security as a feature, not final polish.

### Required controls for this release

| Threat/control area | Measure |
|---|---|
| Least privilege | Request only Gmail `gmail.readonly`; do not ask for send/modify/delete scopes. |
| OAuth attacks | Authorization Code flow, `state` validation, registered HTTPS redirect URL, PKCE where applicable; validate token audience/issuer through provider libraries. |
| Token storage | Encrypt refresh tokens at rest using a deployment-provided encryption key; never put credentials/tokens in source control, logs, browser storage or error reports. |
| Web sessions | Django server-side sessions; secure, HttpOnly, SameSite cookies; force HTTPS in production. Never use localStorage for credentials. |
| Access control | Every view/service starts with the current user and queries only their objects; write tests for cross-user access returning 404/403. |
| CSRF/XSS | Keep Django CSRF middleware on; use `{% csrf_token %}` for every form; rely on Django template escaping; do not mark email/LLM content as safe HTML. |
| Input validation | Django forms/model validation; server-side enum/date validation; constrain lengths; validate URLs. |
| Email content minimisation | Store sender/domain, subject, dates, classification and a small redacted excerpt. Do not retain whole email bodies unless the user explicitly opts in. |
| Secrets | `.env` only locally, host secret manager in production; commit `.env.example` with placeholders; rotate any exposed token immediately. |
| Logging | Log IDs and error categories, never body content, OAuth codes, access tokens, refresh tokens or `Authorization` headers. |
| Account/data deletion | Add a Disconnect Gmail action that revokes/deletes stored tokens and imported message metadata. Add an account deletion route for the final demo if possible. |
| Dependency/deployment safety | Pin dependencies, run `python manage.py check --deploy`, disable `DEBUG`, set allowed hosts, configure secure headers and automated DB backups. |

### Security acceptance tests

- Unauthenticated users cannot access application, task, import or admin endpoints.
- User A cannot request User B’s application by guessed URL.
- OAuth callback with an invalid/missing `state` is rejected.
- Browser HTML shows email subject/body as escaped text, never executable HTML.
- A second import of the same Gmail message creates no second proposal.
- `.env`, `credentials.json`, token files and the database are ignored by Git.
- `check --deploy` returns no critical issues before launch.

### Two-week security boundary

This is safe for a portfolio demo and personal/test users when deployed correctly; it is not yet a compliance-complete consumer SaaS. Public rollout requires a privacy policy, terms, deletion/retention process, incident plan, monitoring, provider verification review and a threat-model refresh.

---

## 6. UI/UX design and page plan

### Design principles

- **Action over data entry:** show the next useful step, not just a large table.
- **Inbox evidence:** every automated proposal links to concise source metadata and rationale.
- **Calm and scannable:** user may be managing rejections and deadlines; keep status colour secondary to plain text.
- **Keyboard and mobile competent:** all core workflows work on a narrow screen and with forms/buttons labelled clearly.

### Information architecture

```text
Dashboard
Applications ─ list / filters / create
  └─ Application detail ─ overview / timeline / tasks / notes
Inbox review ─ pending proposals / accepted/rejected history
Settings ─ profile / Gmail connection / data controls
```

### Page-level specification

| Page | Primary content | Main actions |
|---|---|---|
| Dashboard | Today, overdue tasks, next 7 days, recent application activity, status counts | Complete task, open application, add application |
| Applications | Search, filters (status/source), accessible table on desktop and cards on mobile | Create, filter, open, archive |
| Create/edit application | Company, role, stage, date applied, source, job URL, next task | Save and create another; add next action |
| Application detail | Header/status; next action; chronological event timeline; tasks; notes | Change status, add event/task/note, mark task done |
| Inbox review | One proposal card at a time: type, confidence, extracted details, quoted matching phrase, linked target application | Accept, edit then accept, reject |
| Settings | Gmail connect/disconnect, scopes explanation, data-retention note | Connect, scan, disconnect/delete |

### Wireframe: dashboard

```text
┌───────────────────────────────────────────────────────────┐
│ JobTrack     Dashboard  Applications  Inbox Review   + Add │
├───────────────────────────────────────────────────────────┤
│ Good morning, Alex                                         │
│ 3 actions need attention                                   │
│                                                           │
│ OVERDUE                 NEXT 7 DAYS                        │
│ [Follow up: Acme]     [Coding test: 18 Sep]                │
│ [Submit Deloitte]     [Interview prep: 20 Sep]             │
│                                                           │
│ RECENT ACTIVITY                                             │
│ Amazon — Online assessment proposed from Gmail  [Review]   │
│ Barclays — Interview scheduled                  [Open]     │
│                                                           │
│ [Applied 12] [Assessment 3] [Interview 2] [Offer 1]        │
└───────────────────────────────────────────────────────────┘
```

### UI build order

1. App shell/navigation and typography/colour tokens.
2. Application list and create/edit form.
3. Detail timeline and tasks.
4. Dashboard queries/cards.
5. Inbox review cards.
6. Responsive fixes, empty states, error states and accessibility pass.

---

## 7. Fourteen-day schedule

Assumption: about 4 focused hours per weekday and 6–8 hours per weekend day. Commit working code at least once per day. End every day by writing a short decision log: what changed, why, what is next.

| Day | Build target | Manual learning objective | End-of-day evidence |
|---|---|---|---|
| 1 | Write `README` product brief, set up Git repo, Python environment, Django project, PostgreSQL, `.env.example` | Django project anatomy, migrations, Git workflow | App runs locally; first commit; 3 wireframes |
| 2 | Define models/enums, create and apply migrations; use Django admin to inspect data | Relational modelling, foreign keys, migrations | Admin can create application/event/task records |
| 3 | Build application list, create and edit forms; add login/logout | Forms, validation, ownership queries | User creates only their own applications |
| 4 | Build application-detail page, timeline, task completion and notes | Service-layer thinking and transactions | One application has a functioning action timeline |
| 5 | Build dashboard: overdue/upcoming/recent/status counts | ORM aggregation/query optimisation basics | Dashboard reflects live test data |
| 6 | Polish manual MVP: filtering, search, empty states, responsive styles; write tests | Test-driven bug fixing, accessibility basics | Manual product complete; 10–15 targeted tests |
| 7 | Deploy manual product; set production env vars and HTTPS; run deploy check | Deployment configuration and secret hygiene | Public HTTPS demo URL; `check --deploy` clean |
| 8 | Set up Google Cloud test OAuth consent screen/client; implement Connect Gmail callback and encrypted token store | OAuth flow, state/CSRF, scopes | Your test Gmail account connects/disconnects securely |
| 9 | Implement bounded Gmail message fetch, normalisation and idempotent imported-message storage | API clients, pagination, error handling | A scan stores metadata from known test messages |
| 10 | Write deterministic classifier/extractors and unit tests using saved, redacted fixtures | Regex/text parsing, confidence scoring | Expected fixture messages classify correctly |
| 11 | Build proposed-update creation, matching existing applications and Inbox Review UI | Human-in-the-loop workflow, audit trails | Accept/edit/reject proposal works end to end |
| 12 | Optional LLM fallback behind a feature flag; redact/minimise prompt; record rationale and confidence | Structured output, evaluation and cost/privacy thinking | 10-message comparison: rules vs LLM documented |
| 13 | Security and quality pass: authorization tests, input/error states, mobile view, logs, deletion/disconnect | Threat modelling, test coverage, UX QA | Security checklist signed off; no secrets in Git |
| 14 | Seed demo data, write architecture/security docs, record 2–3 min walkthrough, final deploy and retrospective | Technical communication and portfolio presentation | Finished README, demo link/video, screenshots, tagged release |

### Required daily cadence

1. **20 min:** read the designated resource and set a narrow task.
2. **2.5–5 hours:** build it manually; use AI to explain/review only when blocked.
3. **20 min:** test the happy path and one failure case.
4. **10 min:** commit with a clear message and update the decision log.

---

## 8. AI use and learning rules

Use AI as a tutor, code reviewer and classifier—not as an invisible code generator.

### Permitted high-value uses

- Ask for a concept explanation, then implement it from the official docs.
- Ask for a test plan or security review after completing a feature.
- Ask it to diagnose a specific stack trace, with the relevant code supplied.
- Use an LLM only in `classify_with_llm()` for messages rules cannot classify, returning a constrained JSON schema.
- Keep redacted test fixtures and measure accuracy manually before trusting a classifier.

### Manual work you should own

- Data model and migrations.
- Ownership/permission checks.
- Django forms and templates.
- Gmail OAuth configuration and token lifecycle.
- Classification rules and their test cases.
- Deployment and environment configuration.
- README, architecture diagram, decisions and demo narration.

### LLM fallback contract

```json
{
  "category": "application_received | assessment | interview | offer | rejection | unknown",
  "company_name": "string or null",
  "role_title": "string or null",
  "deadline_iso": "ISO-8601 datetime or null",
  "confidence": 0.0,
  "rationale": "short explanation based on the supplied text"
}
```

Treat output as untrusted input: validate category, date and field lengths server-side. Low-confidence output remains pending review.

---

## 9. Resource checklist

Read in the order the days call for them. Prefer these primary sources over copying tutorials.

### Django and PostgreSQL

- [Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/) — Days 1–3.
- [Django model documentation](https://docs.djangoproject.com/en/stable/topics/db/models/) — Day 2.
- [Django forms](https://docs.djangoproject.com/en/stable/topics/forms/) — Day 3.
- [Django testing overview](https://docs.djangoproject.com/en/stable/topics/testing/overview/) — Days 6, 10 and 13.
- [Django deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/) — Days 7 and 13.
- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html) — Day 2 reference.

### Gmail and OAuth

- [Gmail Python quickstart](https://developers.google.com/workspace/gmail/api/quickstart/python) — Day 8 setup only; adapt it to web-server OAuth rather than copying its local token-file approach.
- [Gmail message search/filtering](https://developers.google.com/workspace/gmail/api/guides/filtering) — Day 9.
- [Gmail push notifications](https://developers.google.com/workspace/gmail/api/guides/push) — read after this release; production sync phase.
- [OWASP OAuth 2.0 cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html) — Day 8.
- [OWASP session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) — Day 13; it explicitly advises against storing tokens in browser storage.

### Security and product quality

- [OWASP secrets management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — Days 1 and 13.
- [Web Content Accessibility Guidelines quick reference](https://www.w3.org/WAI/WCAG22/quickref/) — Day 6/13.
- [GitHub Skills: Introduction to GitHub](https://skills.github.com/) — use alongside every day’s commits if Git is new.

### Later expansion—not part of this two-week build

- [Microsoft Graph Python tutorial](https://learn.microsoft.com/en-us/graph/tutorials/python) — Outlook connector.
- [Celery documentation](https://docs.celeryq.dev/en/stable/) — queue-backed recurring scanning.
- [Gmail push notification guide](https://developers.google.com/workspace/gmail/api/guides/push) and Microsoft Graph change notifications — near-real-time sync.

---

## 10. Testing plan

### Minimum automated tests

- Model: status transition audit created; duplicate imported Gmail message rejected.
- Views: authentication required; User A cannot read/update User B’s application.
- Forms: invalid dates/statuses/overlong fields show errors.
- Service: classifier fixtures cover all six categories and unknown.
- Service: accepting a proposal creates the expected event/task/status and audit record atomically.
- OAuth: invalid callback `state` fails; disconnect clears encrypted token.

### Manual test script before final demo

1. Register/login as a new user.
2. Add an application and an assessment deadline; confirm it appears on Dashboard.
3. Complete the task and confirm it leaves the overdue list.
4. Connect test Gmail account, scan fixture/test emails, and see a pending proposal.
5. Edit the extracted company/role, accept it and verify the timeline/audit.
6. Re-scan; verify no duplicate proposal.
7. Disconnect Gmail; verify scan is unavailable and stored token/message data is removed.
8. Test mobile width, keyboard navigation and a failed/expired Gmail credential.

---

## 11. Portfolio package

Ship these alongside the deployed site:

- `README.md`: problem, features, stack, local setup, screenshots, live demo and limitations.
- `docs/architecture.md`: copy the architecture diagram, key flows, decisions and trade-offs.
- `docs/security.md`: threat list, safeguards, scope boundaries and data-retention policy.
- `docs/decision-log.md`: 5–10 short architecture decisions with alternatives considered.
- `fixtures/`: only synthetic/redacted emails, never real recruiter messages.
- 2–3 minute video: problem → dashboard → application plan → Gmail review → security/privacy design.

### CV-ready result

> Built and deployed a privacy-conscious job-application planning web app with Python, Django and PostgreSQL. Designed an event-based workflow and Gmail OAuth ingestion pipeline with idempotent imports, explainable rule/AI classification, manual review controls and audit logging.

---

## 12. First 90 minutes

1. Create a private GitHub repository called `inbox-to-action-tracker`.
2. Create a GitHub Project/issue board with the 14 daily deliverables above.
3. Create a Python virtual environment; install Django and PostgreSQL driver; initialise project and first app.
4. Add `.gitignore` before adding any secret/configuration files.
5. Create the `Application`, `ApplicationEvent` and `Task` models manually from the table above.
6. Run migrations, create a superuser, verify records in Django admin, and commit:

```text
chore: initialise Django tracker and core planning models
```

The first day succeeds when an application, one task and one timeline event exist in the database—not when the interface is perfect.
