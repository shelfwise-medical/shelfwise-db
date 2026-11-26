# ShelfWise Medical — Engineering decision record

[Project home](../README.md) · [Project story](story.md) · [Sprint plan](sprint-plan.md)

**Purpose:** Make the design choices for the final database project inspectable and revisable. Record evidence from *this project* as it becomes available; do not substitute benchmark numbers from individual portfolios for project results.

**Status:** Initial skeleton for Sprint 1 (26–30 November 2026). **Choices are proposed, not yet approved by the team.** The team should confirm or amend them at its 30 November review.

| Decision | Options | Choice | Evidence | Cost accepted |
| --- | --- | --- | --- | --- |
| Operational database location and engine | Local SQLite; cloud database; on-premises PostgreSQL | **Proposed:** one local SQLite file on the warehouse machine | [Story and offline requirement](story.md); [team architecture starting point](../README.md). **Project concurrency, load and recovery tests pending.** Prior module tests are background only. | Single-machine availability, backup/recovery design, coordination of concurrent writers and local security controls |
| What constitutes safe available stock? | Raw on-hand count; on-hand minus exclusions and prior reservations; lot-by-lot eligibility | **To decide with Smit, Erick, Anshpreet and Chengpu:** exclude expired/quarantined lots and quantities already reserved, without double-counting overlapping exclusions | [Story's stock requirement](story.md); planned [worked example and first query](../team/smit.md). **No tested result yet.** | More complex lot-level accounting and reservation state changes |
| How to handle cold-room excursions? | Alert only; automatically quarantine affected lots until documented release | **Proposed:** quarantine affected lots and reject allocation/picking while quarantined; approval and precise excursion threshold TBD | [Incident story](story.md); planned [Chengpu rules](../team/chengpu.md). **No tested trigger yet.** | False positives, audit/release workflow, validation and recovery effort |
| Historical reporting and backups | Report directly on operational file; scheduled snapshot/export; remote operational DB | **Proposed:** report export (Parquet/DuckDB) only if workload justifies it; independent backup/recovery procedure required | [Sprint 3 plan](sprint-plan.md). **Export/backup not implemented or measured.** | Stale snapshots, refresh validation and monitoring; reporting export is not a backup by itself |

## How to add or change a decision

1. Name the decision, alternatives and the person proposing it.
2. Link a **project** issue, PR, code/test output, query plan or measured timing; if none exists, label the claim **proposal**.
3. State the failure mode or cost the team accepts, not only the benefit.
4. Record the team review date and whether the decision was approved, revised or rejected.
5. When superseded, keep a short dated note; do not silently overwrite the reasoning.

## Sprint 1 review (30 November 2026) — awaiting meeting

- **Attendees and approval:** not yet recorded
- **Decisions revised or accepted:** not yet recorded
- **Evidence / merged PR links:** to be added after the work is merged
