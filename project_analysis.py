import json


with open(
    "organization_projects.json",
    "r",
    encoding="utf-8"
) as file:
    organizations = json.load(file)


# Sort organizations by project count
organizations.sort(
    key=lambda org: org["project_count"],
    reverse=True
)


print("=" * 60)
print("GSoC 2026 PROJECT DISTRIBUTION")
print("=" * 60)

print(
    f"\nOrganizations: {len(organizations)}"
)


total_projects = sum(
    org["project_count"]
    for org in organizations
)

print(f"Total projects: {total_projects}")


print("\nTOP ORGANIZATIONS BY PROJECT COUNT")
print("-" * 60)


for rank, organization in enumerate(
    organizations[:30],
    start=1
):

    print(
        f"{rank:2}. "
        f"{organization['name']:<55} "
        f"{organization['project_count']:>2}"
    )