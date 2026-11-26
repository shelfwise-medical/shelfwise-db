# Anshpreet Singh: Integrity & transactions (order lifecycle)

Back to the [README](../README.md) · [Sprint plan](../docs/sprint-plan.md)

**Your role:** you make the database refuse impossible orders and stock: no negative stock, no skipped order states, no duplicated movements. You share the integrity work with Chengpu, who handles the cold chain.

**You work with:** Erick (your rules run on his tables), Chengpu (the same trigger style), Smit (allocations feed the first query).

## Step 0: get set up (first day)

1. Accept the invitation to the **shelfwise-medical** organization on GitHub (check your email or github.com/notifications).
2. Clone the repo and create your branch:
   ```bash
   git clone https://github.com/shelfwise-medical/shelfwise-db.git
   cd shelfwise-db
   git switch -c anshpreet/sprint-1
   ```
3. Install [uv](https://docs.astral.sh/uv/) if you don't have it (same tool as in our portfolios).
4. **Your first commit:** tick the checkbox below in *this* file, commit it from your own account, push your branch and open a pull request. This proves your access works and starts your commit history.
   - [ ] I have read this file and the [sprint plan](../docs/sprint-plan.md), and I can push to the repo.
5. From now on: one branch per task and a pull request for every change. You can merge your own pull request once your work runs; Roberto reviews everyone's merged work every week before the Monday meeting.

## Sprint 1 tasks (due Monday 30 November)

Sprint 1 is about **rules on paper**, so the schema can support them. Write `integrity/order-rules.md` with:

1. **The allowed status transitions:** `created → allocated → picked → packed → shipped`. Which jumps are forbidden (e.g. `created → shipped`)? Can an order be cancelled, and from which states?
2. **What "allocated" means:** stock from specific batches is reserved for an order line. Which batches may be allocated (released, not expired), and in which order (FEFO: first expired, first out)?
3. **Negative stock:** how will we stop it? A `CHECK` on a stock table, or a `BEFORE INSERT` trigger on `stock_movement` that rejects a pick larger than what is there? Write down both options and their trade-off.
4. **Duplicated movements:** which natural key identifies one movement (for example `source_ref`), so a re-sent delivery is absorbed by `UPSERT` instead of counted twice (as in Module 4)?
5. Give Erick any column these rules need **by Saturday**.

## Definition of done for Sprint 1

- `integrity/order-rules.md` merged and agreed at the Monday meeting.
- Erick's schema v1 has the columns your rules need.
