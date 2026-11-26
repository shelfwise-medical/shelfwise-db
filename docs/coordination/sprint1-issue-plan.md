# Sprint 1 — GitHub issue and board setup plan

**Sprint:** 26–30 November 2026 · **Project:** ShelfWise Medical  
[Project sprint plan](../sprint-plan.md) · [Team role files](../../team/leviscus.md)

**Status:** Draft issue descriptions. **This document does not create GitHub issues, assign members or prove a project board exists.** Open the issues through GitHub after confirming each person's username; use one accountable issue owner and link dependencies. Board columns: **To do → In progress → Review → Done**.

## Issue inventory for Monday 30 November

The repository already has **closed #1** (uv project setup) and **closed #2** (generator design) as of the initial 26 November check; link these as evidence rather than creating duplicate issues. Open one Sprint 1 tracking issue for each workstream that still needs a merged deliverable:

| Proposed issue title | Accountable person | Acceptance evidence / dependency |
| --- | --- | --- |
| Sprint 1: coordination, GitHub workflow and decisions | **Leviscus Njeru** | Confirm `main` protections with an org owner; track the board; merge `docs/decision-record.md` and meeting template; add actual 30 November notes after meeting |
| Sprint 1: relational schema v1 and ER diagram | **Erick Liebisch** | `schema/schema.sql`, Mermaid ER diagram, 3NF notes; reviewed for keys, lot/location relationships; share early with generator owner |
| Sprint 1: seeded generator v1 and planted-case plan | **Roberto Navia Guillen** | Small reproducible generator against schema v1; prints row counts and validates seeded output; **reference closed issues #1 and #2** |
| Sprint 1: order lifecycle and allocation rules | **Anshpreet Singh** | `integrity/order-rules.md`; allowed/forbidden transitions, reservations, FEFO, duplicate movement key and negative stock options |
| Sprint 1: cold-chain excursion and release rules | **Chengpu Li** | `integrity/cold-chain-rules.md`; reading key/units, threshold/duration, quarantine/release and audit semantics |
| Sprint 1: safe available stock definition and first query | **Smit Vekariya** | `queries/definitions.md`, one hand-calculated lot-level example and initial `queries/first-query.sql`; clarify allocation double counting |
| Sprint 1: stock-summary benchmark plan | **Chanbopha Rin** | `benchmark/plan.md`; two designs, read/write/storage measures, five interleaved runs and pre-measurement hypothesis |
| Sprint 1: minimal Datasette interface and demo views | **Ian Okach** | `interface/README.md` with tested run command once generator merges; `interface/views.md` with 3–5 views and initial demo flow |

## Important dependencies and handoffs

- **Schema first:** Erick shares keys and relationships with Roberto, Smit, Anshpreet and Chengpu early. Avoid unnecessary schema churn after Monday.
- **Definition first:** Smit, Erick, Anshpreet and Chengpu agree how available stock, lot status and reservations interact *before* assuming the first query is correct.
- **First vertical slice:** do not postpone the interface until the last sprint. As soon as a small dataset loads, the query should be visible through Datasette.
- **Proof:** Each issue's acceptance criterion should link a merged PR, reproducible command/output, or a checked design document. Do not use planned row counts as measured project evidence.
- **Permissions:** Only an organization owner (or suitably authorized admin) can apply organization/repository protection rules. Ask the owner to configure `main` deletion and force-push restrictions, then test/verify via the UI.

## Board setup checklist

- [ ] Confirm project board owner and access for all eight members
- [ ] Create board with **To do / In progress / Review / Done**
- [ ] Check existing closed issues #1 and #2; avoid duplicates
- [ ] Open the eight tracking issues listed above and assign the actual GitHub usernames
- [ ] Place each issue in the board and add due date / dependencies
- [ ] Request and verify `main` branch ruleset from organization owner
- [ ] Record the board and issue URLs in the Sprint 1 meeting notes
