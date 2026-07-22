# SQLite persistence

VulnTrack uses SQLite for the teaching scenario because it is transactional,
ships with Python, and makes the complete API reproducible without an external
service. `SQLiteFindingRepository` is the persistence boundary; HTTP handlers
must not issue SQL directly.

## Data lifecycle

- The repository initializes the `findings` table idempotently.
- UUIDs and UTC timestamps are assigned when a finding is created.
- Enum and timestamp values are serialized to portable text representations.
- Every statement that includes user data uses SQLite parameters.
- Partial updates are validated before the repository constructs a fixed-column
  assignment list.
- A new connection is opened per operation and always closed by a context
  manager.

## Operational limits

SQLite is appropriate for this small, single-service experiment. It is not a
claim that one local database file is the right production choice for high
write concurrency, multi-region availability, or independent horizontal
scaling. The repository boundary keeps a future PostgreSQL implementation from
changing the public API contract.

Local `*.sqlite3` files are ignored by Git. Tests use a temporary directory and
leave no database in the working tree.
