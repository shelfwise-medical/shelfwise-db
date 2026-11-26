# Schema v1: design notes

Back to the [README](../README.md) · [`schema.sql`](schema.sql) · [ER diagram](er-diagram.md)

## Decisions

| # | Decision | Why |
|---|---|---|
| 1 | **The expiry date and the quality status live on `batch`, not on `product`.** | A product is fixed in the catalogue, but every delivery lot has its own expiry date. Two lots of the same insulin can expire on different days, and only the lot that was in cold room 2 must be quarantined. |
| 2 | **The location lives on `stock_movement`, not on `batch`.** (Answers Roberto's open question 1.) | A lot can be split between rooms: 100 boxes arrive in cold room 2 and 30 are later moved to cold room 1. With `batch.location_id` the lot would be "all here or all there", and after an excursion in room 2 we could not tell that 70 boxes were affected and 30 were safe. A move is two rows: `-30` in room 2, `+30` in room 1 (`kind = 'transfer'`). Tested: `SUM(qty)` per location gives 70 and 30. |
| 3 | **The supplier lives on `batch`, not on `product`.** | The same product can come from different suppliers. Each lot records who delivered it, so a supplier recall targets exactly those lots. |
| 4 | **Stock is not stored; it is calculated from `stock_movement`.** | Every change is a new row that is never edited (audit trail for medical distribution). Stock on hand = `SUM(qty)`. Whether to also keep a stored stock table is Chanbopha's benchmark question. |
| 5 | **Natural keys against duplicates:** `stock_movement.source_ref` (UNIQUE) and `sensor_reading (location_id, ts)` (PRIMARY KEY). | A re-sent delivery or sensor reading is absorbed by `UPSERT` instead of counted twice (as in Module 4). |
| 6 | **`order_line` and `allocation` are bridge tables** for the two m:n relationships. | See the [ER diagram](er-diagram.md). `allocation` points to its order line with a composite foreign key `(order_id, product_id)`. |
| 7 | **Temperature limits live on `product`; readings live on `sensor_reading` per room.** | The rule (2 to 8 °C) belongs to the product; the measurement belongs to the room, not to each box. |

## Why this is in 3NF

- **1NF:** every column holds one value (no lists, no "box 1, box 2" columns).
- **2NF:** in the tables with a composite key (`order_line`, `allocation`, `sensor_reading`) every non-key column depends on the **whole** key. Example: `allocation.qty` needs the order, the product **and** the batch.
- **3NF:** no non-key column depends on another non-key column. Example: the product name is not copied into `batch` or `order_line`; they store `product_id` and join to `product`. The expiry date is not copied into `stock_movement`; it is reached through `batch_id`.

## Still open (to agree on Monday 30 Nov)

1. **Audit trail table** for batch status changes (old value, new value, who, when): Chengpu defines the content; I add the table in v2.
2. **Cancelled orders:** `cancelled` is in the status list; from which states it is allowed is Anshpreet's rule (trigger in Sprint 2).
3. **Who did it:** do movements and status changes need a `user` column (receiving clerk, picker, quality manager)?
4. **Order lines vs. order dates:** is `created_at` on the order enough, or do we need a requested delivery date for "outstanding" orders (Smit's definition)?
5. **Remaining constraints** (`CHECK min_temp_c < max_temp_c`, date formats, no negative stock) come in schema v2 with tests for each exact error.
