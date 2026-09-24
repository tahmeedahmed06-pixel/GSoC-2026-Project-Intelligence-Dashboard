import json
from collections import Counter


INPUT_FILE = "organizations.json"


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    organizations = json.load(file)


print("=" * 60)
print("GSoC 2026 ORGANIZATION ANALYZER")
print("=" * 60)

print(f"\nTotal organizations: {len(organizations)}")


# --------------------------------------------------
# 1. Categories
# --------------------------------------------------

category_counter = Counter()

for organization in organizations:
    for category in organization["categories"]:
        category_counter[category] += 1


print("\nTOP CATEGORIES")
print("-" * 60)

for category, count in category_counter.most_common():
    print(f"{category}: {count}")


# --------------------------------------------------
# 2. Technologies
# --------------------------------------------------

technology_counter = Counter()

for organization in organizations:
    for technology in organization["tech_tags"]:
        technology_counter[technology] += 1


print("\nTOP TECHNOLOGIES")
print("-" * 60)

for technology, count in technology_counter.most_common():
    print(f"{technology}: {count}")


# --------------------------------------------------
# 3. Topic tags
# --------------------------------------------------

topic_counter = Counter()

for organization in organizations:
    for topic in organization["topic_tags"]:
        topic_counter[topic] += 1


print("\nTOP TOPICS")
print("-" * 60)

for topic, count in topic_counter.most_common(30):
    print(f"{topic}: {count}")