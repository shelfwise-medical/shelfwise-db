# Leviscus Njeru: Coordination & documentation

Back to the [README](../README.md) · [Sprint plan](../docs/sprint-plan.md)

**Your role:** you keep the team moving and the evidence in one place. You make sure every decision has a reason and a number, and that anyone can rebuild the project from the repo.

**You work with:** everyone. You run the Monday meetings.

## Step 0: get set up (first day)

1. Accept the invitation to the **shelfwise-medical** organization on GitHub (check your email or github.com/notifications).
2. Clone the repo and create your branch:
   ```bash
   git clone https://github.com/shelfwise-medical/shelfwise-db.git
   cd shelfwise-db
   git switch -c leviscus/sprint-1
   ```
3. Install [uv](https://docs.astral.sh/uv/) if you don't have it (same tool as in our portfolios).
4. **Your first commit:** tick the checkbox below in *this* file, commit it from your own account, push your branch and open a pull request. This proves your access works and starts your commit history.
   - [ ] I have read this file and the [sprint plan](../docs/sprint-plan.md), and I can push to the repo.
5. From now on: one branch per task, a pull request for every change, and one approval from someone with a different role before merging.

## Sprint 1 tasks (due Monday 30 November)

1. **Protect `main`:** Settings → Rules → Rulesets (or Branches) → require a pull request with **1 approval** before merging, and block force pushes. You need to be an organization owner for this; ask Roberto to make you one.
2. **Issues and a project board:** create a GitHub Project (board view: To do / In progress / Review / Done). Create one issue per Sprint 1 task in the [sprint plan](../docs/sprint-plan.md) and assign it to its owner.
3. **Meeting notes:** create `docs/meetings/` with a template (date, who attended, what each person merged, decisions, blockers, next tasks), and write the notes of the 30 November meeting.
4. **Decision record skeleton:** create `docs/decision-record.md` with the columns *Decision | Options | Choice | Evidence | Cost accepted*. First row: "SQLite local-first vs. cloud vs. PostgreSQL" (see the README).

## Definition of done for Sprint 1

- `main` cannot be pushed to directly.
- Every Sprint 1 task has an issue with an owner.
- The 30 November meeting notes are merged.
