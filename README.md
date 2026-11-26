# ShelfWise Medical: Inventory, Cold Chain and Order Fulfilment

Final project for the **Databases** course at HSBI (Prof. Ulrich Norbisrath, winter semester 2026/27). **Presentation: Thursday, 17 December 2026.**

ShelfWise Medical is a **fictional** regional distribution warehouse for medical supplies. Every person and company in this project is invented.

## The story

**ShelfWise Medical** is a regional distribution warehouse in Bielefeld that supplies pharmacies, clinics and doctors' practices across Ostwestfalen-Lippe. About a third of its products are **cold-chain goods**: vaccines, insulin and biologics that must stay between **2 °C and 8 °C** from the moment they arrive until the moment they leave.

On a Saturday in March, the compressor of cold room 2 failed. The temperature climbed to 14 °C for six hours before anyone noticed. On Monday morning a picker shipped 40 packs of insulin from that room to a clinic, because the system still listed them as available. The quality manager, **Dr. Lena Hoffmann**, had to recall the whole batch, call every customer and report the incident to the authorities.

The inventory planner, **Jonas Weber**, has a second problem. His spreadsheet counts what is on the shelf, but not what is already reserved for other orders, what has expired, or what is in quarantine after a temperature excursion. Twice this quarter a hospital order could not be filled, and he only found out when the picker reported an empty shelf.

Their question to us: *"Can the database refuse to ship what is not safe to ship, and tell us what we are short of before an order fails?"*

Full story and cast: [docs/story.md](docs/story.md)

## The first query

> *"Which products have insufficient **safe available stock** to fulfil outstanding customer orders, and how much more is needed?"*
>
> **Working definition (under review in [Issue #12](https://github.com/shelfwise-medical/shelfwise-db/issues/12)):** determine eligible lot/location stock first, then subtract applicable active reservations without double-counting expired or quarantined units. The exact formula and worked example await the query/integrity owners.

## Architecture decision

**Local-first.** The operational database is **SQLite** on a machine inside the warehouse, so receiving, picking and the cold-room sensors keep working when the internet is down. A cold chain must never depend on a network connection: if the database were in the cloud, an outage would stop the temperature readings and the quarantine trigger at the same time.

A **nightly Parquet export** is **proposed** for historical reporting, if performance testing justifies it. A Parquet reporting snapshot is **not** a verified operational SQLite backup. A separate, consistent SQLite backup **and tested restore procedure** must be designed before recovery claims can be made. Neither export scheduling nor backup/restore has been demonstrated in this project yet.

We will **measure concurrent writes** (sensors, clerks, pickers). If `database is locked` happens too often, that is our measured reason to move the operational database to PostgreSQL on-premises.

## Team and roles

| Role | Member | Instructions |
|---|---|---|
| Coordination & documentation | Leviscus Njeru | [team/leviscus.md](team/leviscus.md) |
| Data model | Erick Liebisch | [team/erick.md](team/erick.md) |
| Data generator | Roberto Navia Guillen | [team/roberto.md](team/roberto.md) |
| Integrity & transactions: order lifecycle | Anshpreet Singh | [team/anshpreet.md](team/anshpreet.md) |
| Integrity & transactions: cold chain | Chengpu Li | [team/chengpu.md](team/chengpu.md) |
| Queries & indexes | Smit Vekariya | [team/smit.md](team/smit.md) |
| Benchmark (our measured decision) | Chanbopha Rin | [team/chanbopha.md](team/chanbopha.md) |
| Interface & demo | Ian Okach | [team/ian.md](team/ian.md) |

**Sprint plan:** [docs/sprint-plan.md](docs/sprint-plan.md) · **[Live Sprint Tracker](https://github.com/orgs/shelfwise-medical/projects/1)** · [Sprint 1 issues and evidence index](docs/coordination/sprint1-issue-plan.md)

## How we work

- **Everyone commits their own work** from their own GitHub account. The commit history is part of our evidence of who did what.
- **Work on a branch, merge with a pull request.** Use a branch per task (`<your-name>/<task>`, e.g. `roberto/generator`) and open a pull request; you can merge it yourself once your work runs. No approval is required.
- **Weekly review:** Roberto reviews everyone's merged work every week before the Monday meeting and raises problems there or in the pull request.
- **Small, clear commits** with messages that say what changed.
- **Never commit databases, generated data or secrets** (`*.db`, `*.csv` outputs, `*.parquet`, `.env`). Commit only the scripts that build them; anyone must be able to rebuild everything from the repo.
- **Every claim needs evidence:** a script, its output, a query plan or a measurement.

## Repository layout

```
shelfwise-db/
├── README.md
├── docs/          ← story, sprint plan, decision record, meeting notes (Leviscus)
├── team/          ← one instruction file per team member
├── schema/        ← tables, constraints, ER diagram (Erick)
├── generator/     ← seeded data generator (Roberto)
├── integrity/     ← triggers, UPSERT, order lifecycle, cold chain (Anshpreet, Chengpu)
├── queries/       ← first query, indexes, query plans (Smit)
├── benchmark/     ← calculated vs. stored stock (Chanbopha)
└── interface/     ← Datasette setup and demo (Ian)
```

## Rebuild everything

_Filled in during Sprint 2, once the schema and the generator exist._
