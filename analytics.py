import json
from collections import Counter, defaultdict
from pathlib import Path


INPUT_FILE = Path("gsoc_2026_dataset.json")
OUTPUT_FILE = Path("heatmap_data.json")


def clean_values(values):
    """Return normalized non-empty strings."""
    if not values:
        return []

    return [
        str(value).strip().lower()
        for value in values
        if value and str(value).strip()
    ]


def sorted_counts(counter):
    """Convert Counter into a sorted list of dictionaries."""
    return [
        {
            "name": name,
            "count": count
        }
        for name, count in counter.most_common()
    ]


def convert_nested(mapping):
    """Convert nested Counters into JSON-friendly dictionaries."""
    result = {}

    for key, counter in mapping.items():
        result[key] = sorted_counts(counter)

    return result


def main():

    # =========================================================
    # LOAD DATASET
    # =========================================================

    print("=" * 70)
    print("GSoC 2026 ANALYTICS ENGINE")
    print("=" * 70)

    print(f"\nLoading: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        projects = json.load(f)

    if not isinstance(projects, list):
        raise TypeError(
            "Expected gsoc_2026_dataset.json to contain a list of projects."
        )

    print(f"Projects: {len(projects)}")

    # =========================================================
    # COUNTERS
    # =========================================================

    technology_counts = Counter()
    topic_counts = Counter()
    category_counts = Counter()

    status_counts = Counter()
    size_counts = Counter()
    phase_counts = Counter()

    organization_project_counts = Counter()

    # =========================================================
    # RELATIONSHIPS
    # =========================================================

    technology_organizations = defaultdict(Counter)
    organization_technologies = defaultdict(Counter)

    technology_topics = defaultdict(Counter)
    topic_technologies = defaultdict(Counter)

    organization_topics = defaultdict(Counter)
    topic_organizations = defaultdict(Counter)

    # =========================================================
    # ORGANIZATION METADATA
    # =========================================================

    organization_metadata = {}

    # =========================================================
    # PROCESS EVERY PROJECT
    # =========================================================

    for project in projects:

        organization = (
            project.get("organization_name")
            or project.get("organization_slug")
            or "unknown"
        )

        organization = str(organization).strip()

        technologies = clean_values(
            project.get("tech_tags")
        )

        topics = clean_values(
            project.get("topic_tags")
        )

        categories = clean_values(
            project.get("organization_categories")
        )

        # -----------------------------------------------------
        # Basic counts
        # -----------------------------------------------------

        technology_counts.update(technologies)
        topic_counts.update(topics)
        category_counts.update(categories)

        status = project.get("status")

        if status:
            status_counts[
                str(status).strip().lower()
            ] += 1

        size = project.get("size")

        if size:
            size_counts[
                str(size).strip().lower()
            ] += 1

        phase = project.get("phase")

        if phase:
            phase_counts[
                str(phase).strip().lower()
            ] += 1

        organization_project_counts[organization] += 1

        # -----------------------------------------------------
        # Save organization metadata
        # -----------------------------------------------------

        if organization not in organization_metadata:

            organization_metadata[organization] = {
                "slug": project.get("organization_slug"),
                "categories": categories,
                "technologies": clean_values(
                    project.get("organization_tech_tags")
                ),
                "topics": clean_values(
                    project.get("organization_topic_tags")
                )
            }

        # -----------------------------------------------------
        # Technology <-> Organization
        # -----------------------------------------------------

        for technology in technologies:

            technology_organizations[
                technology
            ][organization] += 1

            organization_technologies[
                organization
            ][technology] += 1

        # -----------------------------------------------------
        # Technology <-> Topic
        # -----------------------------------------------------

        for technology in technologies:

            for topic in topics:

                technology_topics[
                    technology
                ][topic] += 1

                topic_technologies[
                    topic
                ][technology] += 1

        # -----------------------------------------------------
        # Organization <-> Topic
        # -----------------------------------------------------

        for topic in topics:

            organization_topics[
                organization
            ][topic] += 1

            topic_organizations[
                topic
            ][organization] += 1

    # =========================================================
    # BUILD FINAL ANALYTICS OBJECT
    # =========================================================

    heatmap_data = {

        "metadata": {
            "dataset": "GSoC 2026",
            "total_projects": len(projects),
            "total_organizations": len(
                organization_project_counts
            )
        },

        "projects": {

            "total": len(projects),

            "status": sorted_counts(
                status_counts
            ),

            "size": sorted_counts(
                size_counts
            ),

            "phase": sorted_counts(
                phase_counts
            )
        },

        "organizations": {

            "total": len(
                organization_project_counts
            ),

            "project_counts": sorted_counts(
                organization_project_counts
            ),

            "categories": sorted_counts(
                category_counts
            ),

            "metadata": organization_metadata
        },

        "technologies": {

            "counts": sorted_counts(
                technology_counts
            )
        },

        "topics": {

            "counts": sorted_counts(
                topic_counts
            )
        },

        "relationships": {

            "technology_to_organization":
                convert_nested(
                    technology_organizations
                ),

            "organization_to_technology":
                convert_nested(
                    organization_technologies
                ),

            "technology_to_topic":
                convert_nested(
                    technology_topics
                ),

            "topic_to_technology":
                convert_nested(
                    topic_technologies
                ),

            "organization_to_topic":
                convert_nested(
                    organization_topics
                ),

            "topic_to_organization":
                convert_nested(
                    topic_organizations
                )
        }
    }

    # =========================================================
    # SAVE
    # =========================================================

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            heatmap_data,
            f,
            indent=2,
            ensure_ascii=False
        )

    # =========================================================
    # SUMMARY
    # =========================================================

    print("\n" + "=" * 70)
    print("ANALYTICS SUMMARY")
    print("=" * 70)

    print(
        f"\nTotal projects: {len(projects)}"
    )

    print(
        f"Total organizations: "
        f"{len(organization_project_counts)}"
    )

    print("\nTop technologies:")

    for item in sorted_counts(
        technology_counts
    )[:15]:

        print(
            f"  {item['name']:<25}"
            f"{item['count']:>5}"
        )

    print("\nTop topics:")

    for item in sorted_counts(
        topic_counts
    )[:15]:

        print(
            f"  {item['name']:<25}"
            f"{item['count']:>5}"
        )

    print("\nTop organizations:")

    for item in sorted_counts(
        organization_project_counts
    )[:15]:

        print(
            f"  {item['name']:<45}"
            f"{item['count']:>5}"
        )

    print("\nProject status:")

    for item in sorted_counts(
        status_counts
    ):

        print(
            f"  {item['name']:<20}"
            f"{item['count']:>5}"
        )

    print("\nProject size:")

    for item in sorted_counts(
        size_counts
    ):

        percentage = (
            item["count"]
            / len(projects)
            * 100
        )

        print(
            f"  {item['name']:<20}"
            f"{item['count']:>5}"
            f" ({percentage:.2f}%)"
        )

    print("\n" + "=" * 70)
    print(
        f"Saved analytics to: {OUTPUT_FILE}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()