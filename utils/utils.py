from datetime import date, timedelta

def days_left_in_year() -> int:
    """Кількість днів до кінця року"""
    today: date = date.today()
    end_of_year: date = date(today.year, 12, 31)
    difference: timedelta = end_of_year - today
    return difference.days