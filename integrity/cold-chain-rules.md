# Cold Chain Integrity Rules

**Owner:** Chengpu Li  
**Sprint:** Sprint 1  
**Scope:** Sensor readings, temperature excursions, batch quarantine, and audit trail.

## 1. Sensor Readings

### Reading structure

Each temperature reading must contain:

- `location_id`: identifies the cold room.
- `sensor_id`: identifies the sensor producing the reading.
- `ts`: timestamp when the measurement was taken.
- `temperature_c`: measured temperature in Celsius.
- `received_at`: timestamp when the database received the reading.

All timestamps must be stored in UTC.

### Reading frequency

Sensors should send one temperature reading every 5 minutes.

This frequency provides regular monitoring and helps identify temperature excursions quickly.

If readings stop arriving for more than 15 minutes, the cold room should be flagged for a sensor monitoring alert. A missing reading does not prove that the temperature is safe.

### Duplicate prevention

Use a UNIQUE constraint on:

`(location_id, ts)`

This assumes there is one authoritative reading per cold room per timestamp.

If multiple independent sensors are installed in the same room and may report at the same timestamp, use `(sensor_id, ts)` instead.

When a sensor resends an existing reading, use:

`INSERT ... ON CONFLICT DO NOTHING`

This prevents duplicate measurements from being stored or processed twice.

---

## 2. Temperature Excursions

### Safe temperature range

The permitted cold-chain temperature range is:

`2 °C <= temperature_c <= 8 °C`

A temperature reading is an excursion when:

- `temperature_c < 2 °C`, or
- `temperature_c > 8 °C`.

Readings of exactly 2 °C or 8 °C are considered safe.

### Excursion detection policy

A single valid reading outside the permitted range is sufficient to trigger an excursion.

We do not wait for multiple consecutive readings or a minimum duration.

### Justification

Medical products may be damaged by temperature exposure, and waiting for several readings could delay quarantine.

A conservative approach protects patient safety and prevents potentially compromised products from being picked or allocated.

Sensor readings must be validated before processing. Invalid readings, such as missing temperatures or impossible values, should be rejected and recorded as sensor errors rather than treated as valid temperature measurements.

---

## 3. Automatic Batch Quarantine

### Automatic action

When a valid temperature excursion is detected, the database must automatically:

1. Identify the affected cold room using `location_id`.
2. Find every inventory batch currently stored in that room.
3. Change the status of all affected batches to `quarantined`.
4. Record the status changes in the audit trail.
5. Prevent quarantined batches from being allocated, picked, or shipped.

The quarantine operation must execute in a database transaction so that partial updates do not leave some batches available and others quarantined.

### Quarantine enforcement

A database trigger or equivalent database-level enforcement must ensure that batches in `quarantined` status cannot be used for stock allocation or picking.

This rule must work together with Anshpreet's order lifecycle and allocation rules.

An application-level check alone is not sufficient.

### Releasing quarantined batches

A batch must never return automatically to `released` status simply because the temperature returns to the permitted range.

Only an authorized Quality Manager can approve the release.

Before releasing a batch, the Quality Manager must:

- Review the excursion and its duration.
- Review relevant sensor readings.
- Assess the affected products according to the applicable quality procedures.
- Record the release decision and reason.

The release must be an explicit, audited database operation.

If the products cannot be confirmed as safe, the batch must remain quarantined or be assigned an appropriate blocked or rejected status.

---

## 4. Audit Trail

All important integrity-related changes must be recorded.

### Events that must be audited

1. Sensor readings that trigger temperature excursions.
2. Batch status changes, especially transitions into and out of `quarantined`.
3. Stock movements associated with affected batches.
4. Quality Manager release or rejection decisions.

### Audit record structure

Each audit record should contain:

- `audit_id`: unique audit record identifier.
- `entity_type`: type of affected entity, such as batch or stock movement.
- `entity_id`: identifier of the affected record.
- `old_value`: previous value or status.
- `new_value`: updated value or status.
- `changed_by`: user or system responsible.
- `changed_at`: timestamp of the change in UTC.
- `reason`: explanation for the change.
- `source_ref`: related sensor reading, excursion, or operation reference.

### Audit enforcement

Use database triggers to record important batch status changes automatically.

The audit trail must be append-only: existing audit records must not be silently edited or deleted.

System-generated quarantine actions should identify the responsible process as the system rather than falsely attributing the action to a human user.

Stock movements must also remain auditable. Corrections should be made through reversal movements rather than deleting historical records.

---

## 5. Required Columns for Schema v1 (Erick)

The following columns are required to support the cold-chain integrity rules.

| Table | Required column | Purpose |
|---|---|---|
| cold_rooms | location_id | Unique cold room identifier |
| sensor_readings | location_id | Identifies the monitored cold room |
| sensor_readings | sensor_id | Identifies the reporting sensor |
| sensor_readings | ts | Measurement timestamp |
| sensor_readings | temperature_c | Recorded temperature |
| sensor_readings | received_at | Database receipt timestamp |
| inventory_batches | location_id | Current storage location |
| inventory_batches | batch_status | Released, quarantined, blocked, etc. |
| temperature_excursions | excursion_id | Unique excursion identifier |
| temperature_excursions | location_id | Affected cold room |
| temperature_excursions | started_at | First detected out-of-range reading |
| temperature_excursions | temperature_c | Triggering temperature |
| temperature_excursions | status | Open, under_review, resolved |
| batch_status_history | batch_id | Affected batch |
| batch_status_history | old_status | Previous status |
| batch_status_history | new_status | New status |
| batch_status_history | changed_by | User or system responsible |
| batch_status_history | changed_at | Status change timestamp |
| batch_status_history | reason | Explanation for the change |
| batch_status_history | excursion_id | Related excursion, when applicable |

### Required constraints

1. UNIQUE constraint on `(location_id, ts)` for sensor readings, assuming one authoritative reading per room per timestamp.
2. CHECK constraint to ensure valid temperature values.
3. Foreign keys linking sensor readings to cold rooms.
4. Foreign keys linking inventory batches to their cold room.
5. A reliable relationship between excursions and affected batches.
6. Database triggers for automatic quarantine and audit logging.

### Request to Erick

Please include the columns and relationships above in schema v1.

In particular, I need:

- Sensor readings linked to cold room locations.
- A timestamp and temperature value for each reading.
- Batch storage location and batch status.
- A way to record temperature excursions.
- Batch status history for auditing.
- A database-level mechanism to quarantine every batch in an affected room.

These fields are needed before the cold-chain triggers can be implemented.

---

## 6. Summary of Database Integrity Decisions

| Requirement | Proposed solution |
|---|---|
| Regular temperature monitoring | One reading every 5 minutes |
| Duplicate sensor readings | UNIQUE key and UPSERT |
| Temperature excursion | Any valid reading below 2 °C or above 8 °C |
| Automatic quarantine | Database trigger updates all batches in affected room |
| Prevent picking quarantined stock | Database-level allocation and picking validation |
| Release quarantined batches | Explicit Quality Manager approval |
| Audit status changes | Database audit trigger |
| Preserve historical records | Append-only audit and stock movement records |

**Sprint 1 outcome:** The cold-chain rules are documented and agreed upon. Erick's schema v1 must contain the columns and relationships necessary to support automatic temperature excursion detection, batch quarantine, release approval, and audit logging.

Implementation of database triggers and constraints can follow in the implementation sprint.