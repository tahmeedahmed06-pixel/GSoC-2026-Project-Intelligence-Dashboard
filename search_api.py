import json
from pathlib import Path

from project_search import search_projects


DATASET_FILE = Path("gsoc_2026_dataset.json")


def load_projects():
    with DATASET_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def search(query, limit=20):
    """
    Search GSoC projects using the existing search engine
    and return JSON-friendly results.
    """

    parsed_query, results = search_projects(query, limit)

    output = []

    for score, project, reasons in results:

        output.append({
            "score": score,
            "title": project.get("title"),
            "organization": project.get(
                "organization_name"
            ),
            "technologies": project.get(
                "tech_tags", []
            ),
            "topics": project.get(
                "topic_tags", []
            ),
            "status": project.get("status"),
            "phase": project.get("phase"),
            "project_id": project.get("uid"),
            "project_url": (
                "https://summerofcode.withgoogle.com/"
                "programs/2026/projects/"
                f"{project.get('uid', '')}"
            ),
            "reasons": reasons
        })

    return {
        "query": query,
        "parsed_query": parsed_query,
        "count": len(output),
        "results": output
    }


if __name__ == "__main__":

    print("GSoC Search API Test")
    print("=" * 70)

    query = input("Query: ").strip()

    result = search(query)

    print()
    print(json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    ))