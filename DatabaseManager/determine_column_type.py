def determine_column_type(value):
    """
    Определяет тип данных SQL на основе значения.
    :param value: Значение, для которого нужно определить тип.
    :return: Соответствующий тип данных SQL.
    """
    if isinstance(value, str):
        return "VARCHAR(255)"
    elif isinstance(value, int):
        return "INTEGER"
    elif isinstance(value, float):
        return "FLOAT"
    elif isinstance(value, bool):
        return "BOOLEAN"
    elif isinstance(value, bytes):
        return "BYTEA"
    else:
        return "TEXT"  # Если тип не распознан, использовать TEXT