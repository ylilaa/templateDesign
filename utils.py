import re
from calendar import isleap


def get_days_in_year(dateString):
    leap = 365
    year_pattern = r"\d{4}"
    year = re.findall(year_pattern, str(dateString))
    if isleap(int(year[0])):
        leap = 366
    return leap
