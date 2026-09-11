<div align="center">

# 🔬 ResearchMind: Multi-Agent Autonomous Research System

**An autonomous multi-agent pipeline that conducts real-time web intelligence gathering, deep content extraction, structured technical synthesis, and automated peer review.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-8E75B2.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain-1C3C3C.svg?logo=chainlink)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/rpmakki03/Multi-agent-research-system/pulls)

[Live Architecture](#-system-architecture) •
[Features](#-key-features) •
[Quickstart](#-quickstart-guide) •
[Agent Roles](#-agent-specifications) •
[Sample Output](examples/sample_report.md)

</div>

---

## 💡 Overview

Modern LLMs struggle with hallucinations, stale knowledge cutoffs, and unstructured outputs when handling open-ended technical research. **ResearchMind** addresses this by decomposing complex research tasks into a coordinated, multi-agent workflow powered by **Google Gemini** models:

1. **Search Agent**: Formulates queries and gathers real-time search index snippets via Tavily API.
2. **Reader Agent**: Autonomously selects high-signal URLs, crawls the DOM, decomposes boilerplate/scripts, and extracts dense technical context.
3. **Writer Chain**: Synthesizes verified findings into a structured research report with citations and executive summary.
4. **Critic Chain**: Evaluates the drafted report against strict evaluation rubrics (scoring 1-10, strengths, gaps, and verdict) for automated quality assurance.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    User([User Prompt / Research Topic]) --> WebUI[Streamlit Interactive UI]
    WebUI --> Orchestrator[Research Pipeline Orchestrator]

    subgraph Agentic Pipeline
        direction TB
        Orchestrator --> Agent1[1. Search Agent\n(Tavily Search Tool)]
        Agent1 -->|SERP Snippets & URLs| Agent2[2. Reader Agent\n(DOM Crawler & Cleaner)]
        Agent2 -->|Cleaned Deep Content| Agent3[3. Writer Chain\n(Report Synthesis)]
        Agent3 -->|Draft Research Report| Agent4[4. Critic Chain\n(Quality Review & Scoring)]
    end

    Agent4 -->|Final Report + Critic Feedback| OutputPanel[Interactive UI & Markdown Export]
```

### State Flow & Data Contract

| Stage | Input | Agent / Chain | Output |
| :--- | :--- | :--- | :--- |
| **01. Search** | Topic query | Search Agent (`gemini-1.5-flash` + Tavily) | Top 5 SERP titles, URLs, and contextual snippets |
| **02. Deep Read** | SERP results + Topic | Reader Agent (`gemini-1.5-flash` + Web Scraper) | Sanitized 3,000-char DOM text extraction |
| **03. Synthesis** | Search + Scraped Text | Writer Chain (`gemini-1.5-flash` + Prompt Template) | Formatted Markdown report with sources |
| **04. Peer Review**| Draft Report | Critic Chain (`gemini-1.5-flash` + Evaluation Rubric) | Score (X/10), Strengths, Improvement Areas, Verdict |

---

## ✨ Key Features

- **Decoupled Multi-Agent Architecture**: Replaces monolithic prompting with specialized, tool-augmented agents that each handle a single responsibility.
- **Anti-Hallucination Grounding**: Combines live SERP results with direct web crawling (`BeautifulSoup4`), ensuring claims are backed by verifiable sources.
- **Real-Time Pipeline Observability**: Streamlit dashboard provides visual step cards showing `WAITING`, `RUNNING`, and `DONE` states in real time.
- **Automated Peer Review & Scoring**: Integrated self-critique loop evaluates reports across accuracy, comprehensiveness, and structural clarity.
- **Export Ready**: Generated reports can be downloaded instantly as formatted `.md` documents.
- **Dual Execution Interfaces**: Full support for both a web-based dashboard (`app.py`) and a terminal CLI pipeline (`pipeline.py`).

---

## 📁 Repository Structure

```text
Multi-agent-research-system/
├── app.py                  # Streamlit web dashboard with custom dark glassmorphic UI
├── pipeline.py             # CLI runner and sequential pipeline orchestrator
├── agents.py               # Agent definitions, prompt templates, and chain setups
├── tools.py                # Tavily search and BeautifulSoup4 scraping tools
├── requirements.txt        # Production dependencies with pinned version ranges
├── .env.example            # Template for required environment variables
├── LICENSE                 # MIT Open Source License
├── tests/                  # Automated test suite
│   ├── __init__.py
│   ├── test_tools.py       # Unit tests for web search and URL scraping
│   └── test_pipeline.py    # Unit tests for output parsing and state transitions
└── examples/
    └── sample_report.md    # Sample agentic research report output
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository

```bash
git clone https://github.com/rpmakki03/Multi-agent-research-system.git
cd Multi-agent-research-system
```

### 2. Create and Activate a Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Populate `.env` with your API credentials:

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=tvly-...
GEMINI_MODEL=gemini-1.5-flash
```

> **API Key Providers**:
> - [Google AI Studio (Gemini API Key)](https://aistudio.google.com/app/apikey) (Free tier available)
> - [Tavily Search API Key](https://tavily.com/) (1,000 free monthly queries)

---

## 🖥️ Running the Application

### Option A: Interactive Web UI (Recommended)

Launch the Streamlit web dashboard:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`, enter a research topic, and click **⚡ Run Research Pipeline**.

### Option B: Command Line Interface (CLI)

Run the autonomous pipeline directly from your terminal:

```bash
python pipeline.py
```

---

## 🧪 Running Tests

Execute the automated test suite with pytest:

```bash
pytest tests/ -v
```

---

## 📄 Example Research Output

Check out [`examples/sample_report.md`](examples/sample_report.md) for an unedited sample output generated by ResearchMind on *Quantum Computing Advancements*.

---

## 💼 Resume Highlights (For Software / AI Engineers)

If you are showcasing this project on your resume or portfolio, here are suggested bullet points:

- **Built an autonomous multi-agent research pipeline** using LangChain, Google Gemini (1.5 Flash), and Tavily API that decomposes open-ended topics into search, web scraping, synthesis, and critique phases.
- **Engineered an anti-hallucination web-grounding engine** with BeautifulSoup4 to scrape, clean, and extract dense contextual text from primary web sources.
- **Implemented an automated evaluation loop (Critic Chain)** scoring draft research across factual accuracy, structure, and depth with actionable feedback.
- **Designed a real-time reactive dashboard** in Streamlit with asynchronous step tracking, markdown rendering, and instant export capability.

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.