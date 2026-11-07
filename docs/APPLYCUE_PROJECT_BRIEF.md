# ApplyCue project summary and MVP plan

ApplyCue is a web application that helps students, graduates and early-career applicants organise their job search. It brings applications, recruitment events, deadlines and next actions into one workspace, and uses relevant emails to suggest updates that the user can review.

The first release combines a complete manual planner with a working Gmail import and review flow. Its purpose is to test whether this combination reduces administrative effort and helps applicants keep track of what they need to do next.

**Working name:** ApplyCue. **Tagline:** Know your next move. **Release target:** a deployed portfolio project and controlled beta. 


## 1 The problem and intended users

Applicants often manage several recruitment processes simultaneously. Application confirmations, online tests, interviews and decisions arrive through email, while notes and deadlines live elsewhere. A spreadsheet records applications but requires repeated manual updates and offers limited help deciding what to do next.

The initial audience is UK students and graduates applying for internships, placements and graduate roles. Their recruitment stages give the product a useful focus: assessments, video interviews, assessment centres and offer decisions. The same workflow can support other job seekers later.

The central user need is: “When I open ApplyCue, I want to know where each application stands, what I need to do next, and when it is due.”

There are two project objectives:

- **Product:** make application information and actions easy to maintain, including when email extraction is incomplete.
- **Learning:** demonstrate full-stack Python development, relational modelling, authentication, API integration, testing and deployment through code the developer can explain.

## 2 Product positioning

ApplyCue focuses on a planning workspace for each application, with visible evidence behind suggested updates. Email-derived tasks and statuses remain editable, and applications without confirmation emails can be managed manually.

This is a positioning hypothesis to validate with applicants. Inbox tracking and next-action dashboards already exist; for example, [JobFlow describes both email-based tracking and a Today briefing](https://jobflow-ai.com/). ApplyCue should compete through clear workflows, useful graduate recruitment stages and dependable corrections, rather than claiming those features are unique.

The main validation question is whether reviewing a small set of relevant proposals takes less effort than maintaining a spreadsheet. A noisy review queue would undermine the product, even if the extraction technology works.

## 3 The complete user journey

1. A user signs in and adds an application, or connects Gmail to find relevant emails.
2. ApplyCue displays the company, role, current stage, application history and outstanding tasks.
3. An imported email proposes a new application, status change, interview event or task. The proposal shows its source, extracted details and any uncertainty.
4. The user accepts, edits or rejects the proposal. An accepted change appears in the application history.
5. The dashboard brings overdue tasks, upcoming deadlines and scheduled interviews together.
6. The user completes tasks, adds preparation notes and updates progress as the recruitment process develops.

For example, an assessment invitation might propose moving an existing application to Assessment and adding “Complete numerical test” with a confirmed deadline. The user checks the matched role and date, accepts the changes, and sees the task on their dashboard. An ambiguous deadline stays unconfirmed.

## 4 MVP scope

All rows below belong to the email-assisted MVP. Gmail is optional for an individual user, but a working Gmail import is required before describing the release as the email-assisted MVP.

| Capability | Included in the first release | Completion evidence |
|---|---|---|
| Accounts | Django login/logout and private, user-owned records; provision a small set of beta accounts | Two users cannot read or change each other's records |
| Application tracking | Create, edit, search, filter and archive applications; company, role, stage, application date and job link | A user can maintain several applications, including different roles at one employer |
| Application planning | Tasks, deadlines, a notes field, manually scheduled interviews and a history of changes | Completing a task removes it from outstanding work; reopening restores it |
| Dashboard | Overdue tasks, due today, next seven days, upcoming interviews and pending reviews | Dashboard content follows the user's saved data and excludes archived applications |
| Gmail import | One Gmail connection per user; read-only OAuth; user-triggered, bounded scans | Relevant messages from a real consenting test mailbox enter review |
| Email interpretation | Rules identify confirmations, assessments, interviews, offers and rejections; uncertain fields remain unknown | Tests cover clear examples, unrelated mail and ambiguous wording |
| Review and correction | Accept, edit or dismiss proposed applications, statuses, events and tasks; inspect supporting text | Acceptance updates the correct application once and records what changed |
| Data control | Disconnect Gmail, clear imported content, delete the account and export applications as CSV | Each control has its documented effect without affecting another user |
| Delivery | Responsive interface, deployed HTTPS app, tests, synthetic demo data and setup documentation | A tester can complete the main journey without developer help |

The MVP automates extraction and preparation of updates. Scanning starts when the user selects **Scan Gmail**, and application changes require review. Continuous background scanning is a subsequent release.

A manual planner is the first delivery milestone. If Gmail is unfinished, release and describe that milestone accurately; a demonstration using synthetic messages does not establish a functioning inbox integration.

### Features reserved for later

Outlook/Yahoo/IMAP, forwarding addresses, multiple connected inboxes, unattended status changes, calendar integration, email or push reminders, Google Sheets/Notion synchronisation, browser autofill, job discovery, CV generation, subscriptions and native mobile apps are outside the first release.

CSV export supports spreadsheet users without introducing two-way synchronisation. In-app due-date sections provide visibility; they are not external reminder notifications.

## 5 Application stages and planning rules

Use these application statuses: **Saved, Applied, Assessment, Interview, Offer, Accepted, Rejected and Withdrawn**. Interview rounds and assessment centres are event details, so the status list stays manageable.

- Offer means an employer has made an offer; Accepted means the applicant has accepted it. Do not infer one from the other.
- Silence is not a rejection. Show elapsed time since activity without inventing an employer decision.
- Tasks describe work to do; scheduled events describe appointments; history records changes that have happened.
- An application may have no known application date or next task. Empty fields are valid when the information is unavailable.
- Archiving hides an application and its tasks from the normal dashboard while preserving its history.
- A correction creates a new history entry. Reversing an entire previously accepted import is deferred, because later user edits may depend on it.

The beta displays dates in **Europe/London**, clearly labelled. Preserve date-only deadlines as dates, store exact appointment times in UTC, and require confirmation when an imported date or timezone is ambiguous.

## 6 Interface plan

Use a simple navigation bar with Dashboard, Applications, Review and Settings, plus an Add application button.

| Screen | Main purpose | Key behaviour |
|---|---|---|
| Dashboard | Decide what needs attention | Group actions by urgency; link each action to its application |
| Applications | Find and manage the pipeline | Search company/role, filter stage, show next action and open archived records |
| Application detail | Plan one recruitment process | Show stage, next task, scheduled events, notes and history together |
| Review | Check email-derived suggestions | Compare current and proposed values; show email date, source excerpt and proposed application match |
| Settings | Manage connections and stored data | Show connected account, last scan, reconnect state, disconnect, export and deletion controls |

Create/edit forms can be ordinary pages. Use a table on desktop and stacked application summaries on mobile. Status labels must remain understandable without colour, forms need visible labels, and all essential actions should work with a keyboard.

Design these states explicitly: no applications yet, no upcoming actions, no matching search results, scan in progress, no relevant emails found, interrupted scan and Gmail reconnection required. The manual planner remains usable throughout an email-service failure.

## 7 System architecture

Use a **modular Django monolith**: one Python application with separate modules for tracking and email integration. Server-rendered pages keep the initial frontend close to the backend and reduce the amount of infrastructure to learn.

```text
Browser
   | HTTPS and Django session
   v
Django web application
   |-- Accounts and permissions
   |-- Applications, tasks, events and dashboard
   |-- Gmail connection and import processing ------> Gmail API
   |-- Rules and proposal review
   |-- Optional AI extraction experiment ----------> Model provider
   |
   v
PostgreSQL
```

| Layer | MVP decision |
|---|---|
| Language and framework | Python and a supported Django release, with versions locked |
| Frontend | Django templates, HTML, CSS and small JavaScript enhancements |
| Database | SQLite may support the initial local learning exercise; PostgreSQL before hosted beta validation |
| Authentication | Existing Django authentication and server-side sessions; keep username/password login unless email login has already been implemented deliberately |
| Dependencies | Keep the project's Pipenv workflow and commit its lockfile |
| Email | Google API client and web-server OAuth; connection consent is separate from signing into ApplyCue |
| Processing | Small, resumable scan batches with explicit timeouts and saved progress; no long mailbox scan inside a single HTTP request |
| Deployment | Managed Python hosting and PostgreSQL, environment secrets, HTTPS and backups |
| Quality | Django tests, dependency checks and CI on GitHub; error logs exclude email content and tokens |

Keep the current working folder layout. Add an integration module such as `integrations/gmail/` when the feature needs it. A shared import service can later run in a queue worker; Celery/Redis, webhooks and provider abstraction layers are not prerequisites for the first manual scan. If a batch cannot fit within the host's request limits, introduce a worker before increasing the workload.

Match documentation to the installed Django version and keep it on a supported patch release; consult the [official supported versions list](https://www.djangoproject.com/download/).

## 8 Database design

Use Django migrations, explicit relationships and ownership checks. Keep company names as text initially: a shared company directory is not necessary to manage applications.

| Record | Core fields and relationships |
|---|---|
| User | Existing Django account; owns applications and the mailbox connection |
| JobApplication | Owner, company, role, status, applied date, job URL, notes, created/updated timestamps, archived timestamp |
| Task | Application, title, due date, optional due time, completion timestamp, optional originating proposal |
| ApplicationEvent | Application, event kind, recorded timestamp, optional scheduled appointment time, details, previous/new status where relevant, manual/email source |
| MailboxConnection | Owner, provider account identity, encrypted credentials, granted scopes, connection status, last successful scan |
| ImportRun | Connection, selected date range, progress/cursor, counts, started/finished timestamps and sanitised error state |
| ImportedMessage | Connection, provider message/thread IDs, received time, minimal metadata, temporary evidence excerpt and processing state |
| ProposedUpdate | Imported message, optional target application, proposed fields/actions, reference to source evidence, missing fields, pending/accepted/dismissed state, reviewed timestamp |

`ApplicationEvent` supplies both the timeline and status-change history. Start with an application notes field rather than separate note and status-audit tables. Preserve an existing equivalent model name if it is already in use.

Enforce these invariants:

1. Imported message identity is unique by connection and provider message ID. Preserve the connection identity when the same user disconnects and reconnects the same mailbox. Repeated scans do not create repeated proposals.
2. Approval is transactional and can succeed only once per proposal, including when the user double-clicks or retries a request.
3. Every selected application, task or proposal must belong to the current user. Enforce ownership on form submissions as well as page reads.
4. Company and role text are not uniqueness keys. Users may reapply or track multiple roles at the same employer.
5. Clearing imported content removes message subjects, excerpts and pending proposals without cascading into approved applications/tasks. Retain only minimal receipts containing the provider account identity, message ID and processed disposition to prevent re-imports. Explain this in the control; account deletion removes these receipts too. Source references can become empty while the approved record remains.
6. Index frequent queries such as owner/status, application/event time and application/task deadline; add more indexes when query measurements justify them.

## 9 Email processing and AI

The initial scan covers a user-selected period, defaulting to the previous 90 days, with at most 100 candidate messages per run. Process small batches and show when the limit is reached; do not present a partial scan as a complete inbox history. [Gmail supports searching by date, sender and label through its message-list query](https://developers.google.com/workspace/gmail/api/guides/filtering).

The pipeline is:

```text
Fetch candidate messages
  -> normalise text and remove quoted-history noise where possible
  -> skip already processed IDs
  -> classify and extract supported fields
  -> propose an application match
  -> user reviews and corrects
  -> save application changes and history in one transaction
```

Use explicit wording and combined signals for rules. A word such as “unfortunately” alone is insufficient evidence for rejection. Job alerts, interview advice and recruiter marketing belong in negative test cases. Thread IDs, employer domains and role text can suggest a match; ambiguous matches require user selection.

An older email must not silently overwrite a later stage or manual edit. Review shows both the current value and the proposed value, and rechecks them at acceptance time.

AI has two separate roles:

- **During development:** explanations, review, debugging and test suggestions, alongside manual implementation of models, forms and business rules.
- **Inside the product:** a small, optional extraction experiment for ambiguous messages after the rules and review flow work. Keep it behind a feature flag and begin with synthetic messages. Before processing real emails, establish user consent and compatible provider data handling.

The model returns a validated schema, including unknown values and supporting text. Email text is untrusted data; the model receives no tools that can send mail or act on instructions inside messages. It cannot approve proposals, decide permissions or write directly to the database. Display uncertainty as “needs confirmation”; a model-generated confidence number is not a measured probability.

## 10 Security and data lifecycle

Security requirements follow the actual sensitive operations: account access, mailbox consent, stored credentials, imported content and external model processing.

- Use Django password handling, sessions and CSRF protection. Require authentication for private views and ownership checks for every related record.
- Use Google's web-server OAuth libraries, validate session-bound state and use registered redirect URLs. Encrypt retained credentials with a key kept separately from the database. [Google's web-server OAuth guide](https://developers.google.com/identity/protocols/oauth2/web-server).
- Keep deployment secrets outside Git, use HTTPS and secure cookies, and exclude raw emails, tokens and OAuth callback codes from logs and demo fixtures.
- Render email evidence as escaped text. Validate URLs and CSV cells so imported text cannot become executable HTML or spreadsheet formulas.
- Discard full message bodies after processing. Store a review excerpt once and reference it from proposals. Expire excerpts and any copied quotations after seven days or sooner when dismissed. A pending proposal with expired evidence must display that state and require the user to inspect the original email and reconfirm its fields before accepting. Keep quotations out of permanent history; retain only minimal extracted facts for accepted records.
- On disconnect, stop future scans, remove local credentials and request provider revocation. If revocation fails, explain how to revoke access in Google. Provide a separate Clear imported content control with the receipt-retention behaviour described above. Account deletion removes the account, owned data and receipts, with backup expiry documented.
- Maintain database backups and perform one restore test before hosting real beta data. Document the actual backup retention period selected with the host.

`gmail.readonly` grants broad mailbox read access, not permission restricted to job messages. ApplyCue's filtering limits what it processes; the consent explanation must make this distinction clear. Google classifies this scope as restricted and sets verification and, for applicable server storage/transmission, security-assessment requirements. Public Gmail rollout therefore has an external approval dependency beyond the development sprint. [Gmail scope requirements](https://developers.google.com/workspace/gmail/api/auth/scopes).

External OAuth projects in Testing using Gmail scopes receive refresh tokens that expire after seven days. The beta needs a clear reconnect flow. [Google refresh-token expiry rules](https://developers.google.com/identity/protocols/oauth2#expiration).

## 11 Delivery plan

Treat two weeks as a focused development timebox of approximately **60–75 hours**, with scope checkpoints. This is an ambitious estimate for someone learning Django. At 10–15 hours a week, the same work is roughly four to eight weeks. Google verification is outside this estimate.

| Days | Deliverable | Checkpoint |
|---|---|---|
| 1–2 | Confirm Django runs, lock dependencies, create application model and admin; establish login and ownership | A signed-in user can save and retrieve an owned application |
| 3–4 | Application list, detail and forms; tasks, notes and events | Create an application, plan its next action and complete it |
| 5–6 | Dashboard, search/filter/archive, mobile layout and meaningful tests | Two users have isolated data; dashboard dates and task states are correct |
| 7 | Deploy the manual foundation with PostgreSQL and synthetic demo data; assess Gmail OAuth prerequisites | A tester can use the complete manual journey on the hosted app |
| 8–9 | Build the proposal review workflow with synthetic fixtures; implement atomic acceptance | Accept, correct, dismiss and retry all behave correctly |
| 10–11 | Connect one real test Gmail account; fetch bounded batches, classify and deduplicate | A real email produces a reviewable proposal; reconnection and retries work |
| 12 | CSV export, disconnect/deletion, error states and classifier evaluation | Required controls and clear failure paths work |
| 13 | End-to-end review with several testers; fixes and backup/restore check | Release-blocking defects are resolved |
| 14 | Final deploy, README, architecture/security notes, demo recording and release tag | Manual and Gmail flows are demonstrated accurately |

Start checking Google consent requirements early, even though the integration code comes later. If the manual foundation is incomplete at day seven, finish it before adding Gmail. If Gmail remains blocked at day fourteen, release the manual foundation and identify email integration as unfinished. Defer AI expansion and visual extras before reducing ownership, data-control or review safeguards.

## 12 Acceptance and validation

The email-assisted MVP is complete when all of the following are demonstrated:

- A new beta user can create an application, add a deadline and interview, and see both on the dashboard.
- Login and ownership checks protect applications, tasks, events, exports and proposal actions across two test users.
- Multiple applications to one employer remain separate, and ambiguous matches require a choice.
- A live Gmail scan creates proposals; repeated imports and repeated acceptance create no duplicates.
- Accepting a proposal applies all approved changes or none. A conflicting manual edit triggers a fresh review.
- Missing company names, ambiguous deadlines and unrelated emails do not generate invented facts.
- Gmail expiry/failure leaves manual records intact and provides a usable reconnect/retry path.
- Disconnect, content clearing and account deletion follow the stated policy; content clearing preserves approved records and deduplication receipts, while account deletion removes them all.
- Core pages work at mobile width and with keyboard navigation. Loading, empty and error states are understandable.
- The hosted release has no exposed secrets or real email content in its public demonstration, fixtures or repository.

Build a labelled set of at least 40 synthetic or appropriately redacted emails covering positive categories, unrelated messages, ambiguity, old replies and multiple roles at one company. Report classification precision/recall and field-extraction errors with sample counts. Synthetic test results show fixture performance, not proven accuracy across real inboxes.

For a small usability pilot, ask five applicants to add an application, plan a deadline and review an imported update. A useful initial target is four of five completing the flow without help in ten minutes. Record where they hesitate and whether reviewing proposals actually saves effort. These are proposed evaluation targets, not achieved results.

## 13 Later releases and portfolio outcome

After the beta, prioritise work using observed problems:

1. Improve matching and date extraction using correction feedback; add optional AI only where evaluation shows benefit.
2. Add scheduled imports with a durable worker, retries, overlapping-run protection and clear sync status.
3. Add external reminders or calendar export if users miss actions despite using the dashboard.
4. Add Outlook or forwarding support if email coverage prevents adoption; review each provider's access requirements.
5. Consider spreadsheet synchronisation, deeper analytics and a commercial model after repeat usage is established.

The project primarily supports **full-stack software engineering, Python/backend development and integration engineering** applications. Security and responsible AI choices strengthen that evidence without requiring a separate cybersecurity or machine-learning product.

The portfolio package should contain a working demo, reproducible setup, architecture and data-model diagrams, test evidence, a short decision log, known limitations and a walkthrough of a real user journey. Describe features on the CV only once they are implemented and demonstrated.

For learning, own the model design, migrations, forms, permission checks, classification tests and deployment decisions. Make small commits for completed behaviours, review diffs and use feature branches. A useful next development ticket is: **a signed-in user can create an application and see only their own applications in a list**. This establishes the data, authentication and interface foundation for everything that follows.

## 14 Build references

- [Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/) for the first model, view and template flow.
- [Django testing guide](https://docs.djangoproject.com/en/stable/topics/testing/overview/) for user isolation and workflow tests.
- [Django deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/) before hosted testing.
- [Google web-server OAuth](https://developers.google.com/identity/protocols/oauth2/web-server) and [Gmail filtering](https://developers.google.com/workspace/gmail/api/guides/filtering) for integration.
- [Existing research library](RESOURCE_RESEARCH.md) for additional repositories, tutorials and product references; recheck version-sensitive examples before use.
- [Earlier folder proposal](FOLDER_ARCHITECTURE.md) for optional organisational ideas as the code grows; it is not a required scaffold.
