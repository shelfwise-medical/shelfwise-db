# ER diagram: schema v1

Back to the [README](../README.md) · Source of truth: [`schema.sql`](schema.sql) · Design notes: [`notes.md`](notes.md)

GitHub draws this diagram automatically. Notation: `||--o{` = one to many (one on the left, zero or more on the right).

```mermaid
erDiagram
    product        ||--o{ batch          : "is delivered as"
    supplier       ||--o{ batch          : "delivers"
    batch          ||--o{ stock_movement : "moves as"
    location       ||--o{ stock_movement : "is where"
    location       ||--o{ sensor_reading : "is measured by"
    customer       ||--o{ customer_order : "places"
    customer_order ||--|{ order_line     : "contains"
    product        ||--o{ order_line     : "is ordered in"
    order_line     ||--o{ allocation     : "is served by"
    batch          ||--o{ allocation     : "is reserved in"

    product {
        INTEGER product_id PK
        TEXT    name
        INTEGER cold_chain "0 or 1"
        REAL    min_temp_c
        REAL    max_temp_c
    }
    supplier {
        INTEGER supplier_id PK
        TEXT    name
    }
    location {
        INTEGER location_id PK
        TEXT    name
        INTEGER is_cold_room "0 or 1"
    }
    batch {
        INTEGER batch_id PK
        INTEGER product_id FK
        INTEGER supplier_id FK
        TEXT    lot_no
        TEXT    expiry_date
        TEXT    status "released, quarantined, destroyed"
    }
    stock_movement {
        INTEGER movement_id PK
        INTEGER batch_id FK
        INTEGER location_id FK
        INTEGER qty "+ in, - out"
        TEXT    kind
        TEXT    ts
        TEXT    source_ref UK
    }
    sensor_reading {
        INTEGER location_id PK, FK
        TEXT    ts PK
        REAL    temp_c
    }
    customer {
        INTEGER customer_id PK
        TEXT    name
    }
    customer_order {
        INTEGER order_id PK
        INTEGER customer_id FK
        TEXT    status
        TEXT    created_at
    }
    order_line {
        INTEGER order_id PK, FK
        INTEGER product_id PK, FK
        INTEGER qty
    }
    allocation {
        INTEGER order_id PK, FK
        INTEGER product_id PK, FK
        INTEGER batch_id PK, FK
        INTEGER qty
    }
```

## The two m:n relationships

| Between | Bridge table | Why |
|---|---|---|
| `customer_order` and `product` | `order_line` | An order contains many products, and a product appears in many orders |
| `order_line` and `batch` | `allocation` | One order line can be served from several batches (FEFO), and one batch serves many order lines |
