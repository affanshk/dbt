# dbt-modular-warehouse

This repository is a scaffold for a modular dbt-based data warehouse project designed as a portfolio project.

Key conventions
- Layers: bronze -> silver -> gold
  - bronze: raw ingestion (seeds/external sources)
  - silver: cleaned, standardized tables. Only cleaning is allowed in silver. Table-level DQ is required (dbt tests + Great Expectations optional suites).
  - gold: transformations, aggregations, business logic. Complex transforms (aggregations, windows, wide joins) are only permitted in gold.
- Enforcement: a CI check enforces that complex transformations are not present outside models/gold/.
- Adapter support: Postgres and DuckDB included by default. Easily add adapters (Snowflake, BigQuery, Redshift, Databricks) via profiles and requirements.

What is included
- dbt_project.yml and a profiles example for Postgres + DuckDB
- config/ for declaring sources and DQ rules
- scripts/ to generate models from config and to enforce repo structure
- macros/ with helper macros
- example models for silver and gold
- Great Expectations integration stub under dq/
- GitHub Actions CI workflow to run structure checks, dbt compile & tests, and optional GE checks

Next steps
- Update config/sources_config.yml with your real sources and tables.
- Run `python3 scripts/generate_models.py` to create templated models for all sources/tables.
- Populate `profiles.yml` locally (see profiles.example.yml) with credentials for Postgres or DuckDB and run dbt.
- Optionally `great_expectations init` and create expectation suites for silver tables, then configure CI to run them.
