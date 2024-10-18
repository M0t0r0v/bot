def validate_full_name(full_name: str):
    """
    Проверяет введенное полное имя.
    Возвращает фамилию, имя, отчество (если есть), либо ошибку.
    """
    name_parts = full_name.split()

    if len(name_parts) < 2:
        return (
            None,
            "Пожалуйста, введите как минимум Фамилию и Имя через пробел."
        )

    surname = name_parts[0]
    name = name_parts[1]
    patronymic = name_parts[2] if len(name_parts) > 2 else ""

    return (surname, name, patronymic), None
