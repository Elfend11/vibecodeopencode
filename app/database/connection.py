import sqlite3
from contextlib import contextmanager

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Return the SQLite connection for the current application context."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            timeout=10,
        )
        g.db.row_factory = sqlite3.Row
        # SQLite disables foreign keys per connection by default.
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(exception=None):
    """Close the SQLite connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the database schema from schema.sql."""
    db = get_db()
    with current_app.open_resource("database/schema.sql") as schema_file:
        db.executescript(schema_file.read().decode("utf-8"))


@contextmanager
def transaction():
    """Run a block in a single database transaction.

    Commits when the block succeeds and rolls back on any exception, so
    stock updates and loan status changes stay consistent.
    """
    db = get_db()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    else:
        db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database schema."""
    init_db()
    click.echo("Initialized the database.")
