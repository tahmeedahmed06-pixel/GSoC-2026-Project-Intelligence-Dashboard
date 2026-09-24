import json
from collections import Counter, defaultdict


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

with open(
    "gsoc_2026_dataset.json",
    "r",
    encoding="utf-8"
) as file:
    projects = json.load(file)


print("=" * 70)
print("GSoC 2026 DATASET ANALYSIS")
print("=" * 70)

print(f"\nTotal projects: {len(projects)}")


# --------------------------------------------------
# 1. TECHNOLOGY FREQUENCY
# --------------------------------------------------

technology_counter = Counter()

for project in projects:

    for technology in project.get("tech_tags", []):
        technology_counter[technology.lower()] += 1


print("\n" + "=" * 70)
print("TOP TECHNOLOGIES")
print("=" * 70)

for rank, (technology, count) in enumerate(
    technology_counter.most_common(30),
    start=1
):
    print(
        f"{rank:2}. "
        f"{technology:<30} "
        f"{count:>4} projects"
    )


# --------------------------------------------------
# 2. TOPICS
# --------------------------------------------------

topic_counter = Counter()

for project in projects:

    for topic in project.get("topic_tags", []):
        topic_counter[topic.lower()] += 1


print("\n" + "=" * 70)
print("TOP TOPICS")
print("=" * 70)

for rank, (topic, count) in enumerate(
    topic_counter.most_common(30),
    start=1
):
    print(
        f"{rank:2}. "
        f"{topic:<30} "
        f"{count:>4} projects"
    )


# --------------------------------------------------
# 3. PROJECT SIZE
# --------------------------------------------------

size_counter = Counter(
    project.get("size", "unknown")
    for project in projects
)


print("\n" + "=" * 70)
print("PROJECT SIZE")
print("=" * 70)

for size, count in size_counter.items():

    percentage = (
        count / len(projects)
    ) * 100

    print(
        f"{size:<10} "
        f"{count:>4} "
        f"({percentage:.2f}%)"
    )


# --------------------------------------------------
# 4. ORGANIZATION PROJECT COUNT
# --------------------------------------------------

organization_counter = Counter(
    project.get("organization_name", "Unknown")
    for project in projects
)


print("\n" + "=" * 70)
print("TOP ORGANIZATIONS")
print("=" * 70)

for rank, (organization, count) in enumerate(
    organization_counter.most_common(30),
    start=1
):

    print(
        f"{rank:2}. "
        f"{organization:<55} "
        f"{count:>3}"
    )


# --------------------------------------------------
# 5. TECHNOLOGY × ORGANIZATION
# --------------------------------------------------

technology_organizations = defaultdict(set)

for project in projects:

    organization = project.get(
        "organization_name",
        "Unknown"
    )

    for technology in project.get(
        "tech_tags",
        []
    ):

        technology_organizations[
            technology.lower()
        ].add(organization)


print("\n" + "=" * 70)
print("TECHNOLOGY → ORGANIZATION COVERAGE")
print("=" * 70)

for technology, organizations in sorted(
    technology_organizations.items(),
    key=lambda item: len(item[1]),
    reverse=True
)[:30]:

    print(
        f"{technology:<30} "
        f"{len(organizations):>3} organizations"
    )


# --------------------------------------------------
# 6. YOUR CORE TECHNOLOGIES
# --------------------------------------------------

target_technologies = [
    "c",
    "c++",
    "rust",
    "llvm",
    "python",
    "go",
    "linux",
    "kernel",
    "assembly",
    "cuda",
    "docker",
]


print("\n" + "=" * 70)
print("TARGET TECHNOLOGY ANALYSIS")
print("=" * 70)


for target in target_technologies:

    matching_projects = []

    for project in projects:

        technologies = {
            technology.lower()
            for technology in project.get(
                "tech_tags",
                []
            )
        }

        if target in technologies:

            matching_projects.append(project)


    organizations = sorted({
        project.get(
            "organization_name",
            "Unknown"
        )
        for project in matching_projects
    })


    print(
        f"\n{target.upper()}"
    )

    print(
        f"Projects: {len(matching_projects)}"
    )

    print(
        f"Organizations: {len(organizations)}"
    )

    for organization in organizations[:15]:

        print(
            f"  - {organization}"
        )


# --------------------------------------------------
# 7. PROJECT STATUS
# --------------------------------------------------

status_counter = Counter(
    project.get("status", "unknown")
    for project in projects
)


print("\n" + "=" * 70)
print("PROJECT STATUS")
print("=" * 70)

for status, count in status_counter.items():

    print(
        f"{status:<25} "
        f"{count:>4}"
    )


print("\nAnalysis complete.")