import json
from pathlib import Path


INPUT_FILE = Path("heatmap_data.json")
OUTPUT_FILE = Path("dashboard.html")


def main():

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    metadata = data["metadata"]

    technologies = data["technologies"]["counts"]
    organizations = data["organizations"]["project_counts"]

    tech_org = data["relationships"]["technology_to_organization"]

    # ---------------------------------------------------------
    # Top-level heatmap
    # ---------------------------------------------------------

    top_technologies = technologies[:20]
    top_organizations = organizations[:30]

    tech_names = [
        item["name"]
        for item in top_technologies
    ]

    org_names = [
        item["name"]
        for item in top_organizations
    ]

    matrix = []

    for organization in org_names:

        organization_data = {}

        for technology, entries in tech_org.items():

            for entry in entries:

                if entry["name"] == organization:

                    organization_data[
                        technology
                    ] = entry["count"]

                    break

        row = [
            organization_data.get(
                technology,
                0
            )
            for technology in tech_names
        ]

        matrix.append(row)

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    tech_stats = technologies[:30]

    org_stats = organizations[:30]

    topic_stats = data[
        "topics"
    ]["counts"][:30]

    # ---------------------------------------------------------
    # Data passed to browser
    # ---------------------------------------------------------

    dashboard_data = {

        "metadata": metadata,

        "technologyStats": tech_stats,

        "organizationStats": org_stats,

        "topicStats": topic_stats,

        "technologyNames": tech_names,

        "organizationNames": org_names,

        "matrix": matrix
    }

    data_json = json.dumps(
        dashboard_data,
        ensure_ascii=False
    )

    # ---------------------------------------------------------
    # HTML
    # ---------------------------------------------------------

    html = f"""<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>GSoC 2026 Opportunity Heatmap</title>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;

    font-family:
        Inter,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background: #0b1020;

    color: #e8ecf7;
}}

header {{

    padding:
        30px 42px 24px;

    border-bottom:
        1px solid #252c42;
}}

h1 {{
    margin: 0;

    font-size: 30px;
}}

.subtitle {{

    margin-top: 8px;

    color: #9ba6c1;
}}

.container {{

    padding:
        28px 42px 50px;
}}

/* =========================================================
   SEARCH
   ========================================================= */

.search-panel {{

    background: #12182a;

    border:
        1px solid #252c42;

    border-radius: 12px;

    padding: 20px;

    margin-bottom: 24px;
}}

.search-row {{

    display: flex;

    gap: 10px;
}}

.search-input {{

    flex: 1;

    padding:
        13px 15px;

    border:
        1px solid #303951;

    border-radius: 8px;

    background: #0b1020;

    color: #ffffff;

    font-size: 15px;

    outline: none;
}}

.search-input:focus {{

    border-color:
        #6366f1;
}}

button {{

    border: none;

    border-radius: 8px;

    padding:
        0 20px;

    background:
        #6366f1;

    color: white;

    font-weight: 600;

    cursor: pointer;
}}

button:hover {{

    background:
        #4f46e5;
}}

.reset-button {{

    background:
        #252c42;
}}

.reset-button:hover {{

    background:
        #303951;
}}

.search-info {{

    margin-top: 12px;

    color:
        #9ba6c1;

    font-size: 13px;
}}


/* =========================================================
   CARDS
   ========================================================= */

.cards {{

    display: grid;

    grid-template-columns:
        repeat(4, minmax(150px, 1fr));

    gap: 16px;

    margin-bottom: 24px;
}}

.card {{

    background: #12182a;

    border:
        1px solid #252c42;

    border-radius: 12px;

    padding: 20px;
}}

.card-label {{

    color:
        #8e99b5;

    font-size: 13px;
}}

.card-value {{

    margin-top: 8px;

    font-size: 28px;

    font-weight: 700;
}}


/* =========================================================
   PANELS
   ========================================================= */

.panel {{

    background:
        #12182a;

    border:
        1px solid #252c42;

    border-radius: 12px;

    margin-bottom: 24px;

    overflow: hidden;
}}

.panel-header {{

    padding:
        18px 22px;

    border-bottom:
        1px solid #252c42;
}}

.panel-title {{

    font-size: 18px;

    font-weight: 650;
}}

.panel-description {{

    color:
        #8e99b5;

    font-size: 13px;

    margin-top: 5px;
}}

.chart {{

    width: 100%;

    height: 500px;
}}

.two-column {{

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 24px;
}}

/* =========================================================
   SEARCH RESULTS
   ========================================================= */

.results-container {{

    padding:
        10px 22px 22px;

}}


.result {{

    position: relative;

    padding:
        18px 4px 20px;

    border-bottom:
        1px solid #252c42;

    transition:
        background 0.2s ease;

}}


.result:last-child {{

    border-bottom:
        none;

}}


.result:hover {{

    background:
        rgba(99, 102, 241, 0.04);

}}


.result-title {{

    padding-right:
        80px;

    font-size:
        16px;

    font-weight:
        650;

    line-height:
        1.45;

    color:
        #e8ecf7;

}}


.result-org {{

    margin-top:
        6px;

    color:
        #818cf8;

    font-size:
        13px;

    font-weight:
        600;

}}


.result-meta {{

    margin-top:
        10px;

    color:
        #9ba6c1;

    font-size:
        12px;

    line-height:
        1.8;

}}


.result-link {{

    display:
        inline-block;

    margin-top:
        10px;

    color:
        #818cf8;

    font-size:
        12px;

    font-weight:
        600;

    text-decoration:
        none;

}}


.result-link:hover {{

    text-decoration:
        underline;

}}


.score {{

    float:
        right;

    padding:
        4px 8px;

    border:
        1px solid
        rgba(245, 158, 11, 0.25);

    border-radius:
        6px;

    background:
        rgba(245, 158, 11, 0.08);

    color:
        #f59e0b;

    font-size:
        11px;

    font-weight:
        650;

}}

/* =========================================================
   NOTE
   ========================================================= */

.note {{

    padding:
        18px 22px;

    color:
        #9ba6c1;

    font-size: 13px;

    line-height: 1.6;
}}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {{

    .cards {{

        grid-template-columns:
            repeat(2, 1fr);
    }}

    .two-column {{

        grid-template-columns:
            1fr;
    }}

    .container {{

        padding:
            20px;
    }}

    header {{

        padding:
            25px 20px;
    }}

    .search-row {{

        flex-direction:
            column;
    }}

    button {{

        height:
            44px;
    }}
}}

</style>

</head>


<body>


<header>

<h1>
GSoC 2026 Opportunity Heatmap
</h1>

<div class="subtitle">

Public-data analysis of GSoC 2026 projects,
organizations, technologies and topics

</div>

</header>


<div class="container">


<!-- ===================================================== -->
<!-- SEARCH -->
<!-- ===================================================== -->

<div class="search-panel">

<div class="search-row">

<input
    id="searchInput"
    class="search-input"
    type="text"
    placeholder="Search projects... e.g. Rust LLVM"
>

<button onclick="performSearch()">
Search
</button>

<button
    class="reset-button"
    onclick="resetSearch()"
>
Reset
</button>

</div>


<div
    id="searchInfo"
    class="search-info"
>
Search across the GSoC 2026 project dataset.
</div>

</div>


<!-- ===================================================== -->
<!-- SUMMARY -->
<!-- ===================================================== -->

<div class="cards">


<div class="card">

<div class="card-label">
Projects
</div>

<div
    class="card-value"
    id="projectCount"
>
</div>

</div>


<div class="card">

<div class="card-label">
Organizations
</div>

<div
    class="card-value"
    id="organizationCount"
>
</div>

</div>


<div class="card">

<div class="card-label">
Technologies
</div>

<div
    class="card-value"
    id="technologyCount"
>
</div>

</div>


<div class="card">

<div class="card-label">
Topics
</div>

<div
    class="card-value"
    id="topicCount"
>
</div>

</div>


</div>


<!-- ===================================================== -->
<!-- HEATMAP -->
<!-- ===================================================== -->

<div class="panel">

<div class="panel-header">

<div class="panel-title">
Technology × Organization
</div>

<div
    class="panel-description"
    id="heatmapDescription"
>

Number of GSoC 2026 projects connecting
each technology with each organization.

</div>

</div>


<div
    id="heatmap"
    class="chart"
>
</div>

</div>


<!-- ===================================================== -->
<!-- SEARCH RESULTS -->
<!-- ===================================================== -->

<div
    class="panel"
    id="resultsPanel"
    style="display:none;"
>

<div class="panel-header">

<div class="panel-title">
Matching Projects
</div>

<div class="panel-description">
Projects returned by the GSoC search engine.
</div>

</div>


<div
    id="results"
    class="results-container"
>
</div>

</div>


<!-- ===================================================== -->
<!-- STATISTICS -->
<!-- ===================================================== -->

<div class="two-column">


<div class="panel">

<div class="panel-header">

<div class="panel-title">
Top Technologies
</div>

<div class="panel-description">
Number of projects tagged with each technology.
</div>

</div>


<div
    id="technologies"
    class="chart"
>
</div>

</div>


<div class="panel">

<div class="panel-header">

<div class="panel-title">
Top Organizations
</div>

<div class="panel-description">
Number of projects associated with each organization.
</div>

</div>


<div
    id="organizations"
    class="chart"
>
</div>

</div>


</div>


<!-- ===================================================== -->
<!-- TOPICS -->
<!-- ===================================================== -->

<div class="panel">

<div class="panel-header">

<div class="panel-title">
Top Topics
</div>

<div class="panel-description">
Number of GSoC 2026 projects associated with each topic.
</div>

</div>


<div
    id="topics"
    class="chart"
>
</div>

</div>


<!-- ===================================================== -->
<!-- NOTE -->
<!-- ===================================================== -->

<div class="panel">

<div class="note">

<strong>Important:</strong>

This dashboard does not represent actual visitor
clicks, Google Analytics data, or the number of people
viewing an organization.

The heat intensity represents the number of publicly
available GSoC 2026 projects connecting two entities.

It is therefore an
<strong>opportunity / ecosystem heatmap</strong>,
not a visitor-behavior heatmap.

</div>

</div>


</div>


<script>


const DATA = {data_json};


// ========================================================
// SUMMARY
// ========================================================

function setOverallStats() {{

    document.getElementById(
        "projectCount"
    ).textContent =
        DATA.metadata.total_projects
        .toLocaleString();


    document.getElementById(
        "organizationCount"
    ).textContent =
        DATA.metadata.total_organizations
        .toLocaleString();


    document.getElementById(
        "technologyCount"
    ).textContent =
        DATA.technologyStats.length
        .toLocaleString();


    document.getElementById(
        "topicCount"
    ).textContent =
        DATA.topicStats.length
        .toLocaleString();

}}


setOverallStats();


// ========================================================
// PLOT CONFIG
// ========================================================

const CONFIG = {{

    responsive: true,

    displaylogo: false

}};


// ========================================================
// COMMON LAYOUT
// ========================================================

function baseLayout() {{

    return {{

        paper_bgcolor:
            "#12182a",

        plot_bgcolor:
            "#12182a",

        font: {{

            color:
                "#dbe4ff"

        }}

    }};

}}


// ========================================================
// BUILD HEATMAP
// ========================================================

function buildHeatmap(

    organizations,

    technologies,
    matrix,
    title

) {{

    Plotly.react(

        "heatmap",

        [{{

            z: matrix,

            x: technologies,

            y: organizations,

            type: "heatmap",

            hovertemplate:

                "<b>%{{y}}</b><br>" +

                "Technology: %{{x}}<br>" +

                "Projects: %{{z}}" +

                "<extra></extra>",

            colorscale: [

                [0, "#111827"],

                [0.2, "#1e3a5f"],

                [0.4, "#2563eb"],

                [0.7, "#7c3aed"],

                [1, "#f59e0b"]

            ],

            showscale: true

        }}],

        {{

            ...baseLayout(),

            margin: {{

                l: 240,

                r: 40,

                t: 30,

                b: 130

            }},

            xaxis: {{

                title:
                    "Technology",

                tickangle:
                    -45

            }},

            yaxis: {{

                title:
                    "Organization",

                autorange:
                    "reversed"

            }}

        }},

        CONFIG

    );

}}


// ========================================================
// ORIGINAL HEATMAP
// ========================================================

buildHeatmap(

    DATA.organizationNames,

    DATA.technologyNames,

    DATA.matrix,

    "Technology × Organization"

);


// ========================================================
// TECHNOLOGY CHART
// ========================================================

Plotly.newPlot(

    "technologies",

    [{{

        x: DATA.technologyStats
            .map(x => x.count)
            .reverse(),

        y: DATA.technologyStats
            .map(x => x.name)
            .reverse(),

        type:
            "bar",

        orientation:
            "h",

        hovertemplate:

            "<b>%{{y}}</b><br>" +

            "Projects: %{{x}}" +

            "<extra></extra>"

    }}],

    {{

        ...baseLayout(),

        margin: {{

            l: 110,

            r: 30,

            t: 20,

            b: 40

        }},

        xaxis: {{

            title:
                "Projects"

        }}

    }},

    CONFIG

);


// ========================================================
// ORGANIZATION CHART
// ========================================================

Plotly.newPlot(

    "organizations",

    [{{

        x: DATA.organizationStats
            .map(x => x.count)
            .reverse(),

        y: DATA.organizationStats
            .map(x => x.name)
            .reverse(),

        type:
            "bar",

        orientation:
            "h",

        hovertemplate:

            "<b>%{{y}}</b><br>" +

            "Projects: %{{x}}" +

            "<extra></extra>"

    }}],

    {{

        ...baseLayout(),

        margin: {{

            l: 230,

            r: 30,

            t: 20,

            b: 40

        }},

        xaxis: {{

            title:
                "Projects"

        }}

    }},

    CONFIG

);


// ========================================================
// TOPIC CHART
// ========================================================

Plotly.newPlot(

    "topics",

    [{{

        x: DATA.topicStats
            .map(x => x.count)
            .reverse(),

        y: DATA.topicStats
            .map(x => x.name)
            .reverse(),

        type:
            "bar",

        orientation:
            "h",

        hovertemplate:

            "<b>%{{y}}</b><br>" +

            "Projects: %{{x}}" +

            "<extra></extra>"

    }}],

    {{

        ...baseLayout(),

        margin: {{

            l: 160,

            r: 30,

            t: 20,

            b: 40

        }},

        xaxis: {{

            title:
                "Projects"

        }}

    }},

    CONFIG

);


// ========================================================
// SEARCH
// ========================================================

async function performSearch() {{

    const input =
        document.getElementById(
            "searchInput"
        );

    const query =
        input.value.trim();


    if (!query) {{

        resetSearch();

        return;

    }}


    const info =
        document.getElementById(
            "searchInfo"
        );


    info.textContent =
        "Searching...";


    try {{

        const response =
            await fetch(

                "http://127.0.0.1:5000/api/search?q=" +
                encodeURIComponent(query)

            );


        const result =
            await response.json();


        if (!response.ok) {{

            throw new Error(
                result.error ||
                "Search failed"
            );

        }}


        displaySearchResults(
            result
        );


        buildFilteredHeatmap(
            result.results,
            query
        );


    }} catch (error) {{

        info.textContent =
            "Error: " +
            error.message;

    }}

}}


// ========================================================
// DISPLAY SEARCH RESULTS
// ========================================================

function displaySearchResults(result) {{

    const panel =
        document.getElementById(
            "resultsPanel"
        );

    const container =
        document.getElementById(
            "results"
        );

    const info =
        document.getElementById(
            "searchInfo"
        );


    panel.style.display =
        "block";


    info.textContent =
        `Found ${{result.count}} matching projects`;


    container.innerHTML = "";


    if (!result.results.length) {{

        container.innerHTML =
            "<div class='result'>" +
            "No matching projects found." +
            "</div>";

        return;

    }}


    for (
        const project
        of result.results
    ) {{

        const div =
            document.createElement(
                "div"
            );


        div.className =
            "result";


        const technologies =
            project.technologies
                .join(", ");


        const topics =
            project.topics
                .join(", ");


        div.innerHTML = `

            <div class="result-title">

                ${{escapeHtml(
                    project.title
                )}}

                <span class="score">
                    Score: ${{project.score}}
                </span>

            </div>


            <div class="result-org">

                ${{escapeHtml(
                    project.organization
                )}}

            </div>


            <div class="result-meta">

                Technologies:
                ${{escapeHtml(
                    technologies
                )}}

                <br>

                Topics:
                ${{escapeHtml(
                    topics
                )}}

                <br>

                Status:
                ${{escapeHtml(
                    project.status
                )}}

            </div>


            <a
                class="result-link"
                href="${{project.project_url}}"
                target="_blank"
            >
                Open GSoC project →
            </a>

        `;


        container.appendChild(
            div
        );

    }}

}}


// ========================================================
// BUILD FILTERED HEATMAP
// ========================================================

function buildFilteredHeatmap(
    results,
    query
) {{

    if (!results.length) {{

        document.getElementById(
            "heatmapDescription"
        ).textContent =
            "No projects matched the search.";

        buildHeatmap(
            [],
            [],
            [],
            query
        );

        return;

    }}


    const organizationCounts =
        {{}};


    const technologyCounts =
        
        {{}};

    const relationships =
        {{}};


    // -----------------------------------------------------
    // Collect entities
    // -----------------------------------------------------

    for (
        const project
        of results
    ) {{

        const organization =
            project.organization;


        organizationCounts[
            organization
        ] =
            (
                organizationCounts[
                    organization
                ] || 0
            ) + 1;


        for (
            const technology
            of project.technologies
        ) {{

            const normalized =
                technology
                    .toLowerCase()
                    .trim();


            technologyCounts[
                normalized
            ] =
                (
                    technologyCounts[
                        normalized
                    ] || 0
                ) + 1;


            if (
                !relationships[
                    organization
                ]
            ) {{

                relationships[
                    organization
                ] = {{}};

            }}


            relationships[
                organization
            ][
                normalized
            ] =
                (
                    relationships[
                        organization
                    ][
                        normalized
                    ] || 0
                ) + 1;

        }}

    }}


    // -----------------------------------------------------
    // Sort organizations
    // -----------------------------------------------------

    const organizations =
        Object.entries(
            organizationCounts
        )
        .sort(
            (a, b) =>
                b[1] - a[1]
        )
        .map(
            x => x[0]
        );


    // -----------------------------------------------------
    // Sort technologies
    // -----------------------------------------------------

    const technologies =
        Object.entries(
            technologyCounts
        )
        .sort(
            (a, b) =>
                b[1] - a[1]
        )
        .map(
            x => x[0]
        );


    // -----------------------------------------------------
    // Build matrix
    // -----------------------------------------------------

    const matrix =
        organizations.map(
            organization =>

                technologies.map(
                    technology =>

                        (
                            relationships[
                                organization
                            ] || {{}}
                        )[technology] || 0

                )
        );


    document.getElementById(
        "heatmapDescription"
    ).textContent =

        `Filtered heatmap for "${{query}}" — ` +

        `${{results.length}} matching projects`;


    buildHeatmap(
        organizations,
        technologies,
        matrix,
        query
    );

}}


// ========================================================
// RESET
// ========================================================

function resetSearch() {{

    document.getElementById(
        "searchInput"
    ).value = "";


    document.getElementById(
        "searchInfo"
    ).textContent =

        "Search across the GSoC 2026 project dataset.";


    document.getElementById(
        "resultsPanel"
    ).style.display =
        "none";


    document.getElementById(
        "heatmapDescription"
    ).textContent =

        "Number of GSoC 2026 projects connecting " +
        "each technology with each organization.";


    buildHeatmap(

        DATA.organizationNames,

        DATA.technologyNames,

        DATA.matrix,

        "Technology × Organization"

    );

}}


// ========================================================
// ENTER KEY
// ========================================================

document.getElementById(
    "searchInput"
)
.addEventListener(
    "keydown",
    function(event) {{

        if (
            event.key ===
            "Enter"
        ) {{

            performSearch();

        }}

    }}
);


// ========================================================
// HTML ESCAPE
// ========================================================

function escapeHtml(value) {{

    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}}


</script>

</body>

</html>
"""


    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)


    print("=" * 70)
    print("DASHBOARD GENERATED")
    print("=" * 70)
    print()
    print(f"Input : {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print()
    print("Open dashboard.html in your browser.")
    print("=" * 70)


if __name__ == "__main__":
    main()