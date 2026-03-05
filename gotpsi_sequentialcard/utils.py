import os
from datetime import datetime, timedelta
from collections import namedtuple


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


Trial = namedtuple('Trial', ['userid', 'trial', 'target_card', 'click_sequence', 'image', 'timestamp'])

# Completed trial format:
#   userid, trial, steps, r1,r2,r3,r4,r5,r6, imagepath, timestamp
# Example: rada, 1, 2, 0,5,4,0,0,0, ../../bi/images4/c9.jpg, Thu Jan  1 00:05:52 2009
def parse_trial_file(filepath):
    trials = []
    
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if 'image' not in line:
                continue
            
            parts = [p.strip() for p in line.split(',')]
            assert len(parts)==11, parts
            
            userid = parts[0]
            trial_num = int(parts[1])
            steps = int(parts[2])
            clicks = [int(parts[i]) for i in range(3, 9)]  # r1 through r6
            imagepath = parts[9]
            timestamp_str = parts[10].strip()
            timestamp = datetime.strptime(timestamp_str, '%a %b %d %H:%M:%S %Y')
            
            image = os.path.basename(imagepath)
            
            # Validate: r1 should always be 0
            assert clicks[0] == 0, (
                f"Line {line_num}: expected r1=0, got {clicks[0]}"
            )
            
            # Validate: entries after 'steps' clicks should be 0
            trailing = clicks[steps + 1:]
            assert len(trailing)==0 or all(r == 0 for r in trailing), (
                f"Line {line_num}: expected trailing zeros after step {steps}, "
                f"got {clicks}"
            )
            
            # Extract meaningful click sequence; target card is the last click
            click_sequence = clicks[1:steps + 1]
            target_card = click_sequence[-1]
            
            trials.append(Trial(userid, trial_num, target_card, click_sequence, image, timestamp))
    
    return trials