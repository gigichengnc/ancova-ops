# Release Readiness — ReasonedOps v1.4.3 audit close-out

ReasonedOps v1.4.3 is the final v1 **audit-correction and artifact-alignment checkpoint**. It does not add production capability; it closes issues found after the earlier publication checkpoint.

## Why v1.4.3 exists

An external review identified four issues worth correcting before freezing v1:

1. one current-facing storefront document still used external-rebuild wording;
2. reviewer-facing `request intelligence` wording could imply more NLP/ML sophistication than the deterministic rule/keyword Operate baseline actually uses;
3. the validity suite did not execute an unmeasured-confounding false-negative scenario;
4. the preferred citable Zenodo snapshot and the publicly installable PyPI snapshot had different version numbers.

The first three are now corrected on the v1.4.3 release candidate. The fourth is closed by publishing the exact same `v1.4.3` tag across GitHub, Zenodo and PyPI.

## Software / evidence readiness

- [x] `reasoned_ops` is the single canonical package namespace.
- [x] public CLI commands use the `reasoned-` prefix.
- [x] FastAPI request intake and deterministic explainable routing work locally.
- [x] Operate is explicitly documented as a **rule-based deterministic baseline**, not a trained NLP model.
- [x] human confirm / override history preserves the original machine/rule decision.
- [x] outcomes are stored separately from routing decisions.
- [x] department × case-type overlap and identifiability are checked before adjusted ranking.
- [x] unsupported observed comparisons can be withheld.
- [x] method applicability returns `use`, `caution`, `reject` or `recommend_alternative`.
- [x] `reasoned-validity-v2` covers known-effect recovery, measured confounding, no-overlap refusal and slope-interaction detection.
- [x] `reasoned-validity-v2` also includes `unmeasured_confounding_blind_spot` as a **known limitation** scenario.
- [x] Python 3.11 / 3.12 CI covers lint, tests and major CLI workflows.
- [x] distribution CI builds wheel + sdist and installs the wheel in a clean environment.
- [x] Apache-2.0 licensing and `CITATION.cff` are present.
- [x] current-facing project-origin wording describes one project evolving from the author's HKMU Hackathon 2026 participation.
- [x] Zenodo GitHub integration is enabled.

## Hidden-confounding benchmark boundary

The new limitation scenario deliberately generates a true latent case-burden variable, lets it affect both routing and outcome, then removes it before the ordinary Evaluate pipeline sees the data.

Expected behaviour:

```text
observed overlap = supported
      ↓
gate disposition = use
      ↓
adjusted contrast = badly biased / sign reversed
      ↓
interpretation boundary still says unmeasured confounding is not ruled out
```

`PASS` means the benchmark successfully reproduces and discloses this false-negative mode. It does **not** mean ReasonedOps can detect an unrecorded confounder.

## Publication / provenance readiness

Historical state:

```text
PyPI reasoned-ops==1.4.0     published + externally exercised
Zenodo v1.4.1                10.5281/zenodo.22044222
Zenodo v1.4.2                10.5281/zenodo.22044621
```

Final target:

```text
Git tag v1.4.3
      = GitHub Release v1.4.3
      = Zenodo v1.4.3 archived snapshot
      = PyPI reasoned-ops==1.4.3
```

The v1.4.3 release-candidate `CITATION.cff` intentionally has **no top-level DOI**. The old v1.4.2 DOI must not be copied into a new snapshot. Zenodo can only mint the immutable v1.4.3 version DOI after ingesting the GitHub release.

## Final release checklist

### Before merge

- [x] package metadata set to `1.4.3`;
- [x] runtime `__version__` set to `1.4.3`;
- [x] `CITATION.cff` set to `1.4.3` without a speculative DOI;
- [x] PyPI description tightened to rule-based Operate + hidden-confounding limitation boundaries;
- [x] README describes the v1.4.3 audit-closeout provenance plan;
- [x] release/citation/status docs describe exact-tag alignment;
- [x] `CHANGELOG.md` includes a `1.4.3` section;
- [ ] PR CI passes Python 3.11, Python 3.12 and distribution jobs.

### After merge to main

- [ ] main CI passes;
- [ ] release workflow creates **GitHub Release v1.4.3** from the exact successful main commit;
- [ ] confirm the release tag points to the intended v1.4.3 commit.

### Zenodo

- [ ] verify Zenodo ingests **v1.4.3**;
- [ ] verify title = ReasonedOps;
- [ ] verify creator = Gigi Cheng;
- [ ] verify version = v1.4.3;
- [ ] verify license = Apache-2.0;
- [ ] record the exact immutable **v1.4.3 version DOI**;
- [ ] if Zenodo separately displays **Cite all versions / concept DOI**, record it independently rather than inferring it from a version DOI.

### Post-release DOI sync

- [ ] add the verified v1.4.3 version DOI to current citation documentation / `CITATION.cff` on `main`;
- [ ] use a verified concept DOI for a stable README project badge only if it is actually observed;
- [ ] do **not** bump the software version merely to sync an already minted DOI.

The release workflow is idempotent when `v1.4.3` already exists, so a later documentation-only DOI sync should not create another release.

### PyPI exact-tag publication

- [ ] manually run **Publish to PyPI** with input tag exactly `v1.4.3`;
- [ ] verify PyPI shows `reasoned-ops==1.4.3`;
- [ ] install `reasoned-ops==1.4.3` in a fresh environment;
- [ ] verify `reasoned_ops.__version__ == "1.4.3"`;
- [ ] run `reasoned-validity --n 1200 --seed 23 --json` and confirm all five scenario names are present;
- [ ] repeat a small routing/API smoke check;
- [ ] update `publication-verification.md` with observed v1.4.3 results.

## What is not ready

### Real private-data pilot

A real pilot still requires jurisdiction-specific privacy/legal review, purpose/data-use documentation, secure authenticated access, retention/deletion procedures, incident handling, representative data quality checks and predefined pilot stop criteria.

**Pilot status: NOT READY / NOT APPROVED.**

### Production deployment

Production additionally requires deployment architecture, authentication/RBAC, monitoring, backup/recovery, security testing, operational change control and representative real-world validation.

**Production status: NOT READY / NOT APPROVED.**

## Claims supported after this release candidate

Supported:

> ReasonedOps is a runnable research/software prototype that originated from the author's participation in HKMU Hackathon 2026 and evolved into Operate → Audit → Evaluate.

> Operate currently uses a transparent deterministic rule-based baseline, not a trained NLP model.

> Evaluate can refuse some unsupported comparisons visible in the observed design, and its validity benchmark also demonstrates a known unmeasured-confounding failure mode that ordinary observed-data checks cannot detect.

Not supported:

> ReasonedOps has ruled out hidden confounding.

> ReasonedOps improves real service outcomes.

> ReasonedOps is approved for real private data or production use.

## Freeze condition

ReasonedOps v1 should be considered fully frozen when:

```text
v1.4.3 GitHub release archived by Zenodo
      +
verified DOI metadata synced
      +
PyPI 1.4.3 published from exact tag
      +
fresh-environment 1.4.3 verification completed
```

Further substantive work should require a real partner, representative dataset, competition requirement or new evidence question.
