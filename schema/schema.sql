-- ShelfWise Medical: schema v1 (Sprint 1)
-- Owner: Erick Liebisch (data model)
-- Build:  sqlite3 shelfwise.db ".read schema/schema.sql"
--
-- v1 = tables, primary keys, foreign keys, NOT NULL and the basic value lists.
-- v2 (Sprint 2) adds the remaining constraints and the constraint tests.
-- Dates and times are ISO-8601 TEXT ('2026-03-16', '2026-03-16T08:00:00').

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS allocation;
DROP TABLE IF EXISTS order_line;
DROP TABLE IF EXISTS customer_order;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS sensor_reading;
DROP TABLE IF EXISTS stock_movement;
DROP TABLE IF EXISTS batch;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS supplier;
DROP TABLE IF EXISTS product;

-- ── Catalogue: what we sell and who delivers it ─────────────────────────

-- One row per product (not per box). Temperature limits belong to the product.
CREATE TABLE product (
    product_id  INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL UNIQUE,
    cold_chain  INTEGER NOT NULL CHECK (cold_chain IN (0, 1)),
    min_temp_c  REAL,                 -- NULL for ambient products
    max_temp_c  REAL
) STRICT;

CREATE TABLE supplier (
    supplier_id INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL UNIQUE
) STRICT;

-- ── Warehouse: where the stock is and how much ──────────────────────────

-- A zone or a cold room.
CREATE TABLE location (
    location_id  INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL UNIQUE,
    is_cold_room INTEGER NOT NULL CHECK (is_cold_room IN (0, 1))
) STRICT;

-- One delivery lot of a product. The expiry date and the quality status
-- belong to the lot, not to the product: two lots of the same insulin can
-- expire on different days, and only the lot from cold room 2 is quarantined.
CREATE TABLE batch (
    batch_id    INTEGER PRIMARY KEY,
    product_id  INTEGER NOT NULL REFERENCES product(product_id),
    supplier_id INTEGER NOT NULL REFERENCES supplier(supplier_id),
    lot_no      TEXT    NOT NULL,
    expiry_date TEXT    NOT NULL,
    status      TEXT    NOT NULL DEFAULT 'released'
                CHECK (status IN ('released', 'quarantined', 'destroyed')),
    UNIQUE (product_id, lot_no)
) STRICT;

-- Every stock change is a new row that is never edited (audit trail).
-- The location is stored here, not on batch, because one lot can be split
-- between rooms (e.g. 70 boxes stay in cold room 2, 30 are moved to cold room 1).
-- A move between rooms = two rows with the same batch: -30 in room 2, +30 in room 1.
-- Stock on hand of a batch in a location = SUM(qty) of its movements there.
CREATE TABLE stock_movement (
    movement_id INTEGER PRIMARY KEY,
    batch_id    INTEGER NOT NULL REFERENCES batch(batch_id),
    location_id INTEGER NOT NULL REFERENCES location(location_id),
    qty         INTEGER NOT NULL CHECK (qty <> 0),      -- + in, - out
    kind        TEXT    NOT NULL
                CHECK (kind IN ('receipt', 'pick', 'transfer', 'adjustment', 'destruction')),
    ts          TEXT    NOT NULL,
    source_ref  TEXT    NOT NULL UNIQUE                  -- natural key: a re-sent delivery is absorbed by UPSERT
) STRICT;

-- ── Cold chain ──────────────────────────────────────────────────────────

-- The temperature is measured per cold room, not per box.
-- (location_id, ts) is the natural key: a re-sent reading is not stored twice.
CREATE TABLE sensor_reading (
    location_id INTEGER NOT NULL REFERENCES location(location_id),
    ts          TEXT    NOT NULL,
    temp_c      REAL    NOT NULL,
    PRIMARY KEY (location_id, ts)
) STRICT;

-- ── Orders ──────────────────────────────────────────────────────────────

CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL UNIQUE
) STRICT;

-- Status values follow the lifecycle created → allocated → picked → packed → shipped.
-- Allowed transitions are enforced by Anshpreet's trigger (Sprint 2).
CREATE TABLE customer_order (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customer(customer_id),
    status      TEXT    NOT NULL DEFAULT 'created'
                CHECK (status IN ('created', 'allocated', 'picked', 'packed', 'shipped', 'cancelled')),
    created_at  TEXT    NOT NULL
) STRICT;

-- One product in an order: the bridge between orders and products (m:n).
CREATE TABLE order_line (
    order_id    INTEGER NOT NULL REFERENCES customer_order(order_id),
    product_id  INTEGER NOT NULL REFERENCES product(product_id),
    qty         INTEGER NOT NULL CHECK (qty > 0),
    PRIMARY KEY (order_id, product_id)
) STRICT;

-- Stock of one batch reserved for one order line (FEFO decides which batch).
-- One order line can be served from several batches.
CREATE TABLE allocation (
    order_id    INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    batch_id    INTEGER NOT NULL REFERENCES batch(batch_id),
    qty         INTEGER NOT NULL CHECK (qty > 0),
    PRIMARY KEY (order_id, product_id, batch_id),
    FOREIGN KEY (order_id, product_id) REFERENCES order_line(order_id, product_id)
) STRICT;

-- ── Indexes on foreign keys (SQLite does not create them automatically) ─
CREATE INDEX ix_batch_product         ON batch(product_id);
CREATE INDEX ix_movement_batch        ON stock_movement(batch_id);
CREATE INDEX ix_movement_location     ON stock_movement(location_id);
CREATE INDEX ix_order_customer        ON customer_order(customer_id);
CREATE INDEX ix_order_line_product    ON order_line(product_id);
CREATE INDEX ix_allocation_batch      ON allocation(batch_id);
