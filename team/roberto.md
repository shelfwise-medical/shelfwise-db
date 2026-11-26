# Roberto Navia Guillen: Data generator

Back to the [README](../README.md) · [Sprint plan](../docs/sprint-plan.md)

**Your role:** you produce the data everyone tests against. It must be **reproducible** (same seed, same data on every machine) and **interesting** (it has to contain the shortages, expiring batches and excursions the story is about).

**You work with:** Erick (your data must fit his schema), Smit (the first query must find your shortages), Chengpu (sensor readings and the excursion).

## Step 0: get set up (first day)

1. You created the **shelfwise-medical** organization, so you already have access.
2. Clone the repo and create your branch:
   ```bash
   git clone https://github.com/shelfwise-medical/shelfwise-db.git
   cd shelfwise-db
   git switch -c roberto/sprint-1
   ```
3. **Your first commit:** tick the checkbox below in *this* file, commit it from your own account, push your branch and open a pull request.
   - [ ] I have read this file and the [sprint plan](../docs/sprint-plan.md), and I can push to the repo.
4. From now on: one branch per task, a pull request for every change, and one approval from someone with a different role before merging.

## Sprint 1 tasks (due Monday 30 November)

1. **`uv` project:** run `uv init`, add the dependencies we will need (`datasette`, `duckdb`), commit `pyproject.toml`, `uv.lock` and a `.python-version` with 3.14. Merge this **first**, so everyone can run `uv sync`.
2. **`.gitignore` additions** (if not there yet): `*.db`, `*.db-wal`, `*.db-shm`, `*.parquet`, `generator/output/`.
3. **`generator/generate.py` v1:** a small seeded dataset (for example 20 products, 50 batches, 1,000 movements, 200 order lines) that loads into Erick's schema v1. Use `random.seed(42)` and `executemany` with `?` parameters.
4. **Design the "interesting" parts** (written down in `generator/README.md`, built in Sprint 2): which products will be short, which batches expire soon, when the cold-room excursion happens.

## Definition of done for Sprint 1

- `uv sync` works on a fresh clone.
- `uv run python generator/generate.py` builds `shelfwise.db` from `schema/schema.sql` and prints row counts per table.
- Running it twice gives the same row counts (reproducible).
