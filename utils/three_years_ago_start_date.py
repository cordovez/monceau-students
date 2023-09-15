import datetime

def past_three_years():
    today = datetime.date.today()
    three_years_ago = today - datetime.timedelta(days=365 * 3)
    return three_years_ago