import re
from datetime import datetime

def get_datetime_from_group_date_string(group_date_string: str) -> datetime:
    timestamp = int(re.search(r'-?\d+', group_date_string).group())
    milliseconds = int(timestamp / 1000)
    if milliseconds < 0:
        formatted_date = datetime.now()
    else:
        formatted_date = datetime.fromtimestamp(milliseconds)
    return formatted_date