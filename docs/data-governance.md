# Data Governance

## Status

ReasonedOps is currently a **synthetic-only development project**. The repository is **not approved for real private resident or customer service records**.

This document defines project controls for development and future pilot planning. It is not a substitute for jurisdiction-specific legal, privacy, information-security or institutional review before a real deployment.

The machine-readable counterpart is `config/data-governance.json`. CI validates that the development guardrails remain in place.

## Core rules

1. **Minimise before collecting.** A field needs a stated operational purpose before it is added.
2. **Separate operations from analytics.** A field that is useful for live service handling is not automatically appropriate for modelling or training.
3. **Separate feedback from truth.** Staff confirmations and overrides are useful signals, but they are not automatically ground-truth labels.
4. **Do not infer unsupported personal traits.** Communication-intensity or emotional-need signals must not become mental-health, personality or protected-characteristic profiling.
5. **Prefer derived context to raw history.** For recurrence, use the minimum derived feature such as `previous_related_cases` rather than retaining full historical conversations when the full text is not necessary.
6. **No private records in Git.** Real service records, exports, attachments and local databases must never be committed to this repository.
7. **A new sensitive feature requires review.** Sensitive or longitudinal fields must be registered in the governance policy with purpose, retention expectation and pilot requirements before use.

## Development boundary

The approved development provenance is limited to:

- `synthetic`;
- `hand_authored_fixture`.

The project can therefore be developed, tested and evaluated without private operational data.

The current policy explicitly disables:

- real private records;
- direct identifiers;
- training on raw private request text;
- treating human routing feedback as automatic ground truth;
- longitudinal personalisation;
- general analytics exports that are not pseudonymised.

`data/private/`, `data/raw/`, local SQLite databases and environment files are Git-ignored. The ignore rules are a safety layer, not permission to place uncontrolled private data in the repository workspace.

## Data classes

### Operational and outcome data

Examples include structured issue category, department, priority, response time, resolution time, reassignment and escalation. These fields can support routing or outcome evaluation when they are pseudonymous and used for an approved purpose.

### Derived operational signals

`urgency` and `complexity` are modelling inputs. They must have documented definitions and versioned implementation logic if used in a pilot.

`frustration` is more sensitive because it represents communication intensity or emotional need. It is not a psychological measurement. Any analytical use requires an explicitly approved operational question and documented measurement limitations.

### Restricted context

`vulnerability_flag` may encode accessibility or safety context. It exists to trigger additional human attention, not to segment or profile residents. It is excluded from general analytics by default.

### Free text

`message` may contain names, addresses, unit numbers, health information, family circumstances or other unexpected personal data. It is therefore treated as restricted free text.

Raw request text is excluded from general analytics and model-training datasets by default. A future pilot must define why raw text is necessary, who can access it, how long it is kept, and how deletion or de-identification works.

### Pseudonymous identifiers

`case_id` links operational records without requiring a direct personal identifier. `actor_id` attributes a staff review but is excluded from general modelling exports by default.

Pseudonymous does not mean anonymous. Linkage keys and re-identification risk still need controls in any real pilot.

## Retention and deletion expectations

The current development project uses synthetic or hand-authored records, so development data can be regenerated or deleted at any time.

Before any private pilot data is imported, a pilot data schedule must set **concrete retention periods** for each data class. Until that schedule exists, real private data remains prohibited.

The pilot schedule must follow these principles:

- raw request text: keep only for the approved operational need and a documented short review window, then delete or de-identify;
- structured routing records: keep only for the approved audit/evaluation window;
- outcomes: keep only for the approved outcome-evaluation window;
- staff identifiers: keep only for the approved audit requirement and exclude from general training datasets;
- restricted context such as vulnerability: do not keep longer than the operational need unless a specific evaluation purpose and safeguards are approved;
- longitudinal linkage: use the shortest history window that can answer the approved operational question.

Deletion must include primary records and any derived exports that can still be linked to the deleted person or case, subject to documented audit or legal retention obligations identified for the pilot.

## Analytics and pseudonymisation

An analytics dataset should be created as a separate export rather than by analysing the operational database indiscriminately.

The default analytics export should exclude:

- raw request text;
- vulnerability context;
- staff actor identifiers;
- free-text routing-review reasons;
- direct personal identifiers;
- unregistered fields.

Approved structured fields should use a pseudonymous case key. If a pilot needs group-level reporting only, aggregation should be preferred over row-level disclosure.

The code-level `assert_analytics_columns()` guard rejects unregistered fields and fields marked `excluded_by_default`. It does not replace a privacy review; it prevents accidental expansion of the analytics surface.

## Human feedback and labels

A staff confirmation or override reflects an operational decision made in context. It can be useful for error analysis, but several things may make it an unreliable training label:

- staff can disagree;
- organisational policy may change;
- a routing decision can be operationally convenient without being optimal;
- the final outcome may contradict the routing choice;
- review behaviour may differ across teams or shifts.

Human feedback must therefore remain distinct from:

- the original machine/rule recommendation;
- the effective operational routing;
- the observed outcome;
- any adjudicated label set created for model evaluation.

## Longitudinal features

Every longitudinal feature must have an operational purpose and retention rationale before it is implemented.

### `previous_related_cases`

**Status:** approved for synthetic development.

**Purpose:** detect recurrence or unresolved history using a minimum derived count.

**Retention rationale:** the count can provide recurrence context without exposing full historical message content.

**Pilot requirement:** define the linkage method, notice, access controls and maximum history window before use.

### `resident_message_history`

**Status:** not approved.

**Potential purpose:** provide context for recurring service requests.

**Retention rationale:** full longitudinal free text creates unnecessary privacy and profiling risk at the current stage.

**Pilot requirement:** requires a separately approved purpose, notice/consent analysis, minimisation plan, retention period and security review.

### `emotion_trajectory`

**Status:** not approved.

**Potential purpose:** research changes in communication or service need over time.

**Retention rationale:** longitudinal emotion-like inference can become unsupported psychological profiling.

**Pilot requirement:** requires validated operational definitions, explicit review, a necessity case, notice/consent analysis and a prohibition on personality or mental-health inference.

### `resident_profile_embedding`

**Status:** not approved.

**Purpose:** no approved Phase 1 purpose.

**Retention rationale:** persistent behavioural embeddings are unnecessary for the current routing and evaluation goals.

**Pilot requirement:** do not implement without a new governance review and documented need.

## Notice and consent boundary for a future pilot

Before a real pilot introduces longitudinal personalisation or history-based features, the project must document at minimum:

- what data is collected;
- the operational purpose for each field;
- whether the feature is necessary for core service delivery or optional experimentation;
- what notice is provided to residents/customers and staff;
- whether consent is required for the proposed use in the relevant jurisdiction and institutional setting;
- how an individual can exercise applicable access, correction, objection or deletion rights;
- who can access raw data, linked history and analytics exports;
- retention periods and deletion procedures;
- whether third-party AI/model providers receive any data;
- what happens when a person does not participate in optional personalisation.

Optional personalisation must not be silently bundled into basic service access.

## Prohibited by default

The current project does not permit:

- committing real private resident/customer records to Git;
- direct identifiers in general analytics or model-training exports;
- raw private request text as training data without separately approved purpose and safeguards;
- automatic conversion of staff overrides into ground truth;
- mental-health, personality or protected-characteristic inference from service messages;
- persistent resident-level behavioural profiles or embeddings without a new governance review;
- longitudinal personalisation experiments before notice/consent, minimisation, retention and access-control requirements are approved.

## Adding a new field

A new data field should not be added silently. The change should include:

1. a field entry in `config/data-governance.json`;
2. sensitivity classification;
3. operational purpose;
4. analytics-use status;
5. retention expectation;
6. whether explicit review is required;
7. tests or documentation changes if the field affects current schemas or analytics.

For a new longitudinal feature, also add a longitudinal registry entry with status, purpose, retention rationale and pilot requirement.

## Governance check

Run:

```bash
reasoned-governance-check
```

Machine-readable output:

```bash
reasoned-governance-check --json
```

CI runs this check so a pull request cannot quietly change the repository from synthetic-only development into private-data use without making the policy change visible.
