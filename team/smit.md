# Smit Vekariya: Queries & indexes

Back to the [README](../README.md) · [Sprint plan](../docs/sprint-plan.md)

**Your role:** you own the project's **first query**, the one the whole story is about, and you make it fast with indexes you can justify with query plans and timings.

**You work with:** Erick (tables), Roberto (the data must contain shortages for your query to find), Chanbopha (your query is what the benchmark times), Ian (it becomes the main view in Datasette).

## Step 0: get set up (first day)

1. Accept the invitation to the **shelfwise-medical** organization on GitHub (check your email or github.com/notifications).
2. Clone the repo and create your branch:
   ```bash
   git clone https://github.com/shelfwise-medical/shelfwise-db.git
   cd shelfwise-db
   git switch -c smit/sprint-1
   ```
3. Install [uv](https://docs.astral.sh/uv/) if you don't have it (same tool as in our portfolios).
4. **Your first commit:** tick the checkbox below in *this* file, commit it from your own account, push your branch and open a pull request. This proves your access works and starts your commit history.
   - [ ] I have read this file and the [sprint plan](../docs/sprint-plan.md), and I can push to the repo.
5. From now on: one branch per task, a pull request for every change, and one approval from someone with a different role before merging.

## Sprint 1 tasks (due Monday 30 November)

1. **Define "safe available stock" precisely** in `queries/definitions.md`:
   > safe available stock = on hand − allocated to other orders − quarantined − expired

   For each term, say which table and which condition it comes from (e.g. "expired = `batch.expiry_date` < today"). Which orders count as *outstanding* (which statuses)?
2. **A worked example by hand:** 1 product, 3 batches (one expired, one quarantined, one fine), 2 orders. Compute the shortage on paper. In Sprint 2 the query must give the same number.
3. **First draft of the first query** in `queries/first-query.sql`: it does not need to run yet; it shows the joins and the shortage calculation.
4. Check with Erick that schema v1 has everything your definition needs.

## Definition of done for Sprint 1

- `queries/definitions.md` and the worked example merged and agreed at the Monday meeting.
- The first-query draft is in the repo.
