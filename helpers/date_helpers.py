from datetime import date

def replace_date_year(date: date, year: int) -> date:
    """Функція яка змінює рік в даті, враховуючи високосний"""
    try:
        return date.replace(year=year)
    except ValueError:
        return date.replace(year=year, month=2, day=28)