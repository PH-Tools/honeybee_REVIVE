---
DATE: 2026-07-15
STATUS: CANONICAL
---

# honeybee-REVIVE — Tech Stack

## Runtime

- **IronPython 2.7** for the model-extension code (loaded into Rhino via `honeybee_grasshopper_REVIVE`; `# -*- Python Version: 2.7 -*-` headers).
- **CPython ≥ 3.10** for the analysis/reporting code (pandas) and for tests/CI.

## Dependencies

Runtime (`pyproject.toml`): `honeybee-energy`, `pandas`, `ph-units`, and the ADORB calc via **PH-ADORB**. `pandas` is used only in the CPython-only paths (`honeybee_revive/output/`, dev scripts) — see `CODING_STANDARDS.md`.

Dev extras: `pytest`, `coverage`, etc.

## Packaging

- setuptools + wheel; five packages (`honeybee_revive`, `honeybee_energy_revive`, `honeybee_revive_standards`, `honeybee_revive_measures`, `ladybug_revive`). `honeybee_revive_standards` ships JSON via package-data. Published to PyPI as **`honeybee-REVIVE`**.

## Testing

- **pytest** — `python -m pytest`. Coverage via `coverage` (HTML → `_coverage_html/`). Tests mirror the packages (`test_honeybee_revive/`, `test_ladybug_revive/`, …).

## Formatting

- **Black** + **ruff** (line length 120), per the PH-Tools convention.

## Versioning & release

- Version in `pyproject.toml` `[project] version`. GitHub-Release-driven build/deploy via `.github/workflows/ci.yml`; `.github/workflows/notify-hub.yml` triggers a ph-docs rebuild.

## Docs

- `docs/` is a **spoke** in the ph-docs Astro hub (`index.md`, `nav.yml`, `getting-started.md`, `packages.md`). `nav.yml` already references a planned `api/` tree that does not yet exist on disk (generated at build time; see `context/AUTODOC.md`). Do not restructure `docs/`. See `docs/.instructions.md`.
