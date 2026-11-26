# Data generator: design

Back to the [README](../README.md) · Owner: Roberto Navia Guillen · [My instructions](../team/roberto.md)

The generator builds `shelfwise.db` from `schema/schema.sql` and fills it with a **reproducible** dataset (`random.seed(42)`: the same data on every machine).

## Run it

From the repo root:

```bash
uv run python generator/generate.py          # small test dataset (about 1 second)
uv run python generator/generate.py --full   # full dataset (about 3 seconds, ~14 MB)
```

It prints the rows per table, the expected result of every planted case, and two checks: no batch has negative stock, and the products that are short in an independent SQL query are exactly the planted ones. Sample output of the small dataset: [sample-output-small.txt](sample-output-small.txt). (On Windows, add `PYTHONIOENCODING=utf-8` in front if the `°C` in the output gives an encoding error.)

The data has to be **interesting**: if every product had enough stock, nothing expired and no fridge ever failed, the first query would return nothing and the triggers would never fire. So the shortages, expiring batches and the excursion below are planted on purpose, and each one is something a teammate's work must find.

## Time window

One quarter: **1 January to 31 March 2026**. "Today" for queries about expiry and outstanding orders is **Monday 16 March 2026, 08:00**, the morning after the story's incident.

## Volumes

Measured with seed 42:

| Table | Small (default) | Full (`--full`) |
|---|---|---|
| `product` | 20 | 200 (one third cold chain) |
| `supplier` | 3 | 15 |
| `location` | 4 (zones A to C + cold room 2) | 8 (zones A to E, cold rooms 1 to 3) |
| `batch` | 50 | 1,500 |
| `stock_movement` | 1,000 | **117,400** |
| `customer` | 10 | 120 (pharmacies, clinics, practices, hospitals) |
| `customer_order` | 50 | 3,000 |
| `order_line` | 190 | **14,735** |
| `allocation` | 7 | 907 |
| `sensor_reading` | 288 (cold room 2, 14 March only) | 64,227 (every 5 minutes, 3 cold rooms, 1 January to 16 March) |

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

## Assumptions in v1 (to revisit in Sprint 2)

- **The generator does not apply the quarantine.** All batches are `released`; putting the cold room 2 batches into quarantine is the job of Chengpu's trigger. The script prints how many batches must be quarantined (11 small, 96 full) and that the insulin becomes short only after the quarantine.
- **Picks are not linked to orders yet.** They are stock movements with their own `source_ref` (`PCK-...`). Linking each pick to a shipped order line needs a column the schema does not have yet.
- **Picked and packed orders still count as on hand** until they are shipped; their stock is reserved through `allocation`.
- **Replays are loaded with `ON CONFLICT ... DO NOTHING`**, so the database shows that they are absorbed. Anshpreet and Chengpu will replace this with their own `UPSERT` rules.
- Random open orders never ask for more than the free stock, so **only the planted products are short**. The script checks this in SQL.

## Answered by schema v1

1. Erick: `stock_movement.source_ref` is `UNIQUE`, and the location is on the movement, so the batches in cold room 2 are found from their movements. A transfer between rooms is two rows.
2. `sensor_reading` has the primary key `(location_id, ts)`, so replayed readings are absorbed.

## Still open

1. Chengpu: is one reading above 8 °C already an excursion, or only after a minimum duration? The planted excursion lasts 6 hours (47 readings above 8 °C), so both definitions catch it.
2. Smit: is "today" fixed (16 March 2026) in the queries, or a parameter? A fixed date keeps the results reproducible.
