# Story: The Fridge That Failed on a Saturday

Back to the [README](../README.md)

**ShelfWise Medical** is a regional distribution warehouse in Bielefeld that supplies pharmacies, clinics and doctors' practices across Ostwestfalen-Lippe. About a third of its products are **cold-chain goods**: vaccines, insulin and biologics that must stay between **2 °C and 8 °C** from the moment they arrive until the moment they leave.

On a Saturday in March, the compressor of cold room 2 failed. The temperature climbed to 14 °C for six hours before anyone noticed. On Monday morning a picker shipped 40 packs of insulin from that room to a clinic, because the system still listed them as available. The quality manager, **Dr. Lena Hoffmann**, had to recall the whole batch, call every customer and report the incident to the authorities.

The inventory planner, **Jonas Weber**, has a second problem. His spreadsheet counts what is on the shelf, but not what is already reserved for other orders, what has expired, or what is in quarantine after a temperature excursion. Twice this quarter a hospital order could not be filled, and he only found out when the picker reported an empty shelf.

Their question to us: *"Can the database refuse to ship what is not safe to ship, and tell us what we are short of before an order fails?"*

## The cast (all fictional)

| Person | Role | What they need from the database |
|---|---|---|
| **Jonas Weber**, inventory planner | **Main person** | Which products are short for outstanding orders, and how much to reorder |
| **Dr. Lena Hoffmann**, quality manager | Releases or blocks quarantined batches, handles recalls | Which batches were in a cold room during an excursion; who received a recalled batch |
| Receiving clerk | Records deliveries | Every delivery recorded once, with lot number and expiry date |
| Warehouse picker | Picks orders | The batch to pick (first expired, first out), and never a quarantined or expired batch |

## What the cold chain adds

| Concept | Meaning |
|---|---|
| **Batch (lot) number** | Every delivery of a product has a lot number, so a recall can target exactly the affected units |
| **Expiry date, FEFO** | *First Expired, First Out*: always pick the batch that expires first |
| **Cold room sensors** | A temperature reading every few minutes per cold room |
| **Temperature excursion** | A reading outside 2 to 8 °C; every batch stored in that room goes into **quarantine** automatically |
| **Quarantine** | A quarantined batch is not available until the quality manager releases it (or it is destroyed) |
| **Audit trail** | Every stock change is recorded and never edited, as required in medical distribution |

## The order lifecycle

`created → allocated → picked → packed → shipped`

- **allocated:** stock from specific batches is reserved for the order
- **picked:** the picker took it from the shelf (FEFO)
- **shipped:** it left the warehouse; from here it can only be traced, not changed

## The first query

> *"Which products have insufficient **safe available stock** to fulfil outstanding customer orders, and how much more is needed?"*
>
> **safe available stock** = on hand − allocated to other orders − quarantined − expired
