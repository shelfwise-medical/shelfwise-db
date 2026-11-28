# Chengpu Li: Integrity & transactions (cold chain)

Back to the [README](../README.md) · [Sprint plan](../docs/sprint-plan.md)

**Your role:** you turn the story's incident into rules the database enforces by itself: when a cold room leaves 2 to 8 °C, every batch in it goes into quarantine and can no longer be picked. You share the integrity work with Anshpreet, who handles the order lifecycle.

**You work with:** Erick (tables), Roberto (sensor readings and the excursion in the data), Anshpreet (a quarantined batch can never be allocated).

## Step 0: get set up (first day)

1. Accept the invitation to the **shelfwise-medical** organization on GitHub (check your email or github.com/notifications).
2. Clone the repo and create your branch:
   ```bash
   git clone https://github.com/shelfwise-medical/shelfwise-db.git
   cd shelfwise-db
   git switch -c chengpu/sprint-1
   ```
3. Install [uv](https://docs.astral.sh/uv/) if you don't have it (same tool as in our portfolios).
4. **Your first commit:** tick the checkbox below in *this* file, commit it from your own account, push your branch and open a pull request. This proves your access works and starts your commit history.
   - [X] I have read this file and the [sprint plan](../docs/sprint-plan.md), and I can push to the repo.
5. From now on: one branch per task and a pull request for every change. You can merge your own pull request once your work runs; Roberto reviews everyone's merged work every week before the Monday meeting.

## Sprint 1 tasks (due Monday 30 November)

Sprint 1 is about **rules on paper**. Write `integrity/cold-chain-rules.md` with:

1. **Sensor readings:** what one reading contains (cold room, timestamp, temperature), how often it arrives, and which natural key prevents duplicates when a sensor re-sends (`(location_id, ts)`, like `(sensor_id, ts)` in Module 4).
2. **Excursion:** when exactly is a reading an excursion? Any single reading outside 2 to 8 °C, or only if it lasts a certain time? Decide and justify.
3. **Quarantine:** what happens automatically on an excursion (a trigger sets the batches in that room to `quarantined`), and how the quality manager releases a batch again.
4. **Audit trail:** which changes must be recorded (batch status, stock movements), and what an audit row contains (old value, new value, who, when), as in the Module 4 audit trigger.
5. Give Erick any column these rules need **by Saturday**.

## Definition of done for Sprint 1

- `integrity/cold-chain-rules.md` merged and agreed at the Monday meeting.
- Erick's schema v1 has the columns your rules need.
