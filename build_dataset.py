import json

with open(
    "organizations.json",
    "r",
    encoding="utf-8"
) as file:
    organizations = json.load(file)

with open(
    "gsoc_projects.json",
    "r",
    encoding="utf-8"
) as file:
    projects = json.load(file)


# Create organization lookup table
org_lookup = {
    org["slug"]: org
    for org in organizations
}


# Add organization information to every project
for project in projects:

    slug = project.get("organization_slug")

    organization = org_lookup.get(slug)

    if organization:
        project["organization_categories"] = (
            organization.get("categories", [])
        )

        project["organization_tech_tags"] = (
            organization.get("tech_tags", [])
        )

        project["organization_topic_tags"] = (
            organization.get("topic_tags", [])
        )


with open(
    "gsoc_2026_dataset.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        projects,
        file,
        indent=2,
        ensure_ascii=False
    )


print("=" * 60)
print("GSoC 2026 MASTER DATASET")
print("=" * 60)

print(f"\nOrganizations: {len(organizations)}")
print(f"Projects: {len(projects)}")

print("\nSaved:")
print("gsoc_2026_dataset.json")