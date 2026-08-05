# InsightGraph AI

**InsightGraph AI** is a production-style multi-agent AI research and analytics platform that transforms unstructured and structured data into reliable, evidence-backed insights. Built with **LangGraph**, the system orchestrates multiple specialized AI agents that collaborate to analyze documents, perform web research, process datasets, generate visualizations, fact-check information, and produce comprehensive reports.

## Live Demo

Live Application: https://insightgraph-ai.streamlit.app/

## Features

-  Multi-Agent AI workflow powered by LangGraph
-  Intelligent PDF document analysis
-  Real-time web research using Tavily Search
-  CSV data analysis with automated visualizations
-  Retrieval-Augmented Generation (RAG)
-  ChromaDB vector database for semantic search
-  AI-powered fact checking
-  Knowledge merging from multiple sources
-  Automated report generation
-  Export reports for sharing
-  Interactive Streamlit interface

---

## Architecture

The application follows a supervisor-agent architecture where a central orchestrator delegates tasks to specialized AI agents.

```
                    User Query
                         │
                         ▼
                  Supervisor Agent
                         │
 ┌───────────────┬──────────────┬───────────────┐
 ▼               ▼              ▼               ▼
PDF Agent    Web Agent     Data Agent   Visualization
     │             │             │             │
     └─────────────┴─────────────┴─────────────┘
                         │
                  Fact Checker
                         │
                  Knowledge Merger
                         │
                     Reviewer
                         │
                  Report Writer
                         │
                    Final Report
```

---

## AI Agents

### Supervisor Agent
Coordinates the workflow and routes tasks to the appropriate specialized agents.

### PDF Agent
Extracts and retrieves relevant information from uploaded PDF documents using RAG.

### Web Agent
Performs live web research and gathers up-to-date information.

### Data Agent
Processes CSV datasets, performs analysis, and extracts key insights.

### Visualization Agent
Creates charts and visual representations from structured data.

### Fact Checker
Verifies generated information against retrieved evidence.

### Knowledge Merger
Combines findings from documents, web research, and data analysis into a unified knowledge base.

### Reviewer
Reviews and improves the generated content before report creation.

### Report Writer
Produces a structured, comprehensive final report.

Then you can ask follow-up questions about the full project you have built...

---

## Technology Stack

### AI & LLM

- LangGraph
- LangChain
- OpenAI GPT
- Retrieval-Augmented Generation (RAG)

### Vector Database

- ChromaDB

### Backend

- Python
- Pandas

### Frontend

- Streamlit

### Search

- Tavily Search API

### Visualization

- Plotly
- Matplotlib

---

## Project Structure

```
InsightGraph-AI/
│
├── agents/
├── graph/
├── services/
├── tools/
├── prompts/
├── utils/
├── frontend/
├── data/
├── exports/
└── streamlit_app.py
```

---

## Installation

```bash
git clone https://github.com/efti-dot/InsightGraph-AI

cd InsightGraph-AI

pip install -r requirements.txt

streamlit run frontend/streamlit_app.py
```

---

## Author

**MD Iftekhar Hossain**

LinkedIn: https://www.linkedin.com/in/md-iftekhar-hossain-196ba32b9/?skipRedirect=true

GitHub: https://github.com/efti-dot
