from flask import abort

def validate_json_data(data, required_fields=None):
    """Перевіряє, чи передано JSON і чи містить він обов'язкові поля."""
    if not data:
        abort(400, description="Тіло запиту повинно містити JSON-дані.")
    
    if required_fields:
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Відсутнє обов'язкове поле: '{field}'.")

def validate_string_field(value, field_name, min_length=1):
    """Перевіряє, чи є поле непустим рядком потрібної довжини."""
    if not isinstance(value, str) or len(value.strip()) < min_length:
        abort(400, description=f"Поле '{field_name}' має бути рядком довжиною від {min_length} символів.")

def validate_positive_number(value, field_name):
    """Перевіряє, чи є число додатним."""
    if not isinstance(value, (int, float)) or value < 0:
        abort(400, description=f"Поле '{field_name}' має бути числом більшим або рівним 0.")