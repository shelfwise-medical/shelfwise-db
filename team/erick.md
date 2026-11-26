# Erick Liebisch: Data model

Back to the [README](../README.md) · [Sprint plan](../docs/sprint-plan.md)

**Your role:** you design the tables everyone else builds on. Because every other role depends on the schema, Sprint 1 is the most important sprint for you.

**You work with:** Roberto (the generator fills your tables), Anshpreet and Chengpu (their triggers run on your tables), Smit (the first query reads them).

## Step 0: get set up (first day)

1. Accept the invitation to the **shelfwise-medical** organization on GitHub (check your email or github.com/notifications).
2. Clone the repo and create your branch:
   ```bash
   git clone https://github.com/shelfwise-medical/shelfwise-db.git
   cd shelfwise-db
   git switch -c erick/sprint-1
   ```
3. Install [uv](https://docs.astral.sh/uv/) if you don't have it (same tool as in our portfolios).
4. **Your first commit:** tick the checkbox below in *this* file, commit it from your own account, push your branch and open a pull request. This proves your access works and starts your commit history.
   - [ ] I have read this file and the [sprint plan](../docs/sprint-plan.md), and I can push to the repo.
5. From now on: one branch per task, a pull request for every change, and one approval from someone with a different role before merging.

## Sprint 1 tasks (due Monday 30 November)

1. **Schema v1** in `schema/schema.sql`, with `STRICT` tables, primary keys and foreign keys. A starting point to discuss (change it if you find something better):

   | Table | Purpose | Key columns |
   |---|---|---|
   | `product` | What we sell | `product_id`, `name`, `cold_chain` (0/1), `min_temp_c`, `max_temp_c` |
   | `supplier` | Who delivers | `supplier_id`, `name` |
   | `location` | Where stock is stored | `location_id`, `name`, `is_cold_room` (0/1) |
   | `batch` | One delivery lot of a product | `batch_id`, `product_id`, `lot_no`, `expiry_date`, `status` (`released` / `quarantined` / `destroyed`) |
   | `stock_movement` | Every stock change (receipt, pick, adjustment) | `movement_id`, `batch_id`, `location_id`, `qty`, `kind`, `ts`, `source_ref` (natural key against duplicates) |
   | `customer` | Pharmacies, clinics | `customer_id`, `name` |
   | `customer_order` | An order and its status | `order_id`, `customer_id`, `status`, `created_at` |
   | `order_line` | A product in an order | `order_id`, `product_id`, `qty` |
   | `allocation` | Stock of a batch reserved for an order line | `order_id`, `product_id`, `batch_id`, `qty` |
   | `sensor_reading` | Cold room temperatures | `location_id`, `ts`, `temp_c` |

2. **ER diagram** in Mermaid (`schema/er-diagram.md`), with the cardinalities (1:n, m:n).
3. **Short notes** (`schema/notes.md`): which design choices keep the schema in 3NF, and what is still open.
4. Share it in the group chat **by Saturday**, so Roberto can start the generator against it.

## Definition of done for Sprint 1

- `sqlite3 shelfwise.db ".read schema/schema.sql"` runs without errors on a fresh database.
- The team approves schema v1 at the Monday meeting.
