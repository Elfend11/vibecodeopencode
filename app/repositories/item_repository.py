from app.database.connection import get_db


def get_all_items():
    """Return every item with its current stock."""
    rows = get_db().execute(
        "SELECT id, name, total_stock, available_stock FROM Item ORDER BY id"
    ).fetchall()
    return [dict(row) for row in rows]


def get_item_by_id(item_id):
    """Return a single item or None when it does not exist."""
    row = get_db().execute(
        "SELECT id, name, total_stock, available_stock FROM Item WHERE id = ?",
        (item_id,),
    ).fetchone()
    return dict(row) if row is not None else None


def create_item(name, total_stock):
    """Insert a new item; available_stock starts equal to total_stock."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO Item (name, total_stock, available_stock) VALUES (?, ?, ?)",
        (name, total_stock, total_stock),
    )
    db.commit()
    return get_item_by_id(cursor.lastrowid)
