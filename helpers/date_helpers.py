from datetime import date

def replace_date_year(date: date, year: int) -> date:
    try:
        return date.replace(year=year)
    except ValueError:
        return date.replace(year=year, month=2, day=28)