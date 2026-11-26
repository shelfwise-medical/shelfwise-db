"""ShelfWise Medical data generator (v1).

Run from the repo root:
    uv run python generator/generate.py           # small test dataset (Sprint 1)
    uv run python generator/generate.py --full    # full dataset (~120,000 movements, ~15,000 order lines)

Builds shelfwise.db from schema/schema.sql and fills it with a reproducible dataset:
the same seed gives the same data on every machine. The planted test cases are
described in generator/README.md; the script prints the expected result of each one.
"""
import argparse
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "schema.sql"
DB = ROOT / "shelfwise.db"

SEED = 42
START = datetime(2026, 1, 1)
TODAY = datetime(2026, 3, 16, 8, 0)               # "today" for every query: the Monday after the incident
EXCURSION_START = datetime(2026, 3, 14, 2, 0)     # cold room 2, Saturday 14 March
EXCURSION_PEAK = datetime(2026, 3, 14, 5, 0)
EXCURSION_END = datetime(2026, 3, 14, 8, 0)

SIZES = {
    "small": dict(products=20, suppliers=3, zones=3, cold_rooms=[2], batches=50, movements=1_000,
                  customers=10, orders=50, order_lines=200, expired=3, expiring=4, short=2,
                  receipt_qty=(100, 300), sensor_days=[datetime(2026, 3, 14)]),
    "full": dict(products=200, suppliers=15, zones=5, cold_rooms=[1, 2, 3], batches=1_500, movements=120_000,
                 customers=120, orders=3_000, order_lines=15_000, expired=20, expiring=30, short=10,
                 receipt_qty=(300, 900), sensor_days=None),     # None = every day from START to TODAY
}

COLD_PRODUCTS = ["Insulin glargine 100 U/ml pen", "Insulin aspart 100 U/ml pen", "Influenza vaccine 0.5 ml",
                 "Hepatitis B vaccine 1 ml", "Adalimumab 40 mg syringe", "Etanercept 50 mg pen",
                 "Epoetin alfa 4000 IU syringe", "Tetanus vaccine 0.5 ml", "Somatropin 12 mg cartridge",
                 "Liraglutide 6 mg/ml pen"]
AMBIENT_PRODUCTS = ["Paracetamol 500 mg tablets", "Ibuprofen 400 mg tablets", "Sterile gauze 10x10 cm",
                    "Nitrile gloves size M", "Syringe 5 ml", "Saline 0.9% 500 ml", "Amoxicillin 500 mg capsules",
                    "Omeprazole 20 mg capsules", "Elastic bandage 8 cm", "Surgical mask type IIR",
                    "Metformin 850 mg tablets", "Wound dressing 15x15 cm", "Cannula 20G", "Alcohol swabs",
                    "Ramipril 5 mg tablets", "Blood glucose test strips", "Cotton wool 200 g",
                    "Cetirizine 10 mg tablets", "Infusion set 150 cm", "Povidone iodine 10% 100 ml"]
PACK_SIZES = [5, 10, 20, 50, 100, 3, 200]           # 70 cold and 140 ambient names: enough for the full dataset
SUPPLIERS = ["Weser Pharma GmbH", "Teuto Medical AG", "Lippe BioLogistics", "Ems Health Supply",
             "Senne Diagnostics", "Ravensberg Pharma", "Sparrenburg Medical", "Wiehen Labs",
             "Minden Medtech", "Paderborn Biologics", "Detmold Care Products", "Herford Surgical",
             "Halle Pharma Trading", "Verl Clinical Supply", "Bünde Medical Devices"]
CUSTOMER_KINDS = ["Pharmacy", "Clinic", "Practice", "Hospital"]
TOWNS = ["Bielefeld", "Gütersloh", "Herford", "Paderborn", "Detmold", "Minden", "Lemgo", "Bünde",
         "Halle", "Verl", "Rheda-Wiedenbrück", "Bad Salzuflen"]


def iso(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%S")


def generate(size: str) -> None:
    cfg = SIZES[size]
    rnd = random.Random(SEED)

    # ── catalogue ───────────────────────────────────────────────────────────
    n_cold = cfg["products"] // 3
    names_cold = [f"{b}, pack of {p}" for p in PACK_SIZES for b in COLD_PRODUCTS]
    names_amb = [f"{b}, pack of {p}" for p in PACK_SIZES for b in AMBIENT_PRODUCTS]
    products = []                                   # (product_id, name, cold_chain, min_temp_c, max_temp_c)
    for i in range(cfg["products"]):
        cold = i < n_cold
        name = names_cold[i] if cold else names_amb[i - n_cold]
        products.append((i + 1, name, int(cold), 2.0 if cold else None, 8.0 if cold else None))
    cold_ids = [p[0] for p in products if p[2]]
    amb_ids = [p[0] for p in products if not p[2]]
    is_cold = {p[0]: p[2] for p in products}

    suppliers = [(i + 1, SUPPLIERS[i]) for i in range(cfg["suppliers"])]

    zones = [(i + 1, f"Zone {chr(65 + i)}", 0) for i in range(cfg["zones"])]
    rooms = [(len(zones) + k + 1, f"Cold room {n}", 1) for k, n in enumerate(cfg["cold_rooms"])]
    locations = zones + rooms
    zone_ids = [z[0] for z in zones]
    room_ids = [r[0] for r in rooms]
    room2 = next(r[0] for r in rooms if r[1] == "Cold room 2")

    # ── planted products ────────────────────────────────────────────────────
    insulin = cold_ids[0]                           # case 6: the Monday insulin order
    hidden = amb_ids[0]                             # case 2: hidden shortage
    pool = [p for p in cold_ids[1:]] + [p for p in amb_ids[1:]]
    n_short_cold = 3 if size == "full" else 1
    short = sorted(rnd.sample(cold_ids[1:], n_short_cold) +
                   rnd.sample(amb_ids[1:], cfg["short"] - n_short_cold))      # case 1
    planted = {insulin, hidden, *short}

    # ── batches ─────────────────────────────────────────────────────────────
    batches = []                                    # (batch_id, product_id, supplier_id, lot_no, expiry_date, status)
    expiry = {}
    lot_count = {}

    def add_batch(product_id: int, exp: datetime) -> int:
        bid = len(batches) + 1
        lot_count[product_id] = lot_count.get(product_id, 0) + 1
        lot = f"L{product_id:03d}-{lot_count[product_id]:02d}"
        batches.append((bid, product_id, rnd.choice(suppliers)[0], lot, exp.strftime("%Y-%m-%d"), "released"))
        expiry[bid] = exp
        return bid

    def normal_expiry() -> datetime:
        return datetime(2026, 4, 20) + timedelta(days=rnd.randrange(0, 620))

    insulin_batch = add_batch(insulin, datetime(2026, 9, 30))
    hidden_expired = add_batch(hidden, datetime(2026, 3, 1))
    hidden_fresh = add_batch(hidden, datetime(2026, 11, 30))
    for p in short:
        add_batch(p, normal_expiry())
    while len(batches) < cfg["batches"]:
        add_batch(rnd.choice(pool), normal_expiry())

    free_batches = [b[0] for b in batches if b[1] not in planted]
    for bid in rnd.sample(free_batches, cfg["expired"] + cfg["expiring"]):
        if cfg["expired"] > sum(1 for b in free_batches if expiry[b] < TODAY):
            expiry[bid] = datetime(2026, 2, 1) + timedelta(days=rnd.randrange(0, 42))     # case 3: expired before 16 Mar
        else:
            expiry[bid] = TODAY + timedelta(days=rnd.randrange(1, 31))                   # case 4: expires within 30 days
    batches = [(b, p, s, lot, expiry[b].strftime("%Y-%m-%d"), st) for b, p, s, lot, _, st in batches]
    product_of = {b[0]: b[1] for b in batches}

    # ── stock movements ─────────────────────────────────────────────────────
    movements = []                                  # (batch_id, location_id, qty, kind, ts, source_ref)
    balance, last_ts, floor = {}, {}, {}
    ref = {"RCV": 0, "TRF": 0, "PCK": 0}

    def move(bid, loc, qty, kind, ts, prefix):
        ref[prefix] += 1
        movements.append((bid, loc, qty, kind, iso(ts), f"{prefix}-{ref[prefix]:06d}"))
        balance[(bid, loc)] = balance.get((bid, loc), 0) + qty
        last_ts[(bid, loc)] = max(last_ts.get((bid, loc), ts), ts)

    def receive(bid, loc, qty, ts):
        move(bid, loc, qty, "receipt", ts, "RCV")

    lo, hi = cfg["receipt_qty"]
    receive(insulin_batch, room2, 100, datetime(2026, 2, 20, 9, 15))
    receive(hidden_expired, zone_ids[0], 250, datetime(2026, 1, 12, 10, 0))
    receive(hidden_fresh, zone_ids[0], 30, datetime(2026, 3, 2, 11, 30))
    for b in batches:
        bid, pid = b[0], b[1]
        if bid in (insulin_batch, hidden_expired, hidden_fresh):
            continue
        loc = rnd.choice(room_ids if is_cold[pid] else zone_ids)
        latest = min(expiry[bid] - timedelta(days=10), datetime(2026, 3, 10))
        ts = START + timedelta(minutes=rnd.randrange(0, int((latest - START).total_seconds() // 60)))
        receive(bid, loc, rnd.randint(lo, hi), ts)
        if expiry[bid] < TODAY:
            floor[(bid, loc)] = 20                  # expired batches keep some stock on the shelf

    # transfers between rooms: one batch split over two locations (two rows)
    candidates = sorted(k for k in balance if product_of[k[0]] not in planted)
    for bid, loc in rnd.sample(candidates, max(1, len(candidates) // 30)):
        same_type = room_ids if loc in room_ids else zone_ids
        targets = [l for l in same_type if l != loc]
        if not targets:
            continue
        to, qty, ts = rnd.choice(targets), balance[(bid, loc)] * 3 // 10, last_ts[(bid, loc)] + timedelta(days=1)
        move(bid, loc, -qty, "transfer", ts, "TRF")
        move(bid, to, qty, "transfer", ts, "TRF")
        floor.setdefault((bid, to), floor.get((bid, loc), 0))

    # picks until the target number of movements, each key moving forward in time
    keys = sorted(k for k in balance if product_of[k[0]] not in (insulin, hidden))
    while len(movements) < cfg["movements"] and keys:
        k = rnd.choice(keys)
        bid, loc = k
        ts = last_ts[k] + timedelta(minutes=rnd.randrange(30, 1200))
        limit = min(TODAY, expiry[bid])
        room = balance[k] - floor.get(k, 0)
        if ts >= limit or room <= 0:
            keys.remove(k)
            continue
        move(bid, loc, -rnd.randint(1, min(10, room)), "pick", ts, "PCK")
    movements.sort(key=lambda m: m[4])

    # case 7: about 1% of deliveries are re-sent with the same source_ref
    receipts = [m for m in movements if m[3] == "receipt"]
    replayed_movements = rnd.sample(receipts, max(1, len(receipts) // 100))

    # ── orders ──────────────────────────────────────────────────────────────
    customers = []
    for i in range(cfg["customers"]):
        customers.append((i + 1, f"{CUSTOMER_KINDS[i % 4]} {TOWNS[(i // 4) % len(TOWNS)]} {i // 48 + 1}"))
    customer_ids = [c[0] for c in customers]

    orders, lines, allocations = [], [], []
    allocated = {}                                  # batch_id -> reserved qty
    stock_of = {}
    for (bid, _), q in balance.items():
        stock_of[bid] = stock_of.get(bid, 0) + q
    outstanding = ("created", "allocated", "picked", "packed")

    def safe_batches(pid):
        return sorted((b for b in stock_of if product_of[b] == pid and expiry[b] >= TODAY), key=lambda b: expiry[b])

    def allocate(oid, pid, qty):
        for b in safe_batches(pid):                 # FEFO: first expired, first out
            free = stock_of[b] - allocated.get(b, 0)
            take = min(free, qty)
            if take > 0:
                allocations.append((oid, pid, b, take))
                allocated[b] = allocated.get(b, 0) + take
                qty -= take
            if qty == 0:
                break

    def free_safe(pid):
        return sum(stock_of[b] - allocated.get(b, 0) for b in safe_batches(pid))

    pending = {}                                    # product_id -> demand of 'created' orders (not yet allocated)
    random_pool = [p for p in pool if p not in planted]
    avg = cfg["order_lines"] / cfg["orders"]
    n_orders = cfg["orders"] - cfg["short"] - 3     # leave room for the planted orders
    for i in range(n_orders):
        oid = i + 1
        created = START + timedelta(minutes=rnd.randrange(0, int((TODAY - START).total_seconds() // 60)))
        if created < TODAY - timedelta(days=7):
            status = "cancelled" if rnd.random() < 0.02 else "shipped"
        else:
            status = rnd.choice(outstanding)
        orders.append((oid, rnd.choice(customer_ids), status, iso(created)))
        for pid in rnd.sample(random_pool, min(len(random_pool), rnd.randint(1, int(2 * avg) - 1))):
            qty = rnd.randint(1, 20)
            if status in outstanding:
                # random open orders never exceed the free stock: only the planted products may be short
                qty = min(qty, free_safe(pid) - pending.get(pid, 0))
                if qty <= 0:
                    continue
            lines.append((oid, pid, qty))
            if status in ("allocated", "picked", "packed"):
                allocate(oid, pid, qty)
            elif status == "created":
                pending[pid] = pending.get(pid, 0) + qty

    def planted_order(pid, qty, created, status="created"):
        oid = len(orders) + 1
        orders.append((oid, rnd.choice(customer_ids), status, iso(created)))
        lines.append((oid, pid, qty))
        if status == "allocated":
            allocate(oid, pid, qty)
        return oid

    expected = []
    planted_order(hidden, 20, TODAY - timedelta(days=2), status="allocated")      # reserves 20 of the 30 fresh units
    missing = 50
    planted_order(hidden, free_safe(hidden) + missing, TODAY - timedelta(hours=20))
    expected.append(("case 2, hidden shortage", hidden, missing))
    for pid in short:
        missing = rnd.randint(10, 60)
        planted_order(pid, free_safe(pid) + missing, TODAY - timedelta(hours=rnd.randint(2, 48)))
        expected.append(("case 1, shortage", pid, missing))
    insulin_order = planted_order(insulin, 40, datetime(2026, 3, 16, 7, 30))      # case 6

    # ── sensor readings (every 5 minutes) ───────────────────────────────────
    days = cfg["sensor_days"] or [START + timedelta(days=d) for d in range((TODAY - START).days + 1)]
    sensor_rooms = [room2] if cfg["sensor_days"] else room_ids
    readings = []
    for loc in sensor_rooms:
        temp = 5.0
        for day in days:
            for step in range(288):
                ts = day + timedelta(minutes=5 * step)
                if ts > TODAY:
                    break
                temp = min(7.0, max(3.0, temp + rnd.uniform(-0.2, 0.2)))
                value = temp
                if loc == room2 and EXCURSION_START <= ts <= EXCURSION_END:              # case 5
                    if ts <= EXCURSION_PEAK:
                        value = 5.0 + 9.0 * (ts - EXCURSION_START) / (EXCURSION_PEAK - EXCURSION_START)
                    else:
                        value = 14.0 - 9.0 * (ts - EXCURSION_PEAK) / (EXCURSION_END - EXCURSION_PEAK)
                readings.append((loc, iso(ts), round(value, 1)))
    replayed_readings = rnd.sample(readings, max(1, len(readings) // 200))     # case 8

    # ── load into shelfwise.db ──────────────────────────────────────────────
    DB.unlink(missing_ok=True)
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA.read_text(encoding="utf-8"))
    con.execute("PRAGMA foreign_keys = ON")
    with con:
        con.executemany("INSERT INTO product VALUES (?, ?, ?, ?, ?)", products)
        con.executemany("INSERT INTO supplier VALUES (?, ?)", suppliers)
        con.executemany("INSERT INTO location VALUES (?, ?, ?)", locations)
        con.executemany("INSERT INTO batch VALUES (?, ?, ?, ?, ?, ?)", batches)
    move_sql = ("INSERT INTO stock_movement(batch_id, location_id, qty, kind, ts, source_ref) "
                "VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(source_ref) DO NOTHING")
    with con:
        con.executemany(move_sql, movements)
    before = con.execute("SELECT COUNT(*) FROM stock_movement").fetchone()[0]
    with con:
        con.executemany(move_sql, replayed_movements)
    after = con.execute("SELECT COUNT(*) FROM stock_movement").fetchone()[0]
    reading_sql = "INSERT INTO sensor_reading VALUES (?, ?, ?) ON CONFLICT(location_id, ts) DO NOTHING"
    with con:
        con.executemany(reading_sql, readings + replayed_readings)
        con.executemany("INSERT INTO customer VALUES (?, ?)", customers)
        con.executemany("INSERT INTO customer_order VALUES (?, ?, ?, ?)", orders)
        con.executemany("INSERT INTO order_line VALUES (?, ?, ?)", lines)
        con.executemany("INSERT INTO allocation VALUES (?, ?, ?, ?)", allocations)

    # ── report ──────────────────────────────────────────────────────────────
    print(f"shelfwise.db built ({size} dataset, seed {SEED}); today = {iso(TODAY)}")
    print("\nRows per table:")
    for t in ("product", "supplier", "location", "batch", "stock_movement", "sensor_reading",
              "customer", "customer_order", "order_line", "allocation"):
        print(f"  {t:15s} {con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]:>8,}")

    name = {p[0]: p[1] for p in products}
    q = lambda sql, *a: con.execute(sql, a).fetchone()[0]
    print("\nPlanted cases (see generator/README.md):")
    for label, pid, miss in expected:
        print(f"  {label}: product {pid} ({name[pid]}) is short by {miss}")
    today = TODAY.strftime("%Y-%m-%d")
    print(f"  case 3, expired batches with stock left: "
          f"{q('SELECT COUNT(*) FROM (SELECT b.batch_id FROM batch b JOIN stock_movement m USING (batch_id) WHERE b.expiry_date < ? GROUP BY b.batch_id HAVING SUM(m.qty) > 0)', today)}")
    print(f"  case 4, batches expiring within 30 days: "
          f"{q('SELECT COUNT(*) FROM batch WHERE expiry_date >= ? AND expiry_date <= ?', TODAY.strftime('%Y-%m-%d'), (TODAY + timedelta(days=30)).strftime('%Y-%m-%d'))}")
    print(f"  case 5, cold room 2 readings above 8.0 °C on 14 March: "
          f"{q('SELECT COUNT(*) FROM sensor_reading WHERE location_id = ? AND temp_c > 8.0', room2)} "
          f"(peak {q('SELECT MAX(temp_c) FROM sensor_reading WHERE location_id = ?', room2)} °C)")
    print(f"  case 6, Monday insulin order: order {insulin_order}, 40 x {name[insulin]}; "
          f"its only batch ({insulin_batch}) is in cold room 2. Not short before the quarantine, short by 40 after it")
    print(f"  case 7, replayed deliveries: {len(replayed_movements)} re-sent, {after - before} stored twice")
    print(f"  case 8, replayed sensor readings: {len(replayed_readings)} re-sent, "
          f"{len(readings) + len(replayed_readings) - q('SELECT COUNT(*) FROM sensor_reading')} absorbed")
    print(f"  cold room 2 batches with stock on 14 March (must go into quarantine): "
          f"{q('SELECT COUNT(*) FROM (SELECT batch_id FROM stock_movement WHERE location_id = ? AND ts < ? GROUP BY batch_id HAVING SUM(qty) > 0)', room2, iso(EXCURSION_START))}")

    negative = q("SELECT COUNT(*) FROM (SELECT batch_id, location_id FROM stock_movement "
                 "GROUP BY batch_id, location_id HAVING SUM(qty) < 0)")
    print(f"\nCheck: batch/location pairs with negative stock: {negative}")
    # Independent SQL check, before any quarantine: demand of outstanding orders not yet allocated,
    # compared with unexpired stock minus what is already allocated. Only the planted products may appear.
    shortages = con.execute("""
        WITH safe AS (SELECT b.product_id, SUM(m.qty) AS on_hand FROM batch b JOIN stock_movement m USING (batch_id)
                      WHERE b.expiry_date >= :today GROUP BY b.product_id),
             open_orders AS (SELECT order_id FROM customer_order WHERE status IN ('created','allocated','picked','packed')),
             reserved AS (SELECT a.product_id, SUM(a.qty) AS qty FROM allocation a JOIN open_orders USING (order_id)
                          GROUP BY a.product_id),
             demand AS (SELECT l.product_id, SUM(l.qty) AS qty FROM order_line l JOIN open_orders USING (order_id)
                        GROUP BY l.product_id)
        SELECT d.product_id,
               (d.qty - COALESCE(r.qty, 0)) - (COALESCE(s.on_hand, 0) - COALESCE(r.qty, 0)) AS missing
        FROM demand d LEFT JOIN safe s USING (product_id) LEFT JOIN reserved r USING (product_id)
        WHERE (d.qty - COALESCE(r.qty, 0)) > (COALESCE(s.on_hand, 0) - COALESCE(r.qty, 0))
        ORDER BY d.product_id""", {"today": today}).fetchall()
    planted_short = sorted((pid, miss) for _, pid, miss in expected)
    print(f"Check: products short in SQL (before quarantine): {shortages}; planted: {planted_short}; "
          f"match: {shortages == planted_short}")
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--full", action="store_true", help="build the full dataset instead of the small test one")
    generate("full" if parser.parse_args().full else "small")
