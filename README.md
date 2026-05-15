# EWS News RAG Agent Pipeline PoC



## 1. Project Overview



This project is a Proof of Concept for an AI Agent-based pipeline that collects, verifies, classifies, and stores construction-industry news articles for an Early Warning System, EWS.



The system starts from a natural language query such as:



> 오늘일자 기준으로 조중동의 건설경기 관련 뉴스 기사를 탐색해줘



Then it automatically performs:



1\. Natural language query parsing

2\. Google News RSS query planning

3\. Candidate news collection

4\. Google News URL resolution

5\. Original news URL verification

6\. Article metadata and body verification

7\. Rule-based risk event tagging

8\. NVIDIA NIM-based relevance judgement

9\. SQLite structured storage

10\. Chroma Vector DB storage

11\. RAG search

12\. Excel-style feasibility reflection

13\. Natural language response generation



## 2. Key Features



\- Natural language query-based news collection

\- Google News RSS candidate collection

\- Google News intermediate URL resolution

\- Original media URL verification

\- Domain validation for selected media outlets

\- Article metadata and body verification

\- Korean mojibake recovery using ftfy

\- Rule-based construction risk event tagging

\- NVIDIA NIM-based LLM judgement

\- Rate-limit-aware LLM call control

\- Rule-based fallback on LLM failure

\- SQLite storage for structured pipeline logs

\- Chroma Vector DB storage for verified articles

\- Natural language response generation

\- Excel feasibility report generation



## 3. Target Scenario



The main scenario is:



> 오늘일자 기준으로 조중동의 건설경기 관련 뉴스 기사를 탐색해줘



The agent interprets this as:



\- Date: today

\- Media outlets: 조선일보, 중앙일보, 동아일보

\- Keywords: 건설경기, 건설수주, 미분양, PF 부실, 공사비 상승, 건설투자, 주택시장



## 4. Architecture



```text

User Natural Language Query

→ NaturalLanguageQueryParserAgent

→ QueryPlanningAgent

→ RSSCandidateAgent

→ URLAccessAgent

→ ArticleVerificationAgent

→ RuleRiskEventAgent

→ NVIDIA NIM LLMJudgementAgent

→ CrossSourceCheckAgent

→ SQLiteStorageAgent

→ ChromaStorageAgent

→ ExcelReflectionAgent

→ Natural Language Response



## 5. Tech Stack



\- Python

\- Google Colab

\- LangGraph

\- Google News RSS

\- googlenewsdecoder

\- requests

\- BeautifulSoup

\- trafilatura

\- ftfy

\- NVIDIA NIM API

\- OpenAI-compatible API client

\- SQLite

\- ChromaDB

\- Sentence Transformers

\- pandas

\- openpyxl



## 6. Repository Structure



```text

ews-news-agent-poc/

│

├─ README.md

├─ requirements.txt

├─ .gitignore

├─ .env.example

│

├─ notebooks/

│  └─ refactored\_news\_agent\_colab.ipynb

│

├─ docs/

│  ├─ project\_overview.md

│  ├─ architecture.md

│  └─ execution\_guide.md

│

├─ outputs/

│  └─ .gitkeep

│

└─ assets/

&#x20;  └─ .gitkeep



## 7. How to Run



1\. Open `notebooks/refactored\_news\_agent\_colab.ipynb` in Google Colab.

2\. Install packages from the first cell.

3\. Enter your NVIDIA NIM API key when prompted.

4\. Run all definition cells.

5\. At the bottom of the notebook, enter a natural language query.

6\. Run the full pipeline.

7\. Check the natural language response, SQLite tables, Chroma search result, and Excel output.



## 8. Example Query



```text

오늘일자 기준으로 조중동의 건설경기 관련 뉴스 기사를 탐색해줘

## 9. Notes



This project is a PoC, not a production-grade news crawling system.



The pipeline does not store full article text in the Vector DB. It stores verified metadata, summaries, risk events, judgement reasons, and source URLs.



## 10. Future Improvements



\- Canonical URL-based duplicate removal

\- AMP URL normalization

\- Better date and author extraction

\- Stricter final response filtering

\- PostgreSQL migration

\- Scheduled execution with Airflow or Prefect

\- FastAPI-based API serving

\- Dashboard integration

