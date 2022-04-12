import datetime

def ISO_string_from_date(date):
    dateStr = date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return dateStr

def date_from_string(dateStr):
    return datetime.datetime.strptime(dateStr, "%Y-%m-%d")