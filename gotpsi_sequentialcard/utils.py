import os
from datetime import datetime, timedelta


def find_missing_dates(folder_path):
    all_dates = set() #set of dates present

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue
        for filename in os.listdir(subfolder_path):
            if filename.endswith('.dat') and filename.startswith('cardS'):
                date_str = filename[5:11]  # extract YYMMDD
                try:
                    date = datetime.strptime(date_str, '%y%m%d').date()
                    all_dates.add(date)
                except ValueError:
                    continue

    if not all_dates:
        return [], None, None

    earliest_date = min(all_dates)
    latest_date = max(all_dates)

    # Find missing dates
    all_days = set()
    current = earliest_date
    while current <= latest_date:
        all_days.add(current)
        current += timedelta(days=1)

    missing_dates = sorted(all_days - all_dates)

    # Collapse consecutive missing dates into ranges
    missing_ranges = []
    if missing_dates:
        range_start = missing_dates[0]
        range_end = missing_dates[0]

        for date in missing_dates[1:]:
            if date == range_end + timedelta(days=1):
                range_end = date
            else:
                missing_ranges.append((range_start, range_end))
                range_start = date
                range_end = date

        missing_ranges.append((range_start, range_end))

    return missing_ranges, earliest_date, latest_date, all_dates