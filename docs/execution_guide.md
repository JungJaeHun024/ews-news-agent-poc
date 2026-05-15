\# Execution Guide



본 문서는 `refactored\_news\_agent\_colab.ipynb` 노트북을 Google Colab에서 실행하는 방법과 실행 결과를 확인하는 기준을 정리한 문서이다.



본 프로젝트는 건설산업 EWS 비정형 언론보도 데이터의 수집가능성, 원문 접근성, 메타데이터 확보 가능성, 위험 이벤트 추출 가능성, RAG 적재 가능성을 검증하기 위한 PoC이다.



\## 1. 실행 환경



본 프로젝트는 Google Colab 환경을 기준으로 작성되었다.



주요 실행 환경은 다음과 같다.



\- Python

\- Google Colab

\- NVIDIA NIM API

\- SQLite

\- ChromaDB

\- Google News RSS



\## 2. 사전 준비



실행 전 다음 항목을 준비한다.



\- Google Colab 실행 환경

\- NVIDIA NIM API Key

\- GitHub에서 다운로드한 프로젝트 노트북

\- 인터넷 연결 환경



NVIDIA NIM API Key는 GitHub에 업로드하지 않는다.



API Key는 노트북 실행 중 입력하거나 Colab 환경변수로 설정한다.



\## 3. 노트북 위치



실행 대상 노트북은 다음 경로에 위치한다.



`notebooks/refactored\_news\_agent\_colab.ipynb`



Google Colab에서 해당 노트북을 열고 위에서부터 순서대로 실행한다.



\## 4. 패키지 설치



노트북의 첫 번째 패키지 설치 셀을 실행한다.



주요 설치 패키지는 다음과 같다.



\- langgraph

\- feedparser

\- requests

\- beautifulsoup4

\- lxml

\- pandas

\- openpyxl

\- chromadb

\- sentence-transformers

\- googlenewsdecoder

\- trafilatura

\- ftfy

\- openai



\## 5. NVIDIA NIM API Key 설정



노트북 실행 중 NVIDIA NIM API Key를 입력한다.



본 프로젝트에서는 NVIDIA NIM API를 다음 용도로 사용한다.



\- 자연어 질의 파싱

\- 기사 관련성 판단

\- 위험 이벤트 요약

\- 판단 근거 생성



API Key는 `.env`, 노트북 출력, GitHub repository에 포함하지 않는다.



\## 6. 기본 실행 순서



노트북은 다음 순서로 실행한다.



1\. 패키지 설치

2\. import 및 warning 설정

3\. NVIDIA NIM API Key 설정

4\. 공통 설정값 정의

5\. 유틸 함수 정의

6\. 자연어 질의 Parser 정의

7\. 기사 메타데이터 및 본문 추출 함수 정의

8\. 위험 이벤트 사전 정의

9\. SQLite 스키마 생성 함수 정의

10\. LangGraph State 정의

11\. Agent Node 정의

12\. Workflow Compile

13\. 사용자 자연어 질의 입력

14\. Agent Pipeline 실행

15\. SQLite 결과 확인

16\. Chroma RAG 검색 테스트

17\. Excel 결과 파일 생성

18\. 자연어 응답 결과 확인



\## 7. 예시 질의



다음과 같은 자연어 질의를 입력할 수 있다.



\- 오늘일자 기준으로 조중동의 건설경기 관련 뉴스 기사를 탐색해줘

\- 2026년 5월 13일 기준으로 조선일보와 동아일보의 미분양 관련 뉴스를 찾아줘

\- 오늘 기준으로 중앙일보의 PF 부실과 공사비 상승 관련 기사를 수집해서 검증해줘

\- 어제 기준으로 조중동의 주택시장 위험 관련 뉴스를 찾아줘



\## 8. 자연어 질의 처리 방식



사용자 질의는 다음과 같은 구조화된 조건으로 변환된다.



\- 기준일자

\- 대상 언론사

\- 검색 키워드

\- 수집 작업 조건



예를 들어 다음 질의는:



오늘일자 기준으로 조중동의 건설경기 관련 뉴스 기사를 탐색해줘



다음과 같이 해석된다.



\- 기준일자: 오늘

\- 언론사: 조선일보, 중앙일보, 동아일보

\- 키워드: 건설경기, 건설수주, 미분양, PF 부실, 공사비 상승, 건설투자, 주택시장



\## 9. Agent Pipeline 처리 흐름



전체 Agent Pipeline은 다음 순서로 실행된다.



1\. 사용자 자연어 질의 입력

2\. 자연어 질의 파싱

3\. 수집 조건 CONFIG 생성

4\. Google News RSS 검색 작업 생성

5\. 후보 기사 수집

6\. Google News 중간 URL 원문 변환

7\. 원문 URL 접근성 검증

8\. 기사 메타데이터 및 본문 검증

9\. 규칙 기반 위험 이벤트 태깅

10\. NVIDIA NIM 기반 관련성 판단

11\. 위험 이벤트 교차확인

12\. SQLite 저장

13\. Chroma Vector DB 저장

14\. Excel 검토표 생성

15\. 자연어 응답 출력



\## 10. 주요 결과 확인 항목



실행 후 다음 지표를 확인한다.



\- 수집 후보 수

\- 접근 가능 URL 수

\- 실제 기사 수

\- 본문 확인 기사 수

\- NVIDIA NIM 판단 성공 수

\- Chroma 저장 수

\- 관련 기사 목록

\- SQLite 테이블 생성 여부

\- Chroma RAG 검색 결과

\- Excel 결과 파일 생성 여부



\## 11. SQLite 결과 확인



SQLite에는 Agent Pipeline의 단계별 결과가 저장된다.



주요 테이블은 다음과 같다.



\- search\_tasks

\- article\_candidates

\- article\_access\_checks

\- article\_metadata

\- rule\_risk\_events

\- llm\_judgements

\- cross\_source\_checks



SQLite 저장 결과를 통해 각 후보 기사가 어느 단계에서 통과 또는 제외되었는지 추적할 수 있다.



\## 12. Chroma RAG 검색 확인



ChromaDB에는 검증 기준을 통과한 기사만 저장된다.



저장 기준은 다음과 같다.



\- 원문 URL 접근 가능

\- 언론사 도메인 일치

\- 실제 기사 여부 확인

\- 본문 존재

\- 관련성 판단 통과

\- Google News 중간 URL 제외



ChromaDB에는 기사 전문 전체를 저장하지 않고, RAG 활용에 필요한 메타데이터와 요약 정보를 중심으로 저장한다.



\## 13. Excel 결과 확인



노트북 실행 후 Excel 결과 파일이 생성될 수 있다.



Excel 결과 파일에는 다음과 같은 sheet가 포함된다.



\- 01\_search\_tasks

\- 02\_candidates

\- 03\_access\_checks

\- 04\_article\_metadata

\- 05\_rule\_events

\- 06\_llm\_judgements

\- 07\_cross\_source

\- 08\_excel\_reflection

\- 09\_pipeline\_diagnosis



Excel 결과는 수집가능성 검토표와 실행 진단 결과를 확인하기 위한 산출물이다.



\## 14. 실행 결과 예시



정상 실행 시 다음과 같은 요약 결과를 확인할 수 있다.



\- 수집 후보 수: 60

\- 접근 가능 URL 수: 60

\- 실제 기사 수: 23

\- 본문 확인 기사 수: 23

\- NVIDIA NIM 판단 성공 수: 15

\- Chroma 저장 수: 6



위 수치는 실행 시점, 검색 결과, API 응답 상태에 따라 달라질 수 있다.



\## 15. 주의사항



본 프로젝트 실행 시 다음 사항에 유의한다.



\- 본 프로젝트는 PoC이며 운영 시스템이 아니다.

\- Google News RSS 결과는 시간에 따라 달라질 수 있다.

\- NVIDIA NIM shared endpoint는 rate limit이 발생할 수 있다.

\- API Key는 GitHub에 업로드하지 않는다.

\- SQLite DB, Chroma 폴더, Excel 결과물은 기본적으로 GitHub에 업로드하지 않는다.

\- 기사 전문 전체를 Vector DB에 저장하지 않는다.

\- 언론사 원문 이용, 저작권, robots 정책은 별도 검토가 필요하다.



\## 16. 실행 산출물



노트북 실행 후 다음 산출물이 생성될 수 있다.



\- SQLite DB

\- Chroma Vector DB 폴더

\- Excel 결과 파일

\- 자연어 응답 결과

\- SQLite 테이블별 DataFrame 출력

\- Chroma RAG 검색 결과



이 산출물은 로컬 또는 Colab 세션에서 확인하고, GitHub에는 기본적으로 업로드하지 않는다.



\## 17. 문제 발생 시 확인 항목



실행 중 문제가 발생하면 다음 항목을 확인한다.



\### 1. NVIDIA NIM 호출 실패



\- API Key가 올바른지 확인한다.

\- rate limit에 걸렸는지 확인한다.

\- max\_llm\_calls와 llm\_sleep\_sec 설정을 확인한다.



\### 2. 후보 기사가 너무 적은 경우



\- 기준일자를 변경한다.

\- 검색 키워드를 늘린다.

\- 대상 언론사를 조정한다.



\### 3. 실제 기사 수가 적은 경우



\- Google News 중간 URL이 원문 URL로 잘 변환되었는지 확인한다.

\- final\_domain이 allowed\_domains와 일치하는지 확인한다.

\- 언론사 페이지 접근이 제한되는지 확인한다.



\### 4. 본문 추출 실패



\- trafilatura 추출 결과를 확인한다.

\- BeautifulSoup fallback 결과를 확인한다.

\- 언론사 HTML 구조가 변경되었는지 확인한다.



\### 5. Chroma 저장 수가 적은 경우



\- 이는 오류가 아닐 수 있다.

\- 검증 기준을 통과한 기사만 저장하기 때문에 후보 수보다 Chroma 저장 수가 적을 수 있다.

\- RAG 오염을 방지하기 위한 필터링 결과로 해석한다.



\## 18. GitHub 업로드 제외 대상



다음 파일과 폴더는 GitHub에 업로드하지 않는다.



\- `.env`

\- SQLite DB 파일

\- Excel 결과 파일

\- Chroma Vector DB 폴더

\- API Key가 포함된 파일

\- 대용량 실행 로그

\- 임시 캐시 파일



위 항목은 `.gitignore`에 포함하여 관리한다.



\## 19. 정리



이 실행 가이드는 Colab 기반 EWS News RAG Agent Pipeline PoC를 재현하기 위한 절차를 정리한 문서이다.



본 프로젝트의 목적은 운영용 뉴스 수집 시스템 구축이 아니라, 건설산업 EWS 관점에서 비정형 언론보도 데이터의 수집가능성과 AI-Ready 전환 가능성을 검증하는 것이다.

