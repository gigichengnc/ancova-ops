# ReasonedOps: From an AI Concierge Concept to Evidence-Aware Service Operations

[![CI](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/gigichengnc/reasoned-ops?display_name=tag)](https://github.com/gigichengnc/reasoned-ops/releases/latest)
[![PyPI](https://img.shields.io/pypi/v/reasoned-ops.svg)](https://pypi.org/project/reasoned-ops/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22044621.svg)](https://doi.org/10.5281/zenodo.22044621)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)

ReasonedOps originated from my participation in **HKMU Hackathon 2026** and evolved into a runnable, auditable service-operations research prototype.

The project began by asking whether an AI-assisted concierge could understand a resident request, consider urgency and communication context, and route the case to the right team.

As the project evolved, a second problem became more important:

> After an operational system starts producing data, how do we stop managers from drawing conclusions that the data cannot actually support?

ReasonedOps now separates three responsibilities:

> **Operate → Audit → Evaluate**

It is not designed to make management decisions automatically. It is designed to make **unsupported management conclusions harder to reach**.

The project was originally developed under the name **ANCOVA Ops**. It was renamed **ReasonedOps** because ANCOVA/regression is only one method inside the Evaluate layer, not the product itself.

**HKMU Hackathon 2026 is referenced only to describe the project's origin. ReasonedOps is independently developed and is not presented as an official HKMU product or endorsement.**

## Portfolio snapshot

| Item | Current project state |
| --- | --- |
| Original problem | Understand and route unstructured service requests more intelligently |
| Original setting | Property-management / concierge service requests |
| Evolution question | Can the same system also preserve accountability and stop misleading outcome comparisons? |
| Operate | Runnable FastAPI request-intelligence + explainable routing workflow |
| Audit | SQLite persistence for original case, machine route, human review, effective route and outcome |
| Evaluate | Raw summaries, overlap/identifiability checks, method applicability, guarded regression/ANCOVA reporting |
| Refusal behaviour | Can withhold a department ranking when the observed design cannot support it |
| Other research | Offline adaptive-policy evaluation + leakage-aware longitudinal benchmark |
| Model escalation | LSTM / sequence modelling deferred until it can beat simpler baselines on the same benchmark |
| Validation | Hand-authored fixtures + deterministic synthetic known-truth scenarios |
| Python distribution | Wheel + source distribution build and clean-wheel installation validated in CI |
| PyPI status | **Published:** `reasoned-ops==1.4.0` via GitHub OIDC Trusted Publishing |
| Zenodo archive | **v1.4.2 DOI:** `10.5281/zenodo.22044621` |
| Public artifact verification | PyPI package installed outside the repository checkout; Operate → Audit → Evaluate paths exercised successfully |
| Real-world performance claim | **Not made**; representative real-pilot evidence does not exist in this repository |
| Development data boundary | Synthetic / hand-authored public development evidence only |
| Production status | **Not approved** |
| Project identity | **ReasonedOps — Operate → Audit → Evaluate** |

Install the released package:

```bash
pip install reasoned-ops==1.4.0
```

For the clearest summary of how the project changed, start with [`docs/before-vs-after.md`](docs/before-vs-after.md).

## The original question

At HKMU Hackathon 2026, the project direction was broadly:

```text
resident / tenant request
        ↓
NLP + urgency / emotional context
        ↓
department classification
        ↓
historical context
        ↓
adaptive routing
        ↓
department queue
        ↓
outcome feedback
```

That direction contained several useful ideas: natural-language intake, human-centred triage, recurring-case awareness, and learning from outcomes.

But the early concept also mixed together tasks that should have been separated.

The reconstructed starting point is preserved under [`original/`](original/README.md).

## Why did the project evolve?

As development continued, several questions in the early concept were not technically or methodologically clean.

- **ANCOVA was placed too close to message understanding.** ANCOVA cannot parse or filter an individual request; it belongs downstream on accumulated outcome data.
- **A final route was not enough for accountability.** Later evaluation needs to know what the system recommended, why, whether a person changed it, and what outcome followed.
- **Raw department averages can be badly misleading.** A team that handles harder cases may look slower even when its process is not worse.
- **A statistical model should be allowed to say “do not compare”.** If department and case type do not overlap, no attractive adjusted ranking should be manufactured.
- **The project name had become too narrow.** A system that can recommend logistic, survival, cluster-aware, or offline-policy methods is not really an “ANCOVA product”.
- **More complex AI was not automatically progress.** Sequence/LSTM work is deferred until the same benchmark shows incremental value over simpler approaches.
- **Proposal targets are not measured evidence.** Presentation-era percentages are not treated as ReasonedOps performance results.

The detailed audit is in [`docs/original-concept-audit.md`](docs/original-concept-audit.md).

## What changed

| Early Hackathon-stage concept | ReasonedOps today | Why the change matters |
| --- | --- | --- |
| AI concierge / routing as the centre | **Operate → Audit → Evaluate** | Routing alone cannot show whether the process later improved |
| NLP + emotional/context signals | Transparent operational request intelligence | Keeps triage signals separate from unsupported psychological claims |
| ANCOVA described near emotion filtering | ANCOVA only after accumulated outcomes exist | Statistical outcome analysis is not message understanding |
| Department recommendation | Versioned route + human-readable reasons | The recommendation can be reconstructed and challenged |
| Human-centred idea | Append-only human confirm / override history | Human judgement becomes part of the audit trail |
| Outcome feedback | Outcome stored separately from routing history | Later outcomes do not rewrite the earlier decision |
| Compare service performance | Check department × case-type overlap first | Different teams may be handling fundamentally different work |
| Adjusted model produces answer | `supported`, `weak_overlap`, or `not_identifiable` | The software can refuse an unsupported ranking |
| ANCOVA as intellectual centre | Applicability gate selects or rejects method families | Method follows the question |
| Adaptive routing ambition | Offline policy evaluation with deployment lock | Historical-policy research is not silently promoted to live automation |
| Longitudinal history | Leakage-aware synthetic benchmark | Future information must not leak into historical evaluation |
| More advanced sequence model later | LSTM explicitly deferred | Complexity must earn its place |

See [`docs/before-vs-after.md`](docs/before-vs-after.md) for the fuller technical comparison.

## What actually runs

ReasonedOps is a **local research/software prototype**, not only a conceptual document.

### A concrete service case

Imagine this request arrives:

```text
The air conditioner is leaking again. This is the third time and the wet floor could be dangerous.
```

### 1. Operate — structure and route the request

From PyPI:

```bash
pip install reasoned-ops==1.4.0
uvicorn reasoned_ops.api:app --reload
```

Or from a repository checkout:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn reasoned_ops.api:app --reload
```

Send the request:

```bash
curl -X POST http://127.0.0.1:8000/v1/route \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "demo-001",
    "message": "The air conditioner is leaking again. This is the third time and the wet floor could be dangerous.",
    "previous_related_cases": 2,
    "vulnerability_flag": false
  }'
```

The response contains structured operational fields such as:

```text
issue_category
urgency
frustration
complexity
department
priority
requires_human_review
reasons
intelligence_version
router_version
```

The important point is not only that a department is returned. The system also records **why** the recommendation was made and which logic/version produced it.

### 2. Audit — preserve what the machine and human each decided

The machine recommendation is not final authority.
A staff member can confirm or override the route. ReasonedOps preserves the original machine decision rather than replacing it.

Conceptually:

```text
Original request
      ↓
Machine recommendation
      ↓
Human confirmation / override
      ↓
Effective route
      ↓
Observed outcome
```

This makes later questions auditable:

```text
Why was this case sent there?
What did the system originally recommend?
Did a staff member change it?
Which system version was used?
What happened afterward?
```

### 3. Record the outcome separately

When the case is complete, an outcome can be stored through the API.

The outcome is a separate record from the routing decision so the system does not rewrite the historical decision after learning what happened.

### 4. Evaluate — management asks a harder question

Suppose a dashboard later shows:

```text
Maintenance  18 hours average resolution time
Security      7 hours average resolution time
```

A naive conclusion is:

> Maintenance performs worse.

ReasonedOps asks a different question first:

> Did Maintenance and Security actually handle comparable cases?

If Maintenance mainly handled complex repairs and Security mainly handled simpler complaints, the observed design may not support a department comparison at all.

In that situation the correct result can be:

```text
REJECT
Do not produce an adjusted department ranking from this design.
```

If overlap is sufficient, the evaluation layer can then use an appropriate adjusted workflow and report uncertainty and warnings.

That refusal behaviour is one of the main results of the project's evolution.

## One-command reviewer path

Run:

```bash
reasoned-showcase
```

The command executes the current development workflows and writes:

```text
.reasoned_ops/showcase/showcase.md
```

The generated report walks through one service request and then shows how the later evidence checks behave.

The results are synthetic / hand-authored development evidence, not production performance estimates.

## Reuse it from another Python project

ReasonedOps is published on PyPI, so another Python project can depend on it instead of copying source files.

Install the current verified release:

```bash
pip install reasoned-ops==1.4.0
```

The public Python surface starts with:

```python
from reasoned_ops import ServiceCase, baseline_route

case = ServiceCase(
    case_id="example-001",
    message="The air conditioner is leaking again.",
    previous_related_cases=2,
)

decision = baseline_route(case)
print(decision.department)
print(decision.reasons)
```

For reusable project dependencies, prefer an explicit compatible version range such as:

```text
reasoned-ops>=1.4,<2
```

Pin an exact version when reproducibility is more important than automatically receiving compatible updates.

See [`docs/pypi.md`](docs/pypi.md) for package reuse and release publishing, and [`docs/publication-verification.md`](docs/publication-verification.md) for the public-artifact verification record.

## Public release verification

After `reasoned-ops==1.4.0` was published, the package was installed from public PyPI in a Windows environment outside the repository checkout.

That verification exercised:

```text
PyPI install + import version 1.4.0
        ↓
Operate
routing + explanation + FastAPI request
        ↓
Audit
persisted machine route + human override + effective route + outcome
        ↓
Evaluate
known-effect recovery + confounding adjustment + no-overlap refusal + interaction detection
```

The deterministic validity benchmark reported:

```text
Overall pass: True
- known_effect_recovery: PASS
- measured_confounding: PASS
- no_overlap: PASS
- slope_interaction: PASS
```

This establishes that the public package is **installable and executable as a local research/software prototype**. It does not establish independent scientific effectiveness, causal business impact, private-data approval, or production readiness.

See [`docs/publication-verification.md`](docs/publication-verification.md).

## Method and model decisions

The project deliberately records several decisions **not** to escalate complexity or claims.

- transparent routing remains the reference baseline;
- ANCOVA was moved downstream instead of being forced into message understanding;
- no-overlap department comparisons are withheld;
- binary, censored, clustered and policy-counterfactual questions can be redirected to other method families;
- regression/ANCOVA output is non-causal by default;
- adaptive routing remains offline;
- longitudinal evaluation uses chronological leakage controls;
- LSTM remains deferred until justified by the same benchmark.

See [`docs/model-decisions.md`](docs/model-decisions.md).

## Current architecture

```text
SERVICE REQUEST
      |
      v
OPERATE
request intelligence
      ↓
explainable routing recommendation
      |
      +------> human confirmation / override
                       |
                       v
AUDIT
original request + machine decision + human review + effective route
                       |
                       v
observed outcome
      |
      v
EVALUATE
raw summaries
      ↓
comparison-support / identifiability gate
      ↓
method applicability
      |
      +--> USE / CAUTION: guarded regression / ANCOVA when appropriate
      |
      +--> REJECT: do not make the comparison
      |
      +--> RECOMMEND_ALTERNATIVE: logistic / survival / cluster-aware /
                                 offline-policy family as appropriate
```

ANCOVA is one tool inside **Evaluate**. It is not the project identity.

## Evidence and validation

The repository separates several forms of development evidence:

### Hand-authored routing fixture

A small fixture checks deterministic routing behaviour, expected-human-review cases and explanation coverage.

It is an implementation benchmark, not external accuracy.

### Synthetic known-truth outcome scenarios

The validity benchmark deliberately constructs situations where the data-generating truth is known. It checks whether the software can:

- approximately recover known effects;
- reduce measured case-mix confounding;
- refuse a structural no-overlap comparison;
- detect a deliberately introduced slope interaction.

These scenarios validate software/statistical behaviour, not real service impact.

### Synthetic adaptive-policy logs

Offline policy research uses deterministic logged-policy data with known propensities, chronological validation, support diagnostics and deployment locks.

### Synthetic longitudinal histories

The longitudinal benchmark compares simpler recurrence/time approaches under leakage-aware chronological validation.

### Public artifact execution

The PyPI verification demonstrates that the packaged release can be installed and its current local workflow executed outside the repository checkout.

That is distribution/execution evidence, not a new real-world outcome evidence class.

## Reproducibility

The GitHub Actions CI matrix runs on Python **3.11** and **3.12** and checks:

- editable package installation;
- Ruff linting;
- unit/regression tests;
- routing evaluation;
- evaluation validity;
- applicability decisions;
- adaptive-policy workflow;
- longitudinal benchmark;
- outcome analysis;
- management report;
- portfolio showcase;
- data-governance policy.

A separate distribution job also checks:

- `python -m build`;
- one wheel + one source distribution;
- installation of the built wheel into a clean virtual environment;
- import/version consistency from that installed wheel;
- a routing smoke check;
- an installed CLI entry point.

Main command-line entry points are:

```text
reasoned-evaluate
reasoned-validity
reasoned-applicability
reasoned-analyze
reasoned-management-report
reasoned-policy
reasoned-longitudinal
reasoned-showcase
reasoned-governance-check
```

## Repository map

```text
.
├── original/                  # reconstructed early Hackathon-stage concept
├── src/reasoned_ops/          # current Python implementation
├── data/
│   └── evaluation/            # hand-authored public development fixture
├── config/                    # machine-readable data-governance boundary
├── docs/                      # audits, comparisons, methodology, decisions, publishing guides
├── tests/                     # unit / regression tests
├── PYPI.md                    # package-index description
└── .github/workflows/         # CI, GitHub release and PyPI publishing workflows
```

The repository intentionally keeps **the project's own historical development** separate from the current implementation.

## Documentation guide

Start here:

- [`original/README.md`](original/README.md) — reconstructed early Hackathon-stage concept;
- [`docs/before-vs-after.md`](docs/before-vs-after.md) — clearest early-vs-current comparison;
- [`docs/original-concept-audit.md`](docs/original-concept-audit.md) — what was preserved, corrected, narrowed or deferred;
- [`docs/model-decisions.md`](docs/model-decisions.md) — why methods/models were selected, rejected or deferred;
- [`docs/architecture.md`](docs/architecture.md) — current technical architecture;
- [`docs/statistical-methodology.md`](docs/statistical-methodology.md) — guarded outcome-analysis workflow;
- [`docs/evaluation-applicability.md`](docs/evaluation-applicability.md) — `use` / `caution` / `reject` / alternative-method gate;
- [`docs/management-report.md`](docs/management-report.md) — management-facing evidence report;
- [`docs/data-governance.md`](docs/data-governance.md) — development data/privacy boundary;
- [`docs/pypi.md`](docs/pypi.md) — package reuse and Trusted Publishing procedure;
- [`docs/publication-verification.md`](docs/publication-verification.md) — verification of the public PyPI artifact;
- [`docs/citation.md`](docs/citation.md) — Zenodo DOI and citation/archive guidance;
- [`docs/project-status.md`](docs/project-status.md) — current completion and deployment status.

## Current limitations

ReasonedOps demonstrates a disciplined service-operations workflow; it does **not** establish real-world effectiveness.

Important limitations remain:

- routing evaluation is hand-authored development evidence;
- outcome, adaptive-policy and longitudinal quantitative evidence is synthetic;
- no representative real private-data pilot has been run;
- adjusted regression results are not causal effects by default;
- authentication/RBAC and production security are outside the research prototype;
- real longitudinal personalisation is not approved;
- production deployment is not approved.

## Next evidence gate

The next meaningful step is **not another model**.

If the project is ever resumed for a real use case, the next gate is:

```text
specific organisation / service process
        ↓
privacy + governance approval
        ↓
representative real cases
        ↓
independent routing / outcome-quality protocol
        ↓
predefined questions and stop criteria
        ↓
run the existing baseline once
        ↓
report what the real evidence supports
```

Only after that would production integration or more complex modelling be justified.

## Historical preservation

ReasonedOps preserves the history of the same project rather than presenting its current form as if it appeared fully formed.

The project originated from my participation in **HKMU Hackathon 2026** and was originally developed under the name **ANCOVA Ops**. Historical changelog entries retain that earlier name where it accurately describes the project at the time.

The current implementation lives under `src/reasoned_ops/`; the reconstructed starting concept lives under `original/`.

The strongest result of the project is the progression itself:

```text
hackathon concept
      ↓
audit assumptions
      ↓
separate operational and analytical tasks
      ↓
build explainable routing
      ↓
preserve decision history
      ↓
capture outcomes separately
      ↓
check whether comparisons are supportable
      ↓
select, caution, reject or redirect the method
      ↓
defer unjustified complexity
      ↓
define the next real evidence gate
```

That is what **ReasonedOps** now represents.