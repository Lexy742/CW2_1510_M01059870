# Copilot / AI coding instructions for this repository

Short summary
- This repo contains Week 8 coursework: a small Python package `app` that loads CSV datasets into an SQLite DB and provides simple user management (bcrypt) and CRUD for incidents/tickets.
- Entrypoint used in exercises: `Week 8/main.py` (run from repo root with the path or from the `Week 8` folder).

Key files & structure
- `Week 8/main.py` — top-level script that creates tables, migrates users, loads CSVs and exercises service functions.
- `app/data/` — data-layer modules:
  - `db.py` — connection helper; exposes `DB_PATH` and `connect_database()`.
  - `schema.py` — table creation functions (e.g., `create_all_tables(conn)` / `create_users_table(conn)`).
  - `datasets.py`, `tickets.py`, `incidents.py`, `users.py` — table-specific loaders/CRUD.
- `app/services/` — business logic (e.g., `user_service.py` handles registration, login, migrations).
- `users.txt` and `DATA/` — data files used for migrations and CSV loads.

How to run locally (simple)
- From repo root (recommended):

  cd "Week 8"
  python main.py

- Notes:
  - The app creates/uses the SQLite DB at `DATA/intelligence_platform.db` (see `app/data/db.py`).
  - CSVs expected: `DATA/cyber_incidents.csv`, `DATA/it_tickets.csv`, `DATA/datasets_metadata.csv`. If missing, CSV loaders will print a message and skip.
  - The user migration looks for `DATA/users.txt` by default — there is also a `users.txt` at the repo root, so confirm the path before running migration.

Project-specific conventions / common gotchas for an AI helper
- Imports inside package modules must be package-relative. Fix pattern examples:
  - Bad: `from db import connect_database` or `from data.db import connect_database` (these cause ModuleNotFoundError when `app` is imported).
  - Good: `from .db import connect_database` (inside `app/data/*`) or `from app.data.db import connect_database` when importing from outside `app`.
  - Example fixes applied in this branch: `app/data/incidents.py`, `app/data/datasets.py`, `app/data/tickets.py`.
- Be careful with small typos that cause runtime errors: `con` vs `conn`, `excute` vs `execute`, mismatched table names (`incidents` vs `cyber_incidents`). When you change SQL, run `main.py` to catch these quickly.
- Database path is a project-level constant: `DB_PATH = Path("DATA") / "intelligence_platform.db"` in `app/data/db.py` — prefer using `connect_database()` to obtain connections.

Data flow summary (how things connect)
- `main.py` calls `connect_database()` → `create_all_tables(conn)` → `migrate_users_from_file()` → CSV loaders `load_csv_to_table(...)` which use `pandas` and `df.to_sql(..., conn)` to append data.
- `user_service.register_user()` uses `app.data.users.insert_user()` (which calls `connect_database()`), and passwords are hashed via `bcrypt`.

Quick debugging checklist for AI edits
- After editing imports or DB code, run `python "Week 8/main.py"` from repo root and inspect tracebacks.
- If you see ModuleNotFoundError referencing `db` or `data`, prefer replacing `from db`/`from data.db` with `from .db` inside `app/data` modules.
- For SQL errors or unexpected behavior: inspect `app/data/schema.py` to confirm table and column names match SQL used by loader/CRUD functions.
- For migrations: confirm the path passed to `migrate_users_from_file()` — tests used `DATA/users.txt` but some code references `users.txt` at repo root.

Dependencies
- See `Week 8/requirements.txt` for required packages (e.g., `pandas`, `bcrypt`). Use the repo's Python environment when running.

When to create PR vs small patch
- Small, mechanical fixes (relative imports, typo fixes, SQL param order) can be applied directly and verified by running `main.py`.
- Larger refactors (switching DB backends, changing schema) should come with an update to `app/data/schema.py` and a short migration plan in the PR description.

If anything is unclear or you'd like me to expand a section (examples, more file references, or add templates for tests/CI), tell me which part to iterate on.
