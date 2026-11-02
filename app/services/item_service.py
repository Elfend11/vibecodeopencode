from app.errors import ApiError
from app.repositories import item_repository


def _parse_non_negative_int(value, field_name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ApiError(f"Field '{field_name}' harus berupa bilangan bulat.")
    if value < 0:
        raise ApiError(f"Field '{field_name}' tidak boleh bernilai negatif.")
    return value


def list_items():
    """Return the current list of lab equipment."""
    return item_repository.get_all_items()


def create_item(payload):
    """Validate the payload and store a new item."""
    if not isinstance(payload, dict):
        raise ApiError("Request body harus berupa objek JSON.")

    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ApiError("Field 'name' wajib diisi dan tidak boleh kosong.")

    total_stock = _parse_non_negative_int(
        payload.get("total_stock", 0), "total_stock"
    )

    return item_repository.create_item(name.strip(), total_stock)
