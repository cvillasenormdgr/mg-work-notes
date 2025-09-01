import requests
from urllib.parse import urlencode
from collections import defaultdict

# Your Make webhook URL (configured to accept GET requests)
webhook_url = "https://hook.eu2.make.com/iyz8vmkeij3i689468wy0afnmw87gd6s"

# Send simple GET request
response = requests.get(webhook_url)


if response.status_code == 200:
    events = response.json()
    grouped = defaultdict(list)

    for event in events:
        summary = event['summary']
        if ':' in summary:
            # Split on the first colon only
            prefix, rest = summary.split(':', 1)
            grouped[prefix.strip()].append(rest.strip())
        else:
            grouped[summary].append(None)  # No sub-item

    markdown_lines = []
    for category, items in grouped.items():
        if all(item is None for item in items):
            # Just a standalone event
            markdown_lines.append(f"- {category}")
        else:
            markdown_lines.append(f"- {category}:")
            for item in items:
                if item:
                    markdown_lines.append(f"    - {item}")

    markdown = '\n'.join(markdown_lines)
    print(f"Events:\n{markdown}")

else:
    print(f"Error: {response.status_code}")