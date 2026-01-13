import requests
from collections import defaultdict

# Your Make webhook URL (configured to accept GET requests)
webhook_url = "https://hook.eu2.make.com/iyz8vmkeij3i689468wy0afnmw87gd6s"

response = requests.get(webhook_url)

if response.status_code == 200:
    events = response.json()

    # Nested dict: {prefix: {subgroup: [items]}}
    grouped = defaultdict(lambda: defaultdict(list))

    for event in events:
        summary = event['summary'].strip()

        # Step 1: check if it starts with "XX-YY:"
        if "-" in summary and ":" in summary:
            prefix_part, rest = summary.split("-", 1)   # split WN-TL -> WN , TL: ...
            subgroup_part, *remaining = rest.split(":", 1)  # split TL: Task -> TL , Task
            prefix = prefix_part.strip()
            subgroup = subgroup_part.strip()
            item = remaining[0].strip() if remaining else None
            grouped[prefix][subgroup].append(item)

        else:
            # Fallback for events without this pattern
            grouped["Misc"][summary].append(None)

    # Now build markdown
    markdown_lines = []
    for prefix, subgroups in grouped.items():
        markdown_lines.append(f"- {prefix}:")
        for subgroup, items in subgroups.items():
            markdown_lines.append(f"  - {subgroup}:")
            for item in items:
                if item:
                    markdown_lines.append(f"    - {item}")

    markdown = "\n".join(markdown_lines)
    print(f"Events:\n{markdown}")

else:
    print(f"Error: {response.status_code}")