# context/ — canonical repo documentation

Stable, ground-truth documentation for honeybee-REVIVE. Distinct from `planning/` (in-flight work) and `docs/` (the public site published by the ph-docs hub).

`CLAUDE.md` at the repo root is the dispatcher; this folder holds the docs it routes to.

## Index

| Doc | Read when you need… |
|-----|---------------------|
| [`PRD.md`](PRD.md) | What honeybee-REVIVE is for and what belongs here |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | The five packages, the `_extend`/`properties` pattern, the ADORB flow |
| [`TECH_STACK.md`](TECH_STACK.md) | Runtime split, deps, packaging, testing, CI, release |
| [`CODING_STANDARDS.md`](CODING_STANDARDS.md) | The IPy2.7 vs CPython boundary, serialization, testing |
| [`AUTODOC.md`](AUTODOC.md) | Feature spec for the automated API-doc generator feeding ph-docs |

## Maintenance rule

When a change alters the object model, serialization, or the IPy2.7/CPython boundary, fold it into the relevant doc here. Keep it true.
