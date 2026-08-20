# Release Readiness — v0.5.2

This checklist distinguishes three different meanings of "ready":

1. **repository checkpoint ready** — another developer can clone, install, test and understand the project;
2. **pilot ready** — approved to process real private service data in a controlled study;
3. **production ready** — approved to operate as a real service-routing system.

ANCOVA Ops v0.5.2 is intended to satisfy the first category only. The portfolio showcase and Apache-2.0 licensing improve repository reviewability and reuse clarity; they do not change the pilot or production boundary.

## Repository checkpoint readiness

- [x] package version is `0.5.2` in both project metadata and `ancova_ops.__version__`;
- [x] Python 3.11 and 3.12 CI coverage;
- [x] lint and unit tests;
- [x] smoke tests for every major CLI workflow;
- [x] one-command `ancova-showcase` reviewer workflow;
- [x] reproducible synthetic and hand-authored development data;
- [x] API quick start and command examples;
- [x] architecture documentation reflects Phases 0–4;
- [x] project status and evidence boundaries documented;
- [x] changelog added;
- [x] root Apache License 2.0 text and SPDX `Apache-2.0` package metadata;
- [x] synthetic/private-data governance boundary validated in CI;
- [x] adaptive-policy research remains separated from the operational route path;
- [x] sequence-model work remains explicitly deferred rather than implied to be complete.

### Licensing boundary

ANCOVA Ops project material distributed under the repository license is licensed under Apache-2.0. Third-party dependencies and any separately identified third-party material remain subject to their own licences and notices. A separate third-party notices file should be added when incorporated/adapted material creates an actual notice-preservation requirement; it is not created speculatively.

## Pilot readiness

The following remain intentionally incomplete:

- [ ] jurisdiction-specific privacy/legal review;
- [ ] documented operational purpose and lawful/data-use basis for each private field;
- [ ] notice and consent design where required;
- [ ] concrete retention and deletion schedule;
- [ ] pseudonymisation and identity-linkage design;
- [ ] authenticated staff identities and role-based access control;
- [ ] secure pilot storage and secrets management;
- [ ] approved procedure for data-subject/service-user deletion or correction requests;
- [ ] incident response and breach-handling process;
- [ ] external AI/model-provider data-processing review if private text leaves the controlled environment;
- [ ] real-data annotation and outcome-quality protocol;
- [ ] pilot monitoring and stop criteria.

**Pilot status: NOT READY / NOT APPROVED.**

## Production readiness

Production requires all pilot controls plus additional engineering and operational evidence:

- [ ] real-data routing benchmark with representative sampling;
- [ ] real-data outcome-analysis validation;
- [ ] prospective or otherwise defensible evaluation of adaptive-policy impact;
- [ ] deployment architecture and environment separation;
- [ ] authenticated API access and authorization;
- [ ] observability, monitoring and alerting;
- [ ] uptime, recovery and backup objectives;
- [ ] security testing and dependency-management process;
- [ ] policy activation runbook and rollback drill;
- [ ] explicit integration contract between the policy registry and `/v1/route`;
- [ ] human escalation and manual fallback procedure;
- [ ] model/rule change-control ownership;
- [ ] production data-retention and audit-retention controls;
- [ ] operational acceptance criteria approved by the service owner.

**Production status: NOT READY / NOT APPROVED.**

## Evidence claims allowed at v0.5.2

Acceptable wording:

> ANCOVA Ops v0.5.2 implements reproducible synthetic and hand-authored development workflows for explainable routing, outcome analysis, offline policy evaluation and longitudinal model comparison, with a one-command portfolio showcase. The repository is licensed under Apache-2.0.

Not acceptable without new evidence:

> ANCOVA Ops improves real service resolution time, routing accuracy or resident satisfaction.

> The adaptive policy is better than the baseline in production.

> The longitudinal model predicts real resident behaviour.

> ANCOVA proves a department or staff group causally performs better.

> The portfolio showcase is proof of production readiness.

> Apache-2.0 licensing makes the software production-ready or legally compliant for a private-data deployment.

## Go/no-go rule

The existence of working code, green CI, a polished showcase, an open-source license or promising synthetic metrics is **not** sufficient to move from repository checkpoint to private-data pilot or production deployment. Those transitions require separate governance and evidence decisions.
