# ReasonedOps

[![CI](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/gigichengnc/reasoned-ops/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/gigichengnc/reasoned-ops?display_name=tag)](https://github.com/gigichengnc/reasoned-ops/releases/latest)
[![PyPI](https://img.shields.io/pypi/v/reasoned-ops.svg)](https://pypi.org/project/reasoned-ops/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](pyproject.toml)

**Route service requests, preserve machine/human decision history, and refuse management comparisons the observed data cannot support.**

ReasonedOps is a local service-operations research prototype organized around three responsibilities:

> **Operate → Audit → Evaluate**

- **Operate:** transparent rule/phrase request features and deterministic routing, exposed through FastAPI.
- **Audit:** preserve the original request, machine recommendation, human confirm/override, effective route, and outcome separately.
- **Evaluate:** inspect raw outcomes, comparison support and method applicability before producing an adjusted result; a department ranking can be withheld when the design is not identifiable.

## Run it

Install the currently verified public package and generate the reviewer showcase:

```bash
pip install reasoned-ops==1.4.3
reasoned-showcase
```

Or run the service API:

```bash
uvicorn reasoned_ops.api:app --reload
```

> **Evidence boundary:** Operate is a deterministic rule/phrase baseline, not a trained NLP model. Public routing evidence is hand-authored; outcome, policy and longitudinal evidence is synthetic. No representative real private-data pilot or production deployment is claimed. Observed-data diagnostics also cannot prove that unmeasured confounding is absent.

ReasonedOps originated from an **HKMU Hackathon 2026** concierge concept and was later rebuilt independently into the current evidence-aware workflow. The project was previously named **ANCOVA Ops**; ANCOVA/regression is now only one method inside Evaluate, not the product identity. HKMU is referenced only as project origin, not as an endorsement.

## Portfolio snapshot

| Item | Current project state |
| --- | --- |
| Original problem | Understand and route unstructured service requests more intelligently |
| Original setting | Property-management / concierge service requests |
| Evolution question | Can the same system preserve accountability and stop misleading outcome comparisons? |
| Operate | **Rule-based request features + deterministic routing baseline** exposed through FastAPI; v1.4.4 hardens word/phrase matching and safety-review rules |
| Audit | SQLite persistence for original case, machine route, human review, effective route and outcome |
| Evaluate | Raw summaries, overlap/identifiability checks, method applicability, guarded regression/ANCOVA reporting |
| Refusal behaviour | Can withhold a department ranking when the observed design cannot support it |
| Known limitation benchmark | Explicitly reproduces a case where hidden confounding is invisible to implemented checks and the gate still says `use` |
| Other research | Offline adaptive-policy evaluation + leakage-aware longitudinal benchmark |
| Model escalation | LSTM / sequence modelling deferred until it can beat simpler baselines on the same benchmark |
| Validation | Hand-authored fixtures + deterministic synthetic known-truth and known-limitation scenarios |
| Python distribution | Wheel + source distribution build and clean-wheel installation validated in CI |
| Previously verified public release | **v1.4.3** — GitHub / Zenodo / PyPI aligned and externally exercised |
| Current code checkpoint | **v1.4.4 release candidate** — post-audit routing, applicability and diagnostics bugfixes |
| PyPI status | Currently published and externally exercised: `reasoned-ops==1.4.3`; v1.4.4 is not public until exact-tag release verification is complete |
| Zenodo archives | v1.4.1 → `10.5281/zenodo.22044222`; v1.4.2 → `10.5281/zenodo.22044621`; v1.4.3 → `10.5281/zenodo.22046490` |
| v1.4.4 provenance | **Pending release**; no DOI is claimed before Zenodo ingests the exact v1.4.4 tag |
| Real-world performance claim | **Not made**; representative real-pilot evidence does not exist in this repository |
| Development data boundary | Synthetic / hand-authored public development evidence only |
| Production status | **Not approved** |
| Project status | v1 reopened only for the v1.4.4 audit bugfix close-out; freeze again after public-artifact alignment |
| Project identity | **ReasonedOps — Operate → Audit → Evaluate** |

Install the currently verified public package:

```bash
pip install reasoned-ops==1.4.3
```

The v1.4.4 hardening checkpoint exists because a further adversarial review found reproducible Operate and evidence-gate issues after v1.4.3: substring collisions such as `current`/`rent` and `feedback`/`fee`, emergency/safety requests that did not reliably enter human review, a standalone applicability CLI that could be told overlap was `supported`, and VIF warnings calculated on categorical dummy columns. Those findings are fixed with regression coverage before v1 is frozen again.

The v1.4.4 release will use the **same Git tag** as the source for the GitHub release, Zenodo archive and PyPI publication. The release-candidate `CITATION.cff` therefore intentionally carries no v1.4.3 DOI; the exact v1.4.4 DOI will only be recorded after Zenodo mints it.

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

That direction contained useful ideas: natural-language intake, human-centred triage, recurring-case awareness, and learning from outcomes. It also mixed together tasks that should have been separated and implied model sophistication that the current baseline does not claim.

The reconstructed starting point is preserved under [`original/`](original/README.md).

## Why did the project evolve?

As development continued, several questions in the early concept were not technically or methodologically clean.

- **ANCOVA was placed too close to message understanding.** ANCOVA cannot parse or filter an individual request; it belongs downstream on accumulated outcome data.
- **A final route was not enough for accountability.** Later evaluation needs to know what the system recommended, why, whether a person changed it, and what outcome followed.
- **Raw department averages can be badly misleading.** A team that handles harder cases may look slower even when its process is not worse.
- **A statistical model should be allowed to say “do not compare”.** If department and case type do not overlap, no attractive adjusted ranking should be manufactured.
- **Observed-data diagnostics cannot certify that every relevant confounder was measured.** A clean-looking frame can still support a badly biased adjusted answer.
- **The project name had become too narrow.** A system that can recommend logistic, survival, cluster-aware, or offline-policy methods is not really an “ANCOVA product”.
- **More complex AI was not automatically progress.** Sequence/LSTM work is deferred until the same benchmark shows incremental value over simpler approaches.
- **Proposal targets are not measured evidence.** Presentation-era percentages are not treated as ReasonedOps performance results.

The detailed audit is in [`docs/original-concept-audit.md`](docs/original-concept-audit.md).

## What changed

| Early Hackathon-stage concept | ReasonedOps today | Why the change matters |
| --- | --- | --- |
| AI concierge / routing as the centre | **Operate → Audit → Evaluate** | Routing alone cannot show whether the process later improved |
| NLP + emotional/context signals | **Rule-based operational request features** | The current baseline is transparent and does not pretend a keyword/rule system is a trained NLP model |
| ANCOVA described near emotion filtering | ANCOVA only after accumulated outcomes exist | Statistical outcome analysis is not message understanding |
| Department recommendation | Versioned route + human-readable reasons | The recommendation can be reconstructed and challenged |
| Human-centred idea | Append-only human confirm / override history | Human judgement becomes part of the audit trail |
| Outcome feedback | Outcome stored separately from routing history | Later outcomes do not rewrite the earlier decision |
| Compare service performance | Check department × case-type overlap first | Different teams may be handling fundamentally different work |
| Adjusted model produces answer | `supported`, `weak_overlap`, or `not_identifiable` | The software can refuse an unsupported ranking |
| Diagnostics look clean | Known-limitation benchmark for omitted confounding | Passing observed checks does not prove the adjusted answer is correct |
| ANCOVA as intellectual centre | Applicability gate selects or rejects method families | Method follows the question |
| Adaptive routing ambition | Offline policy evaluation with deployment lock | Historical-policy research is not silently promoted to live automation |
| Longitudinal history | Leakage-aware synthetic benchmark | Future information must not leak into historical evaluation |
| More advanced sequence model later | LSTM explicitly deferred | Complexity must earn its place |

See [`docs/before-vs-after.md`](docs/before-vs-after.md) for the fuller comparison.

## What actually runs

ReasonedOps is a **local research/software prototype**, not only a conceptual document.

### 1. Operate — rule-based structure and routing

Imagine this request arrives:

```text
The air conditioner is leaking again. This is the third time and the wet floor could be dangerous.
```

From the currently verified public package:

```bash
pip install reasoned-ops==1.4.3
uvicorn reasoned_ops.api:app --reload
```

Or from the current v1.4.4 repository checkpoint:

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

These fields are produced by a **transparent rule/phrase baseline plus declared thresholds**. v1.4.4 uses word/phrase boundaries rather than raw substring matching and adds explicit emergency, safety and security human-review paths. Terms such as `frustration` remain operational text features, not psychological measurements. The baseline exists so future NLP/ML approaches have something explicit to outperform rather than replacing a simple method merely because a more complex model is available.

### 2. Audit — preserve what the machine and human each decided

The machine recommendation is not final authority. A staff member can confirm or override the route, while ReasonedOps preserves the original machine decision rather than replacing it.

```text
Original request
      ↓
Machine / rule recommendation
      ↓
Human confirmation / override
      ↓
Effective route
      ↓
Observed outcome
```

This makes later questions auditable: what the system recommended, which version produced it, why it recommended that route, whether a staff member changed it, and what happened afterward.

### 3. Record the outcome separately

When the case is complete, the outcome can be stored separately from the routing decision. Later knowledge therefore does not rewrite the historical decision.

### 4. Evaluate — ask whether the management comparison is supportable

Suppose a dashboard later shows:

```text
Maintenance  18 hours average resolution time
Security      7 hours average resolution time
```

A naive conclusion is:

> Maintenance performs worse.

ReasonedOps asks first:

> Did Maintenance and Security actually handle comparable cases?

If department and case type do not provide enough overlap, the correct result can be:

```text
REJECT
Do not produce an adjusted department ranking from this design.
```

If overlap is sufficient, an adjusted workflow can be used with diagnostics, uncertainty and explicit non-causal boundaries.

## The validity benchmark now tests a blind spot too

The current `reasoned-validity` benchmark includes five deterministic synthetic scenarios:

```text
known_effect_recovery
measured_confounding
no_overlap
slope_interaction
unmeasured_confounding_blind_spot
```

The first four exercise behaviour the implemented workflow is expected to handle. The fifth is deliberately different.

For `unmeasured_confounding_blind_spot`, the data generator creates a true latent case-burden variable that affects both department assignment and resolution time. The benchmark then **removes that variable before the ordinary Evaluate pipeline sees the data**.

The expected result is intentionally uncomfortable:

```text
observed overlap looks supported
        ↓
implemented diagnostics do not see the omitted variable
        ↓
applicability gate returns USE
        ↓
adjusted department contrast is badly biased and reverses the known true direction
```

`PASS` for this scenario therefore means **the benchmark successfully reproduced and disclosed a known false-negative mode**. It does **not** mean ReasonedOps detected hidden confounding.

The existing `use` interpretation boundary explicitly says that the gate does not prove model correctness, absence of unmeasured confounding, or causal identification. The benchmark turns that disclosure into executable evidence of what the current safeguards cannot detect.

This distinction matters: ReasonedOps can refuse some unsupported comparisons that are visible in observed data, but it cannot certify that unrecorded causes do not exist.

## One-command reviewer path

Run:

```bash
reasoned-showcase
```

The command executes the current development workflows and writes:

```text
.reasoned_ops/showcase/showcase.md
```

The generated report walks through one service request and later evidence checks. The results are synthetic / hand-authored development evidence, not production performance estimates.

## Public release verification

The previously verified `reasoned-ops==1.4.3` package was published from the exact Git tag `v1.4.3`, after the same release had been archived by Zenodo.

The publishing workflow verified:

```text
requested tag: v1.4.3
release commit: 461b5fc81c2b31fc5fcc51c585004d059bb85586
package version: 1.4.3
```

Both the wheel and source distribution were accepted by PyPI, with Trusted Publishing / Sigstore attestations generated during publication.

The public package was then installed in a Windows environment outside the repository checkout. Observed results included:

```text
reasoned_ops.__version__ = 1.4.3

reasoned-validity --n 1200 --seed 23
Overall pass: True
- known_effect_recovery: PASS
- measured_confounding: PASS
- no_overlap: PASS
- slope_interaction: PASS
- unmeasured_confounding_blind_spot: PASS
```

A routing smoke check on the recurring leaking-air-conditioner request returned:

```text
department = maintenance
priority = high
requires_human_review = True
secondary_notify = community_management
```

That establishes installability, exact-version provenance and executable local behaviour for v1.4.3. It does **not** establish independent scientific effectiveness, causal business impact, private-data approval, or production readiness. v1.4.4 must repeat the same exact-tag public-artifact verification before becoming the new frozen checkpoint.

See [`docs/publication-verification.md`](docs/publication-verification.md).

## Method and model decisions

The project deliberately records several decisions **not** to escalate complexity or claims.

- rule-based transparent routing remains the reference baseline;
- ANCOVA was moved downstream instead of being forced into message understanding;
- no-overlap department comparisons are withheld;
- hidden confounding is acknowledged as an observational blind spot rather than treated as detectable by ordinary diagnostics;
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
rule-based request features
      ↓
deterministic routing recommendation + rule trace
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

The repository separates several evidence classes:

- **Hand-authored routing fixture:** deterministic routing behaviour, expected-human-review cases and rule-trace coverage. v1.4.4 adds adversarial substring and safety cases. This is an implementation benchmark, not external accuracy.
- **Synthetic known-truth outcome scenarios:** known-effect recovery, measured-confounding adjustment, no-overlap refusal and slope-interaction detection.
- **Synthetic known-limitation scenario:** hidden confounding deliberately omitted from the observed frame to demonstrate a false-negative mode the implemented checks cannot identify.
- **Synthetic adaptive-policy logs:** deterministic logged-policy data with known propensities, chronological validation, support diagnostics and deployment locks.
- **Synthetic longitudinal histories:** simpler recurrence/time approaches compared under leakage-aware chronological validation.
- **Public artifact execution:** v1.4.3 is the currently externally exercised PyPI artifact; v1.4.4 remains a release candidate until exact-tag publication and fresh-environment verification are complete.

None of these evidence classes establishes real service improvement or causal effectiveness.

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

A separate distribution job checks wheel/sdist build, clean-environment wheel installation, import/version consistency, routing smoke behaviour and an installed CLI entry point.

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

- [`original/README.md`](original/README.md) — reconstructed early Hackathon-stage concept;
- [`docs/before-vs-after.md`](docs/before-vs-after.md) — early-vs-current comparison;
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
- [`docs/project-status.md`](docs/project-status.md) — completion and deployment status.

## Current limitations

ReasonedOps demonstrates a disciplined service-operations workflow; it does **not** establish real-world effectiveness.

Important limitations remain:

- Operate is a deterministic rule/phrase baseline, not a trained NLP model;
- routing evaluation is hand-authored development evidence;
- outcome, adaptive-policy and longitudinal quantitative evidence is synthetic;
- observed-data diagnostics cannot rule out unmeasured confounding;
- the validity benchmark demonstrates one such false-negative mode explicitly;
- no representative real private-data pilot has been run;
- adjusted regression results are not causal effects by default;
- authentication/RBAC and production security are outside the research prototype;
- real longitudinal personalisation is not approved;
- production deployment is not approved.

## Next evidence gate

The next meaningful step is **not another model**.

ReasonedOps v1 was reopened only to correct reproducible audit findings in v1.4.3. After v1.4.4 is archived, published from the exact tag and externally rechecked, v1 should be frozen again. If the project is later resumed for a real use case, the next gate is:

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
build a transparent routing baseline
      ↓
preserve decision history
      ↓
capture outcomes separately
      ↓
check whether comparisons are supportable
      ↓
expose an observed-data blind spot
      ↓
select, caution, reject or redirect the method
      ↓
defer unjustified complexity
      ↓
define the next real evidence gate
```

That is what **ReasonedOps** now represents.
