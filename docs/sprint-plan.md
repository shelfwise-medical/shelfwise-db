# Sprint plan

Back to the [README](../README.md)

**Presentation: Thursday, 17 December 2026.** We meet every **Monday**; each sprint ends at the Monday meeting, where every member shows what they merged.

| Sprint | Dates | Goal |
|---|---|---|
| **Sprint 1** | Thu 26 Nov → **Mon 30 Nov** | Foundations: repo, schema v1, generator v1, definitions agreed |
| **Sprint 2** | Mon 30 Nov → **Mon 7 Dec** | It works: full data, integrity rules, the first query answers |
| **Sprint 3** | Mon 7 Dec → **Mon 14 Dec** | It is measured: benchmark, indexes, cold-chain incident, interface |
| **Final sprint** | Mon 14 Dec → **Thu 17 Dec** | Freeze, rehearse, present |

## Sprint 1: Foundations (Thu 26 Nov → Mon 30 Nov)

**Goal:** everyone can clone the repo and run something; the data model and the key definitions are agreed.

| Member | Deliverable by Monday 30 Nov |
|---|---|
| Leviscus | Repo rules active (`main` protected), issues and project board created, meeting notes template |
| Erick | `schema/schema.sql` v1 + ER diagram (Mermaid), reviewed by the team |
| Roberto | `uv` project set up; `generator/generate.py` v1 (small seeded dataset that loads into schema v1) |
| Anshpreet | Order lifecycle rules written down: allowed status transitions and what "allocated" means |
| Chengpu | Cold-chain rules written down: sensor reading format, excursion definition, quarantine and release |
| Smit | Precise definition of "safe available stock" + first draft of the first query on paper |
| Chanbopha | Benchmark plan: the two designs, what to measure, how many runs |
| Ian | Datasette runs on the database from the generator; list of the 3 to 5 views the demo needs |

**Monday 30 Nov meeting:** approve schema v1 (changes after this cost everyone time), approve the definitions, assign Sprint 2 issues.

## Sprint 2: It works (Mon 30 Nov → Mon 7 Dec)

**Goal:** the full dataset loads, the integrity rules hold, and the first query gives a correct answer.

| Member | Deliverable by Monday 7 Dec |
|---|---|
| Leviscus | Decision record started (one row per design decision, each with evidence); README "Rebuild everything" section |
| Erick | Schema v2 with all constraints (`CHECK`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `STRICT`); constraint tests with their exact errors |
| Roberto | Full dataset: ~120,000 stock movements, ~15,000 order lines, deliberate shortages, expiring batches, one cold-room excursion |
| Anshpreet | Triggers: no negative stock, only allowed status transitions; `UPSERT` against duplicated movements (double-run test) |
| Chengpu | Sensor ingest with `UPSERT`; excursion trigger that quarantines the batches in the affected room; audit trail trigger |
| Smit | First query working and verified by hand on a small case; `EXPLAIN QUERY PLAN` before indexes |
| Chanbopha | Both stock designs built (calculated from movements vs. stock table kept by a trigger); first timings |
| Ian | Datasette with the first query as a canned query; first draft of the demo flow |

## Sprint 3: It is measured (Mon 7 Dec → Mon 14 Dec)

**Goal:** every decision has a number behind it, and the story's incident can be replayed in the demo.

| Member | Deliverable by Monday 14 Dec |
|---|---|
| Leviscus | Decision record complete; reflections and evidence links checked; presentation outline |
| Erick | Final ER diagram matching the real schema; explanation of each normal form decision |
| Roberto | Concurrency test (several writers at once: how often `database is locked`?), which decides SQLite vs. PostgreSQL; nightly Parquet export |
| Anshpreet | FEFO picking query (first expired, first out); full lifecycle tested from created to shipped |
| Chengpu | Replay of the story's incident: excursion → quarantine → the picker cannot pick that batch; recall query (who received a batch) |
| Smit | Indexes chosen and justified with plans and timings (median of 5, interleaved) |
| Chanbopha | Final benchmark: read speed, write cost and storage of both designs; recommendation with numbers |
| Ian | Interface complete; demo script with timings; backup screenshots in case the live demo fails |

## Final sprint: Present (Mon 14 Dec → Thu 17 Dec)

| Day | What |
|---|---|
| Mon 14 Dec | **Feature freeze:** nothing new after this meeting, only fixes. Full rehearsal with a timer |
| Tue 15 Dec | Fix what the rehearsal showed; clean rebuild on a fresh clone to prove reproducibility |
| Wed 16 Dec | Second rehearsal; every member can explain their part and answer "how do you know?" |
| **Thu 17 Dec** | **Presentation** |

## Rules for every sprint

- Work goes through a **branch and a pull request**; you can merge your own pull request, no approval required.
- **Weekly review:** Roberto reviews all merged work before each Monday meeting.
- Each member's work is committed from **their own account**.
- A task is **done** only when it is merged, it runs from a fresh clone, and its evidence (output, plan, timing) is committed.
- If you are blocked, say so in the group chat **the same day**, not at the Monday meeting.
