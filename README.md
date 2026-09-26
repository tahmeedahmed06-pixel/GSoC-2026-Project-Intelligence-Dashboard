# GSoC 2026 Project Intelligence Dashboard

A data-driven analysis and search platform for exploring the **Google Summer of Code (GSoC) 2026 public project ecosystem**.

This project collects publicly available GSoC organization and project data, builds a structured dataset, analyzes technologies and topics, and provides an interactive dashboard with a project search engine and ecosystem heatmap.

---

## Overview

Finding suitable GSoC projects can be difficult when hundreds of organizations and projects are involved.

This project transforms publicly available GSoC 2026 data into an explorable dataset and interactive dashboard.

It can answer questions such as:

- Which technologies appear most frequently?
- Which topics are most common?
- Which organizations have the most projects?
- Which organizations work with a particular technology?
- Which projects involve Rust, C++, LLVM, Python, Linux, Docker, or other technologies?
- Which projects match a combination of technologies or topics?

The project combines:

**Web Data Collection → Dataset Construction → Data Analysis → Search Engine → REST API → Interactive Dashboard**

---

## Important: What the Heatmap Represents

The heatmap in this project is **not a visitor click heatmap**.

The project does not have access to Google's private website analytics or other visitors' individual browsing and click data.

Instead, the heatmap represents relationships within the **public GSoC project ecosystem**.

For example, it can visualize relationships between:

- Organizations
- Technologies
- Projects
- Topics

Therefore, this project should be understood as a:

> **GSoC opportunity and ecosystem analysis dashboard**

rather than a visitor-behavior analytics system.

---

## Data Source

The project uses publicly accessible GSoC 2026 information exposed by the Google Summer of Code website.

The data collection process uses public website data and publicly accessible API endpoints.

No attempt is made to access private analytics, authentication-protected information, or other users' private activity.

---

## Dataset

The collected dataset contains information about GSoC 2026 organizations and projects.

Current collected statistics:

| Metric | Count |
|---|---:|
| Organizations | 183 |
| Public project records | 1,102 |

Project records contain fields such as:

- Project title
- Project description
- Organization
- Technologies
- Topics
- Project status
- Project phase
- Project size
- Project length
- Mentors
- Contributor information where publicly available
- Project URLs
- Organization metadata

---

## Technology Analysis

Some of the most frequently occurring technologies in the collected dataset include:

| Technology | Projects |
|---|---:|
| Python | 461 |
| C++ | 165 |
| JavaScript | 140 |
| TypeScript | 125 |
| Docker | 115 |
| C | 112 |
| Java | 75 |
| React | 75 |
| Git | 72 |
| Rust | 72 |
| PyTorch | 67 |
| GitHub Actions | 65 |
| PostgreSQL | 64 |
| Django | 57 |
| NumPy | 55 |

These counts are based on the collected public project dataset.

---

## Topic Analysis

Frequently occurring project topics include:

- Machine Learning
- Web
- Open Source
- Scientific Computing
- Security
- Web Development
- Testing
- Developer Tools
- Networking
- Systems Programming
- Deep Learning
- DevOps
- CI/CD
- Artificial Intelligence
- Data Visualization

---

## Dashboard Features

### Summary Statistics

The dashboard displays:

- Total projects
- Total organizations
- Number of technologies
- Number of topics

### Technology × Organization Heatmap

The dashboard visualizes relationships between technologies and organizations.

This makes it possible to explore which organizations are associated with particular technology ecosystems.

### Technology Analysis

Displays frequently occurring technologies across the collected projects.

### Organization Analysis

Displays organizations according to their number of projects in the collected dataset.

### Topic Analysis

Displays frequently occurring topics across projects.

### Project Search

The dashboard includes a custom search engine for finding projects using:

- Normal text
- Technologies
- Topics
- Organizations
- Status
- AND queries
- OR queries
- Exact phrases

---

## Search Engine

The project includes a custom Python search engine.

### Basic Search

```text
Rust
```

```text
LLVM
```

```text
C++ Linux
```

### AND Search

```text
C++ AND Linux
```

### OR Search

```text
Rust OR C++
```

### Phrase Search

```text
"machine learning"
```

### Technology Filter

```text
technology:rust
```

or:

```text
tech:rust
```

### Topic Filter

```text
topic:compiler
```

### Organization Filter

```text
organization:LLVM
```

or:

```text
org:LLVM
```

### Status Filter

```text
status:active
```

### Combined Search

Filters can be combined with normal search terms.

Example:

```text
technology:rust topic:compiler
```

The search engine ranks matching projects using factors including:

- Technology matches
- Topic matches
- Title matches
- Organization matches
- Description matches
- Exact phrase matches

---

## Architecture

```text
                    GSoC 2026 Public Data
                              |
                              v
                 +------------------------+
                 |    Data Collection     |
                 |  Playwright / APIs     |
                 +-----------+------------+
                             |
                             v
                 +------------------------+
                 | Dataset Construction   |
                 |       JSON Data        |
                 +-----------+------------+
                             |
                  +----------+----------+
                  |                     |
                  v                     v
        +------------------+   +------------------+
        |  Data Analysis   |   | Project Search   |
        |   analytics.py   |   | project_search.py|
        +--------+---------+   +--------+---------+
                 |                      |
                 +----------+-----------+
                            |
                            v
                  +--------------------+
                  |     Flask API      |
                  |     server.py      |
                  +---------+----------+
                            |
                            v
                  +--------------------+
                  | Interactive        |
                  | Dashboard          |
                  +--------------------+
```

---

## Project Structure

```text
website-scanner/
│
├── scanner.py
├── api_inspector.py
├── org_inspector.py
├── crawl_organizations.py
│
├── analyze.py
├── project_analysis.py
├── project_inspector.py
├── all_projects_api.py
├── build_dataset.py
├── dataset_analysis.py
├── technology_graph.py
├── analytics.py
│
├── project_search.py
├── search_api.py
├── server.py
│
├── dashboard.py
├── dashboard.html
│
├── organizations.json
├── organization_projects.json
├── gsoc_projects.json
├── gsoc_2026_dataset.json
├── heatmap_data.json
│
├── .gitignore
└── README.md
```

---

## Main Components

### `scanner.py`

Initial Playwright-based inspection of the GSoC website.

### `api_inspector.py`

Inspects publicly accessible GSoC API endpoints.

### `org_inspector.py`

Inspects organization-level information.

### `crawl_organizations.py`

Crawls GSoC organization pages and collects project information.

### `build_dataset.py`

Builds the structured GSoC project dataset.

### `analytics.py`

Analyzes the project dataset and generates data used by the dashboard.

### `project_analysis.py`

Performs additional project-level analysis.

### `dataset_analysis.py`

Analyzes the collected dataset.

### `technology_graph.py`

Builds technology relationship data.

### `project_search.py`

Implements the custom project search engine and query parser.

### `search_api.py`

Connects the search engine to the web API.

### `server.py`

Runs the Flask backend and exposes the search API and dashboard.

### `dashboard.py`

Generates the interactive dashboard.

### `dashboard.html`

Generated dashboard interface.

---

## Technologies Used

### Programming Languages

- Python
- JavaScript

### Data Collection

- Playwright
- Requests
- Public REST APIs

### Backend

- Flask

### Frontend

- HTML
- CSS
- JavaScript

### Data Processing

- JSON
- Python-based analysis

### Version Control

- Git
- GitHub

---

## Requirements

- Python 3.12+
- Playwright
- Flask
- Requests
- Chromium

---

## Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd website-scanner
```

Create a virtual environment:

### Windows

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install playwright flask requests
```

Install Chromium for Playwright:

```powershell
python -m playwright install chromium
```

---

## Running the Dashboard

Generate the dashboard:

```powershell
python dashboard.py
```

Start the Flask server:

```powershell
python server.py
```

Open the dashboard:

```text
http://127.0.0.1:5000/
```

---

## API

### Search

Example:

```text
http://127.0.0.1:5000/api/search?q=Rust
```

Another example:

```text
http://127.0.0.1:5000/api/search?q=Rust%20LLVM
```

### Health Check

```text
http://127.0.0.1:5000/api/health
```

---

## Running the Data Collection Pipeline

Individual components can be executed separately.

Initial website inspection:

```powershell
python scanner.py
```

Inspect the public API:

```powershell
python api_inspector.py
```

Inspect organizations:

```powershell
python org_inspector.py
```

Crawl organizations:

```powershell
python crawl_organizations.py
```

Build the project dataset:

```powershell
python build_dataset.py
```

Run analytics:

```powershell
python analytics.py
```

The exact execution order may depend on which part of the dataset needs to be regenerated.

---

## Key Findings

Analysis of the collected dataset shows a broad technology ecosystem across GSoC 2026 projects.

Some notable observations include:

- Python appears across a large portion of the collected project ecosystem.
- C and C++ remain strongly represented.
- Rust appears across multiple organizations and project areas.
- Machine learning is one of the most common project topics.
- Web development and scientific computing represent substantial parts of the dataset.
- Infrastructure technologies such as Docker and CI/CD tooling appear frequently.
- Organizations have substantially different technology and topic profiles.

These observations describe the collected public dataset.

They should not be interpreted as:

- Official GSoC rankings
- Organization quality rankings
- Selection predictions
- Acceptance probabilities

---

## Limitations

### Public Data Only

The project only uses publicly accessible information.

It does not attempt to access:

- Private Google Analytics data
- Individual visitor histories
- Other users' clicks
- Private contributor information
- Authentication-protected analytics
- Restricted APIs

### Dataset Coverage

The public project endpoint contained 1,102 project records during collection, while the GSoC program statistics showed a larger allocated-project count.

Therefore, these numbers should not be treated as identical measures.

### Dynamic Website

The GSoC website is dynamic and its API structure may change.

If Google changes the website or API structure, the collection scripts may require updates.

### Search Ranking

The search engine uses a custom relevance-scoring system.

Search scores are used for ordering results and should not be interpreted as official GSoC project quality or relevance scores.

---

## Project Motivation

The original idea behind this project was to investigate whether a website could provide a heatmap showing where users interact most.

During development, it became clear that real visitor click and heatmap data requires access to the website owner's analytics or an equivalent publicly exposed dataset.

Instead of attempting to obtain private analytics, the project was redesigned around a public-data problem:

> Can publicly available GSoC data be transformed into a searchable map of the open-source project ecosystem?

The result is an end-to-end system combining:

- Web inspection
- API discovery
- Data collection
- Web crawling
- Dataset engineering
- Data analysis
- Search algorithms
- REST APIs
- Interactive visualization

---

## Future Improvements

Possible future extensions include:

- More advanced search ranking
- Additional project filters
- Organization-specific dashboards
- Project comparison
- Technology trend analysis
- Historical GSoC dataset comparison
- Network graphs between technologies and organizations
- Exportable analysis reports
- Deployment as a public web application

These are optional extensions and are not required for the current version.

---

## Disclaimer

This is an independent analysis project built using publicly available GSoC information.

It is not affiliated with or endorsed by Google or the Google Summer of Code program.

The dashboard heatmap represents relationships within the publicly collected project ecosystem and does **not** represent private website visitor behavior or click activity.

---

## License

No license has been selected for this project yet.
