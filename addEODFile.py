import os
from datetime import datetime, timedelta
import calendar

def generate_eod_filenames(start_date=None):
    if not start_date:
        start_date = datetime.today()

    # Ensure start_date is a weekday (skip weekends)
    while start_date.weekday() > 4:
        start_date += timedelta(days=1)

    filenames = []
    for i in range(5):
        current = start_date + timedelta(days=i)
        if current.weekday() <= 4:
            date_str = current.strftime("%y%m%d")
            filenames.append(f"{date_str}EOD.md")
    return filenames


def get_month_and_week(today=None):
    if not today:
        today = datetime.today()

    # Month name (e.g. "September")
    month_name = today.strftime("%B")

    # First day of the month
    first_day = today.replace(day=1)

    # Find first Monday of the month
    first_monday = first_day
    while first_monday.weekday() != 0:  # 0 = Monday
        first_monday += timedelta(days=1)

    # How many weeks since the first Monday
    week_number = ((today - first_monday).days // 7) + 1

    return month_name, week_number


# === MAIN ===
today = datetime.today()
month_name, week_number = get_month_and_week(today)

folder_path = f"EOD/{today.strftime('%m')}{month_name}/Week {week_number}/"
os.makedirs(folder_path, exist_ok=True)

filenames = generate_eod_filenames(today)
content = "## Support Needed (3Ds):\n## Done:\n## To do:\n## Google Tasks:\n"

for name in filenames:
    file_path = os.path.join(folder_path, name)
    with open(file_path, 'w') as f:
        f.write(content)

print(f"Created {len(filenames)} files in: {folder_path}")
