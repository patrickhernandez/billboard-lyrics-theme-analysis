from datetime import date, datetime, timedelta

def convert_to_date(d):
    if isinstance(d, date):
        return d
    elif isinstance(d, str):
        try: 
            return datetime.strptime(d, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('String date must be YYYY-MM-DD')
    elif isinstance(d, int):
        s = str(d)
        if len(s) != 8:
            raise ValueError('Numeric date must be YYYYMMDD')
        return date(int(s[:4]), int(s[4:6]), int(s[6:]))
    else:
        return None

def get_dates(start=None, end=None):
    dates = []
    min_start = date(1958, 8, 2)
    start = convert_to_date(start)
    end = convert_to_date(end)
    today = date.today()

    if start is None or start < min_start:
        start = min_start
    if end is None or end > today:
        end = today - timedelta(days=(today.weekday() - 5) % 7)
    
    current = start + timedelta(days=(5 - start.weekday()) % 7)
    while current <= end:
        dates.append(current)
        current += timedelta(days=7)

    return dates
