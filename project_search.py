import json
import re


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_FILE = "gsoc_2026_dataset.json"
DEFAULT_LIMIT = 10


# ============================================================
# LOAD DATASET
# ============================================================

with open(DATASET_FILE, "r", encoding="utf-8") as f:
    projects = json.load(f)

print(f"Loaded {len(projects)} projects.")


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize(text):
    """
    Normalize text for searching.

    Example:
        "LLVM Compiler" -> "llvm compiler"
    """

    if text is None:
        return ""

    return str(text).lower().strip()


# ============================================================
# SEARCH FIELDS
# ============================================================

def get_search_fields(project):
    """
    Extract all searchable fields from a project.
    """

    return {
        "title": normalize(
            project.get("title", "")
        ),

        "organization": normalize(
            project.get("organization_name", "")
        ),

        "body": normalize(
            project.get("body", "")
        ),

        "body_short": normalize(
            project.get("body_short", "")
        ),

        "technologies": [
            normalize(x)
            for x in project.get("tech_tags", [])
        ],

        "topics": [
            normalize(x)
            for x in project.get("topic_tags", [])
        ],

        "status": normalize(
            project.get("status", "")
        ),

        "phase": normalize(
            project.get("phase", "")
        ),
    }


# ============================================================
# QUERY PARSER
# ============================================================

def parse_query(query):
    """
    Convert a user query into structured components.

    Supported:

        LLVM

        C++ Linux

        C++ AND Linux

        Rust OR C++

        "machine learning"

        technology:rust

        topic:compiler

        organization:LLVM

        status:active

        technology:rust topic:compiler
    """

    query = query.strip()

    # --------------------------------------------------------
    # Extract quoted phrases
    # --------------------------------------------------------

    phrases = re.findall(
        r'"([^"]+)"',
        query
    )

    # Remove quoted phrases from the remaining query
    remaining = re.sub(
        r'"[^"]+"',
        "",
        query
    )

    # --------------------------------------------------------
    # Tokenize
    # --------------------------------------------------------

    tokens = remaining.split()

    terms = []

    operators = []

    filters = []

    i = 0

    while i < len(tokens):

        token = tokens[i].strip()

        if not token:
            i += 1
            continue

        upper = token.upper()

        # ----------------------------------------------------
        # Operators
        # ----------------------------------------------------

        if upper in ("AND", "OR"):

            operators.append(
                upper
            )

            i += 1
            continue

        # ----------------------------------------------------
        # Filters
        # ----------------------------------------------------

        if ":" in token:

            field, value = token.split(
                ":",
                1
            )

            field = field.lower().strip()
            value = value.lower().strip()

            allowed_fields = {
                "technology",
                "tech",
                "topic",
                "organization",
                "org",
                "status",
                "phase",
            }

            if (
                field in allowed_fields
                and value
            ):

                filters.append(
                    {
                        "field": field,
                        "value": value,
                    }
                )

            else:

                # Unknown field:
                # treat it as a normal search term
                terms.append(
                    token.lower()
                )

        else:

            terms.append(
                token.lower()
            )

        i += 1

    return {
        "terms": terms,
        "phrases": [
            normalize(x)
            for x in phrases
        ],
        "operators": operators,
        "filters": filters,
    }


# ============================================================
# FILTER MATCHING
# ============================================================

def filter_matches(fields, filter_item):
    """
    Check whether a project satisfies one filter.
    """

    field = filter_item["field"]
    value = filter_item["value"]

    # --------------------------------------------------------
    # Technology
    # --------------------------------------------------------

    if field in ("technology", "tech"):

        return any(
            value == technology
            for technology in fields["technologies"]
        )

    # --------------------------------------------------------
    # Topic
    # --------------------------------------------------------

    if field == "topic":

        return any(
            value == topic
            for topic in fields["topics"]
        )

    # --------------------------------------------------------
    # Organization
    # --------------------------------------------------------

    if field in ("organization", "org"):

        return (
            value
            in fields["organization"]
        )

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    if field == "status":

        return (
            fields["status"]
            == value
        )

    # --------------------------------------------------------
    # Phase
    # --------------------------------------------------------

    if field == "phase":

        return (
            fields["phase"]
            == value
        )

    return False


# ============================================================
# TERM SCORING
# ============================================================

def term_score(term, fields):
    """
    Calculate relevance for one search term.

    Stronger signals receive higher scores.
    """

    score = 0

    reasons = []

    # --------------------------------------------------------
    # Exact technology
    # --------------------------------------------------------

    if term in fields["technologies"]:

        score += 50

        reasons.append(
            f"technology: {term}"
        )

    # --------------------------------------------------------
    # Exact topic
    # --------------------------------------------------------

    if term in fields["topics"]:

        score += 40

        reasons.append(
            f"topic: {term}"
        )

    # --------------------------------------------------------
    # Exact title
    # --------------------------------------------------------

    if term == fields["title"]:

        score += 50

        reasons.append(
            "exact title"
        )

    elif term in fields["title"]:

        score += 25

        reasons.append(
            "title"
        )

    # --------------------------------------------------------
    # Organization
    # --------------------------------------------------------

    if term in fields["organization"]:

        score += 15

        reasons.append(
            "organization"
        )

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    occurrences = fields["body"].count(
        term
    )

    if occurrences:

        description_score = min(
            occurrences,
            10
        )

        score += description_score

        reasons.append(
            f"description: "
            f"{occurrences} occurrence(s)"
        )

    return score, reasons


# ============================================================
# PHRASE SCORING
# ============================================================

def phrase_score(phrase, fields):
    """
    Score an exact quoted phrase.
    """

    score = 0

    reasons = []

    # --------------------------------------------------------
    # Exact title phrase
    # --------------------------------------------------------

    if phrase == fields["title"]:

        score += 60

        reasons.append(
            f'exact title phrase: "{phrase}"'
        )

    elif phrase in fields["title"]:

        score += 40

        reasons.append(
            f'title phrase: "{phrase}"'
        )

    # --------------------------------------------------------
    # Technology phrase
    # --------------------------------------------------------

    if phrase in fields["technologies"]:

        score += 50

        reasons.append(
            f'technology phrase: "{phrase}"'
        )

    # --------------------------------------------------------
    # Topic phrase
    # --------------------------------------------------------

    if phrase in fields["topics"]:

        score += 45

        reasons.append(
            f'topic phrase: "{phrase}"'
        )

    # --------------------------------------------------------
    # Description phrase
    # --------------------------------------------------------

    occurrences = fields["body"].count(
        phrase
    )

    if occurrences:

        score += min(
            occurrences * 5,
            20
        )

        reasons.append(
            f'description phrase: '
            f'{occurrences} occurrence(s)'
        )

    return score, reasons


# ============================================================
# PROJECT MATCHING + SCORING
# ============================================================

def score_project(project, parsed_query):

    fields = get_search_fields(
        project
    )

    total_score = 0

    reasons = []

    terms = parsed_query["terms"]

    phrases = parsed_query["phrases"]

    filters = parsed_query["filters"]

    operators = parsed_query["operators"]

    # ========================================================
    # FILTERS
    # ========================================================

    for filter_item in filters:

        if not filter_matches(
            fields,
            filter_item
        ):

            return 0, []

        total_score += 100

        reasons.append(
            f"filter: "
            f"{filter_item['field']}"
            f"={filter_item['value']}"
        )

    # ========================================================
    # PHRASES
    # ========================================================

    for phrase in phrases:

        score, phrase_reasons = phrase_score(
            phrase,
            fields
        )

        if score == 0:

            return 0, []

        total_score += score

        reasons.extend(
            phrase_reasons
        )

    # ========================================================
    # TERMS
    # ========================================================

    term_scores = []

    for term in terms:

        score, term_reasons = term_score(
            term,
            fields
        )

        term_scores.append(score)

        # ----------------------------------------------------
        # AND behavior
        # ----------------------------------------------------

        if (
            operators
            and "OR" not in operators
        ):

            if score == 0:

                return 0, []

        else:

            # Default behavior for multiple terms:
            # AND

            if len(terms) > 1:

                if score == 0:

                    return 0, []

        total_score += score

        reasons.extend(
            term_reasons
        )

    # ========================================================
    # OR SUPPORT
    # ========================================================

    if "OR" in operators:

        if terms:

            if not any(
                score > 0
                for score in term_scores
            ):

                return 0, []

            # Remove the strict AND requirement
            # by recalculating using matching terms.

            total_score = 0

            reasons = []

            # Filters
            total_score += (
                len(filters) * 100
            )

            # Phrases
            for phrase in phrases:

                score, phrase_reasons = phrase_score(
                    phrase,
                    fields
                )

                if score > 0:

                    total_score += score

                    reasons.extend(
                        phrase_reasons
                    )

            # Matching terms
            for term in terms:

                score, term_reasons = term_score(
                    term,
                    fields
                )

                if score > 0:

                    total_score += score

                    reasons.extend(
                        term_reasons
                    )

    # ========================================================
    # MULTI-TERM BONUS
    # ========================================================

    matching_terms = sum(
        score > 0
        for score in term_scores
    )

    if len(terms) > 1:

        total_score += (
            matching_terms * 10
        )

    # ========================================================
    # RETURN
    # ========================================================

    return total_score, reasons


# ============================================================
# SEARCH
# ============================================================

def search_projects(query, limit=DEFAULT_LIMIT):

    parsed_query = parse_query(
        query
    )

    results = []

    for project in projects:

        score, reasons = score_project(
            project,
            parsed_query
        )

        if score > 0:

            results.append(
                (
                    score,
                    project,
                    reasons
                )
            )

    # Highest score first
    results.sort(
        reverse=True,
        key=lambda item: item[0]
    )

    return (
        parsed_query,
        results[:limit]
    )


# ============================================================
# PRINT PARSED QUERY
# ============================================================

def print_parsed_query(parsed_query):

    print()
    print("Parsed query:")

    print(
        f"  Terms: "
        f"{parsed_query['terms']}"
    )

    print(
        f"  Phrases: "
        f"{parsed_query['phrases']}"
    )

    print(
        f"  Operators: "
        f"{parsed_query['operators']}"
    )

    print(
        f"  Filters: "
        f"{parsed_query['filters']}"
    )


# ============================================================
# PRINT RESULTS
# ============================================================

def print_results(
    query,
    parsed_query,
    results
):

    print()
    print("=" * 70)

    print(
        f"SEARCH: {query}"
    )

    print("=" * 70)

    print_parsed_query(
        parsed_query
    )

    print()

    if not results:

        print(
            "No matching projects found."
        )

        return

    print(
        f"Found {len(results)} "
        f"top results."
    )

    print()

    for index, (
        score,
        project,
        reasons
    ) in enumerate(
        results,
        1
    ):

        print(
            f"{index}. "
            f"{project.get('title', 'Unknown')}"
        )

        print(
            "   Organization: "
            f"{project.get('organization_name', 'Unknown')}"
        )

        technologies = project.get(
            "tech_tags",
            []
        )

        topics = project.get(
            "topic_tags",
            []
        )

        print(
            "   Technologies: "
            + ", ".join(
                technologies
            )
        )

        print(
            "   Topics: "
            + ", ".join(
                topics
            )
        )

        print(
            f"   Score: {score}"
        )

        print(
            "   Why:"
        )

        for reason in reasons:

            print(
                f"      - {reason}"
            )

        print(
            "   Project ID: "
            f"{project.get('uid', 'Unknown')}"
        )

        print(
            "   Status: "
            f"{project.get('status', 'Unknown')}"
        )

        print(
            "   URL: "
            "https://summerofcode.withgoogle.com/"
            "programs/2026/projects/"
            f"{project.get('uid', '')}"
        )

        print(
            "-" * 70
        )


# ============================================================
# HELP
# ============================================================

def print_help():

    print()

    print("=" * 70)
    print("SEARCH HELP")
    print("=" * 70)

    print()

    print("Basic search:")
    print("  LLVM")
    print("  Python")
    print("  compiler")

    print()

    print("AND search:")
    print("  C++ Linux")
    print("  Rust LLVM")
    print("  Python Django")

    print()

    print("Explicit AND:")
    print("  C++ AND Linux")

    print()

    print("OR search:")
    print("  Rust OR C++")

    print()

    print("Exact phrase:")
    print('  "machine learning"')

    print()

    print("Technology filter:")
    print("  technology:rust")
    print("  technology:c++")

    print()

    print("Topic filter:")
    print("  topic:compiler")
    print("  topic:robotics")

    print()

    print("Organization filter:")
    print("  organization:LLVM")
    print("  org:rust")

    print()

    print("Status filter:")
    print("  status:active")
    print("  status:passed")

    print()

    print("Combined:")
    print(
        "  technology:rust topic:compiler"
    )

    print(
        "  technology:c++ topic:systems"
    )

    print()

    print("Commands:")
    print("  help")
    print("  exit")

    print()


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("GSoC 2026 PROJECT SEARCH ENGINE")
    print("=" * 70)

    print()

    print(
        f"Total projects: {len(projects)}"
    )

    print()

    print("Examples:")

    print("  LLVM")
    print("  Rust LLVM")
    print("  C++ Linux")
    print("  Python")
    print("  machine learning")
    print("  compiler")

    print()

    print(
        "Type 'help' for advanced search."
    )

    print(
        "Type 'exit' to quit."
    )

    print()

    while True:

        try:

            query = input(
                "Search> "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print()
            print("Exiting.")
            break

        if not query:
            continue

        if query.lower() == "exit":

            print(
                "Goodbye."
            )

            break

        if query.lower() == "help":

            print_help()

            continue

        parsed_query, results = search_projects(
            query
        )

        print_results(
            query,
            parsed_query,
            results
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()