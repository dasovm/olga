import datetime


# date_serie is pandas dataframe['Date']
def get_weekday_from_serie(date_serie):
    days = []
    for i in range(len(date_serie)):
        date = date_serie[i].weekday()
        days.append(get_weekday_in_text(date))
    return days


# date_serie is pandas dataframe['Date']
def get_month_from_serie(date_serie):
    months = []
    for i in range(len(date_serie)):
        date = date_serie[i].strftime("%B").upper()
        months.append(date)
    return months


def get_date_from_string(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%d")


def get_weekday_in_text(day_pos):
    if day_pos == 0:
        return 'MONDAY'
    if day_pos == 1:
        return 'TUESDAY'
    if day_pos == 2:
        return 'WEDNESDAY'
    if day_pos == 3:
        return 'THURSDAY'
    if day_pos == 4:
        return 'FRIDAY'
    if day_pos == 5:
        return 'SATURDAY'
    return 'SUNDAY'
