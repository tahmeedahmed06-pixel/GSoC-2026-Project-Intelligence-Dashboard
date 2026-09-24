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


# --------------------------------------------------
# BUILD TECHNOLOGY SETS
# --------------------------------------------------

project_technologies = []

for project in projects:

    technologies = {
        technology.lower().strip()
        for technology in project.get(
            "tech_tags",
            []
        )
    }

    project_technologies.append(
        technologies
    )


# --------------------------------------------------
# TECHNOLOGY FREQUENCY
# --------------------------------------------------

technology_counter = Counter()

for technologies in project_technologies:

    for technology in technologies:

        technology_counter[
            technology
        ] += 1


# --------------------------------------------------
# TECHNOLOGY PAIRS
# --------------------------------------------------

pair_counter = Counter()

for technologies in project_technologies:

    technologies = sorted(technologies)

    for i in range(len(technologies)):

        for j in range(
            i + 1,
            len(technologies)
        ):

            pair = (
                technologies[i],
                technologies[j]
            )

            pair_counter[pair] += 1


# --------------------------------------------------
# PRINT
# --------------------------------------------------

print("=" * 70)
print("GSoC 2026 TECHNOLOGY RELATIONSHIP ANALYSIS")
print("=" * 70)

print(
    f"\nProjects analyzed: {len(projects)}"
)


print("\n" + "=" * 70)
print("MOST COMMON TECHNOLOGY PAIRS")
print("=" * 70)


for rank, (
    pair,
    count
) in enumerate(
    pair_counter.most_common(50),
    start=1
):

    tech_a, tech_b = pair

    print(
        f"{rank:2}. "
        f"{tech_a:<25} + "
        f"{tech_b:<25} "
        f"{count:>3} projects"
    )


# --------------------------------------------------
# YOUR TECHNOLOGY ECOSYSTEM
# --------------------------------------------------

targets = [
    "c++",
    "c",
    "rust",
    "llvm",
    "linux",
    "kernel",
    "assembly",
    "cmake",
    "cuda",
]


print("\n" + "=" * 70)
print("TARGET TECHNOLOGY RELATIONSHIPS")
print("=" * 70)


for target in targets:

    related = []

    for (
        pair,
        count
    ) in pair_counter.items():

        if target in pair:

            other = (
                pair[1]
                if pair[0] == target
                else pair[0]
            )

            related.append(
                (
                    other,
                    count
                )
            )


    related.sort(
        key=lambda item: item[1],
        reverse=True
    )


    print(
        f"\n{target.upper()}"
    )

    for (
        technology,
        count
    ) in related[:15]:

        print(
            f"  {technology:<25} "
            f"{count:>3} projects"
        )


print("\nAnalysis complete.")