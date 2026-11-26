# Ian Okach: Interface & demo

Back to the [README](../README.md) · [Sprint plan](../docs/sprint-plan.md)

**Your role:** you make the project visible. On 17 December the professor will see our work through your interface and your demo, so you decide what the story looks like on screen.

**You work with:** Smit (the first query becomes the main view), Chengpu (the incident replay), Leviscus (the presentation outline).

## Step 0: get set up (first day)

1. Accept the invitation to the **shelfwise-medical** organization on GitHub (check your email or github.com/notifications).
2. Clone the repo and create your branch:
   ```bash
   git clone https://github.com/shelfwise-medical/shelfwise-db.git
   cd shelfwise-db
   git switch -c ian/sprint-1
   ```
3. Install [uv](https://docs.astral.sh/uv/) if you don't have it (same tool as in our portfolios).
4. **Your first commit:** tick the checkbox below in *this* file, commit it from your own account, push your branch and open a pull request. This proves your access works and starts your commit history.
   - [ ] I have read this file and the [sprint plan](../docs/sprint-plan.md), and I can push to the repo.
5. From now on: one branch per task, a pull request for every change, and one approval from someone with a different role before merging.

## Sprint 1 tasks (due Monday 30 November)

1. **Datasette runs:** once Roberto's generator v1 is merged, run `uv run datasette shelfwise.db` and check that every table opens. Write the exact commands in `interface/README.md`.
2. **Plan the views** in `interface/views.md`: the 3 to 5 screens the demo needs, one per person in the story. For example: Jonas's shortage list (the first query), Dr. Hoffmann's quarantined batches, the picker's FEFO pick list, the excursion timeline of cold room 2.
3. **Demo outline v0** (in the same file): the order in which we tell the story in about 15 minutes.

## Definition of done for Sprint 1

- `interface/README.md` with the commands to start Datasette, tested on your machine.
- `interface/views.md` merged and agreed at the Monday meeting.
