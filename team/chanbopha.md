# Chanbopha Rin: Benchmark (our measured decision)

Back to the [README](../README.md) · [Sprint plan](../docs/sprint-plan.md)

**Your role:** you run the measurement that defends our main design decision. The professor grades decisions defended with numbers, so this is the evidence the presentation will lean on.

**The decision:** how do we know the current stock?
- **Design A, calculate:** sum all stock movements every time we ask (always correct, nothing duplicated, slower to read).
- **Design B, store:** keep a `stock` table that a trigger updates on every movement (instant to read, slower to write, duplicated data).

This is Module 5 (normalized vs. denormalized) and Module 4 (trigger cost) applied to our project.

**You work with:** Smit (his first query is what you time), Roberto (data volume), Anshpreet (the trigger in design B).

## Step 0: get set up (first day)

1. Accept the invitation to the **shelfwise-medical** organization on GitHub (check your email or github.com/notifications).
2. Clone the repo and create your branch:
   ```bash
   git clone https://github.com/shelfwise-medical/shelfwise-db.git
   cd shelfwise-db
   git switch -c chanbopha/sprint-1
   ```
3. Install [uv](https://docs.astral.sh/uv/) if you don't have it (same tool as in our portfolios).
4. **Your first commit:** tick the checkbox below in *this* file, commit it from your own account, push your branch and open a pull request. This proves your access works and starts your commit history.
   - [ ] I have read this file and the [sprint plan](../docs/sprint-plan.md), and I can push to the repo.
5. From now on: one branch per task and a pull request for every change. You can merge your own pull request once your work runs; Roberto reviews everyone's merged work every week before the Monday meeting.

## Sprint 1 tasks (due Monday 30 November)

Write `benchmark/plan.md` with:

1. **The two designs** in a few sentences each, and which tables each needs.
2. **What you will measure:** read time of the first query, write cost (time to insert 10,000 movements with and without the trigger), and storage (`dbstat`, as in Module 5).
3. **How you will measure:** warm-up run, at least 5 interleaved runs, median and min-max spread (as in Modules 5 and 6a).
4. **Your prediction:** which design wins at reading, which at writing, and by how much. Write it down **before** measuring; being wrong is a finding.

## Definition of done for Sprint 1

- `benchmark/plan.md` merged and agreed at the Monday meeting.
