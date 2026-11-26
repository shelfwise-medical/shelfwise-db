# Data generator: design

Back to the [README](../README.md) · Owner: Roberto Navia Guillen · [My instructions](../team/roberto.md)

The generator builds `shelfwise.db` from `schema/schema.sql` and fills it with a **reproducible** dataset (`random.seed(42)`: the same data on every machine). This file is the design; the script follows once schema v1 is merged.

The data has to be **interesting**: if every product had enough stock, nothing expired and no fridge ever failed, the first query would return nothing and the triggers would never fire. So the shortages, expiring batches and the excursion below are planted on purpose, and each one is something a teammate's work must find.

## Time window

One quarter: **1 January to 31 March 2026**. "Today" for queries about expiry and outstanding orders is **Monday 16 March 2026, 08:00**, the morning after the story's incident.

## Volumes

| Table | v1 (Sprint 1, small test) | Full (Sprint 2) |
|---|---|---|
| `product` | 20 | 200 (about one third cold chain) |
| `supplier` | 3 | 15 |
| `location` | 4 (3 ambient zones + cold room 2) | 8 (5 ambient zones, cold rooms 1 to 3) |
| `batch` | 50 | ~1,500 |
| `stock_movement` | 1,000 | **~120,000** |
| `customer` | 10 | 120 (pharmacies, clinics, practices) |
| `customer_order` | 50 | ~3,000 |
| `order_line` | 200 | **~15,000** |
| `sensor_reading` | one day, cold room 2 | every 5 minutes per cold room for the quarter (~78,000) |

## The planted cases

Each case has an owner who must be able to find it with their work.

| # | Case | How it is generated | Who must find it |
|---|---|---|---|
| 1 | **Shortages** | About 5% of products get less stock than their outstanding orders need; 3 of them are cold-chain products | Smit: the first query lists exactly these products and the missing quantity |
| 2 | **Hidden shortage** | A product with enough stock **on the shelf** that is still short once allocations, quarantine and expiry are subtracted | Smit: proves the query uses *safe available stock*, not shelf stock |
| 3 | **Expired with stock left** | ~20 batches expired before 16 March but still have stock | Smit (excluded from available stock), Anshpreet (never allocated) |
| 4 | **Expiring soon** | ~30 batches expire within 30 days of 16 March | Anshpreet: FEFO picks these first |
| 5 | **The cold-room excursion** | Cold room 2, **Saturday 14 March 2026, 02:00 to 08:00**: readings rise from 5 °C to a peak of **14 °C**, then return to normal. All other readings stay between 3 and 7 °C | Chengpu: the trigger quarantines every batch in cold room 2 |
| 6 | **The Monday insulin order** | Monday 16 March: a clinic orders 40 packs of insulin, and the only insulin batch is in cold room 2 | Chengpu and Anshpreet: the database must refuse to allocate or pick it |
| 7 | **Replayed movements** | ~1% of deliveries are sent twice with the same `source_ref` (as after a network retry) | Anshpreet: `UPSERT` absorbs them, so stock is not counted twice |
| 8 | **Replayed sensor readings** | Some readings re-sent with the same `(location_id, ts)` | Chengpu: no duplicate readings |

## Rules the generator follows

- Only the seed decides the data: no `datetime.now()`, no unseeded randomness.
- `executemany` with `?` parameters (never string formatting), one transaction per table.
- The script prints the row count of every table and the number of rows per planted case, so anyone can check the data in one look.
- The output database is never committed (`*.db` is in `.gitignore`); only the script is.

## Open questions for the Monday meeting

1. Erick: does schema v1 have a `source_ref` (or similar) on `stock_movement`, and a `location_id` on `batch` or on the movement, so we know which batches were in cold room 2?
2. Chengpu: is one reading above 8 °C already an excursion, or only after a minimum duration? The planted excursion lasts 6 hours, so both definitions catch it.
3. Smit: is "today" fixed (16 March 2026) in the queries, or a parameter? A fixed date keeps the results reproducible.
