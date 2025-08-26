import os
from datetime import datetime, timedelta

def generate_eod_filenames(start_date=None):
    if not start_date:
      start_date = datetime.today()
    
    while start_date.weekday() > 4:
      start_date += timedelta(days=1)

    filenames = []

    for i in range(5):
      current = start_date + timedelta(days=i)
      if current.weekday() <= 4:
        date_str = current.strftime("%y%m%d")
        filenames.append(f"{date_str}EOD.md")

    return filenames

folder_path = "EOD/08August/Week 4/"

os.makedirs(folder_path, exist_ok=True)

filenames = generate_eod_filenames()
content = "## Support Needed (3Ds):\n## Done:\n## To do:\n## Google Tasks:\n"

for name in filenames:
    file_path = os.path.join(folder_path, name)
    with open(file_path, 'w') as f:
        f.write(f"{content}")

print(f"Created {len(filenames)} files in: {folder_path}")
