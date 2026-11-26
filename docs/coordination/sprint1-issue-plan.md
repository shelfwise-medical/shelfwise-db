# Sprint 1 — GitHub issue and board setup plan

**Sprint:** 26–30 November 2026 · **Project:** ShelfWise Medical  
[Project sprint plan](../sprint-plan.md) · [Team role files](../../team/leviscus.md)

**Status (verified 26 November 2026): LIVE.** The [public organization Sprint Tracker](https://github.com/orgs/shelfwise-medical/projects/1) has **eight issues (#7–#14)** attached, with **3 In Progress**, **5 Todo**, **0 Review**, and **0 Done**. Six accounts are assigned; the invitations for **@chengpuli-sketch (Chengpu)** and **@smitvekariyaa-code (Smit)** are pending as shown in the organization invitation screen. Their issues remain unassigned until eligible for assignment. These are evidence-based tracking statuses, not claims about unpushed local work. Project decisions and actual Sprint 1 acceptance remain open.

## Issue inventory for Monday 30 November

The repository has closed [#1 (uv setup)](https://github.com/shelfwise-medical/shelfwise-db/pull/1) and [#2 (generator design)](https://github.com/shelfwise-medical/shelfwise-db/pull/2) as **pull requests**, not standalone issues; these remain supporting evidence and are not duplicated. The following **eight tracking issues are now open**. Their acceptance criteria remain the source of truth, and their individual GitHub project status is updated when evidence changes:

| Live GitHub issue (status at setup) | Accountable person | Acceptance evidence / dependency |
| --- | --- | --- |
| [#7 — Sprint 1: coordination, GitHub workflow and decisions](https://github.com/shelfwise-medical/shelfwise-db/issues/7) (**In Progress**) | **Leviscus Njeru** | Confirm `main` protections with an org owner; track the board; merge `docs/decision-record.md` and meeting template; add actual 30 November notes after meeting |
| [#8 — Sprint 1: relational schema v1 and ER diagram](https://github.com/shelfwise-medical/shelfwise-db/issues/8) (**In Progress**) | **Erick Liebisch** | `schema/schema.sql`, Mermaid ER diagram, 3NF notes; reviewed for keys, lot/location relationships; share early with generator owner |
| [#9 — Sprint 1: seeded generator v1 and planted-case plan](https://github.com/shelfwise-medical/shelfwise-db/issues/9) (**In Progress**) | **Roberto Navia Guillen** | Small reproducible generator against schema v1; prints row counts and validates seeded output; **reference closed issues #1 and #2** |
| [#10 — Sprint 1: order lifecycle and allocation rules](https://github.com/shelfwise-medical/shelfwise-db/issues/10) (**Todo**) | **Anshpreet Singh** | `integrity/order-rules.md`; allowed/forbidden transitions, reservations, FEFO, duplicate movement key and negative stock options |
| [#11 — Sprint 1: cold-chain excursion and release rules](https://github.com/shelfwise-medical/shelfwise-db/issues/11) (**Todo**) | **Chengpu Li** | `integrity/cold-chain-rules.md`; reading key/units, threshold/duration, quarantine/release and audit semantics |
| [#12 — Sprint 1: safe available stock definition and first query](https://github.com/shelfwise-medical/shelfwise-db/issues/12) (**Todo**) | **Smit Vekariya** | `queries/definitions.md`, one hand-calculated lot-level example and initial `queries/first-query.sql`; clarify allocation double counting |
| [#13 — Sprint 1: stock-summary benchmark plan](https://github.com/shelfwise-medical/shelfwise-db/issues/13) (**Todo**) | **Chanbopha Rin** | `benchmark/plan.md`; two designs, read/write/storage measures, five interleaved runs and pre-measurement hypothesis |
| [#14 — Sprint 1: minimal Datasette interface and demo views](https://github.com/shelfwise-medical/shelfwise-db/issues/14) (**Todo**) | **Ian Okach** | `interface/README.md` with tested run command once generator merges; `interface/views.md` with 3–5 views and initial demo flow |

## Important dependencies and handoffs

- **Schema first:** Erick shares keys and relationships with Roberto, Smit, Anshpreet and Chengpu early. Avoid unnecessary schema churn after Monday.
- **Definition first:** Smit, Erick, Anshpreet and Chengpu agree how available stock, lot status and reservations interact *before* assuming the first query is correct.
- **First vertical slice:** do not postpone the interface until the last sprint. As soon as a small dataset loads, the query should be visible through Datasette.
- **Proof:** Each issue's acceptance criterion should link a merged PR, reproducible command/output, or a checked design document. Do not use planned row counts as measured project evidence.
- **Permissions:** Only an organization owner (or suitably authorized admin) can apply organization/repository protection rules. Ask the owner to configure `main` deletion and force-push restrictions, then test/verify via the UI.

## Board setup checklist

- [ ] Confirm project board owner and access for all eight members
- [x] Create [board #1](https://github.com/orgs/shelfwise-medical/projects/1) with **Todo / In Progress / Review / Done** (26 Nov)
- [x] Confirm #1 and #2 were earlier merged **PRs**; no duplicate tracking issues created
- [x] Create and add eight tracking issues [#7–#14](https://github.com/shelfwise-medical/shelfwise-db/issues) to the project; **six accounts assigned**. Assignment of Chengpu and Smit remains pending invitation acceptance (separate item below)
- [x] Place all eight issues on [the board](https://github.com/orgs/shelfwise-medical/projects/1) with status 3 In Progress / 5 Todo; the [issue bodies](https://github.com/shelfwise-medical/shelfwise-db/issues) state the 30 Nov deadline and dependencies
- [x] Verify active [Protect main ruleset #28158049](https://github.com/shelfwise-medical/shelfwise-db/settings/rules/28158049) for PR requirement, deletion and force-push protection; zero mandatory approvals
- [ ] Confirm Smit and Chengpu have accepted their organization invitations; assign [#12](https://github.com/shelfwise-medical/shelfwise-db/issues/12) and [#11](https://github.com/shelfwise-medical/shelfwise-db/issues/11) respectively (do not infer from pending invitations)
