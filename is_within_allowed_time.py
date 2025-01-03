from datetime import datetime


def is_within_allowed_time():
    """Проверяет, находится ли текущее время между 23:00 и 11:00."""
    now = datetime.now().time()
    start_time = datetime.strptime("23:00", "%H:%M").time()
    end_time = datetime.strptime("11:00", "%H:%M").time()

    # Условие для времени между 23:00 и 11:00
    return now >= start_time or now <= end_time
