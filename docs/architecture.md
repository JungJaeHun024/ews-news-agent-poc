\# Architecture



\## 전체 아키텍처



본 프로젝트는 자연어 질의를 입력받아 건설경기 관련 언론보도를 수집, 검증, 판단, 저장, 검색하는 Agentic Data Pipeline 구조로 설계되었다.



전체 흐름은 다음과 같다.



```text

User Natural Language Query

→ NaturalLanguageQueryParserAgent

→ CONFIG Builder

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

## 설계 원칙

본 프로젝트의 핵심 설계 원칙은 다음과 같다.

- LLM이 직접 웹을 탐색하지 않는다.
- 수집, URL 검증, 본문 추출, 저장은 코드 기반으로 처리한다.
- LLM은 검증된 후보 기사에 대해서만 판단한다.
- LLM 호출 실패 시 규칙 기반 fallback을 사용한다.
- 모든 단계의 결과를 추적 가능한 구조로 저장한다.
- RAG에는 검증된 기사만 적재한다.
- 기사 전문 전체를 Vector DB에 저장하지 않는다.

## 주요 컴포넌트

### 1. NaturalLanguageQueryParserAgent

사용자의 자연어 질의를 구조화된 수집 조건으로 변환한다.

입력 예시:

```text
오늘일자 기준으로 조중동의 건설경기 관련 뉴스 기사를 탐색해줘
```

출력 예시:

```json
{
  "target_date": "2026-05-15",
  "selected_outlets": ["조선일보", "중앙일보", "동아일보"],
  "keywords": ["건설경기", "건설수주", "미분양", "PF 부실", "공사비 상승", "건설투자", "주택시장"]
}
```

NVIDIA NIM을 사용하여 자연어 질의를 파싱하고, 실패 시 규칙 기반 fallback을 사용한다.

### 2. CONFIG Builder

파싱된 자연어 질의 결과를 기반으로 전체 Agent 실행 설정을 생성한다.

주요 설정값은 다음과 같다.

- target_date
- outlets
- keywords
- max_candidates_per_task
- max_total_candidates
- nvidia_nim_model
- llm_sleep_sec
- max_llm_calls
- sqlite_path
- chroma_path
- excel_path

### 3. QueryPlanningAgent

언론사, 도메인, 키워드, 기준일자를 조합하여 Google News RSS 검색 작업을 생성한다.

검색 쿼리는 다음 요소를 포함한다.

- keyword
- site domain
- after date
- before date

### 4. RSSCandidateAgent

Google News RSS에서 후보 기사를 수집한다.

수집 결과에는 다음 정보가 포함된다.

- candidate_id
- task_id
- outlet_name
- keyword
- candidate_title
- candidate_url
- rss_published
- rss_summary

### 5. URLAccessAgent

Google News RSS의 중간 URL을 실제 언론사 원문 URL로 변환하고 접근성을 검증한다.

주요 처리 내용은 다음과 같다.

- Google News URL resolver 적용
- final_url 확인
- final_domain 확인
- allowed_domains 검증
- HTTP status 확인
- 접근 가능 여부 판단
- HTML 응답 디코딩

### 6. ArticleVerificationAgent

접근 가능한 URL을 대상으로 실제 기사 여부와 본문 존재 여부를 검증한다.

추출 항목은 다음과 같다.

- title
- author
- published_at
- published_date
- description
- canonical_url
- body_exists
- body_length
- body_preview
- article_page_result
- metadata_quality
- verification_score
- quality_grade

### 7. RuleRiskEventAgent

기사 제목, 설명, 본문 일부를 기반으로 건설경기 관련 위험 이벤트를 규칙 기반으로 태깅한다.

이벤트 유형은 다음과 같다.

- 건설수주 감소
- 미분양 증가
- PF 부실
- 공사비 상승
- 착공 지연
- 주택시장 위험
- 건설투자 부진
- 기업 재무 건전성

### 8. NVIDIA NIM LLMJudgementAgent

검증된 기사 중 위험 신호가 있는 후보에 대해 NVIDIA NIM API를 호출하여 관련성을 판단한다.

판단 항목은 다음과 같다.

- relatedness
- main_risk_event
- risk_events
- fact_opinion_forecast
- event_summary
- judgement_reason

NVIDIA NIM shared endpoint의 rate limit을 고려하여 전체 후보 기사에 LLM을 전수 호출하지 않는다.

### 9. CrossSourceCheckAgent

위험 이벤트별로 복수 언론사에서 유사한 이벤트가 확인되는지 계산한다.

생성 항목은 다음과 같다.

- event_type
- outlet_count
- article_count
- cross_source_confirmed
- evidence_summary

### 10. SQLiteStorageAgent

각 단계 결과를 SQLite에 저장한다.

주요 테이블은 다음과 같다.

- search_tasks
- article_candidates
- article_access_checks
- article_metadata
- rule_risk_events
- llm_judgements
- cross_source_checks

### 11. ChromaStorageAgent

검증된 관련 기사만 Vector DB에 저장한다.

저장 대상 조건은 다음과 같다.

- URL 접근 가능
- 도메인 일치
- 실제 기사
- 본문 존재
- 관련성 판단 통과
- Google News 중간 URL 제외

저장 내용은 기사 전문 전체가 아니라 다음 정보 중심이다.

- 제목
- 언론사
- 작성일자
- 작성자
- 요약
- 위험 이벤트
- 판단 근거
- 원문 URL

### 12. ExcelReflectionAgent

수집가능성 검토표에 사용할 항목별 판단 결과와 근거를 생성한다.

검토 항목은 다음과 같다.

- 원문 확보 가능성
- 출처 URL 확보 가능성
- 메타데이터 확보 가능성
- 자동수집 가능성
- 수집 안정성
- 저작권·이용권한 검토
- RAG 활용 가능성
- 위험 이벤트 추출 가능성
- 교차확인 가능성

## 저장 구조

### SQLite

SQLite는 단계별 결과를 구조화하여 저장한다.

이를 통해 각 기사 후보가 어떤 단계에서 통과 또는 제외되었는지 추적할 수 있다.

### ChromaDB

ChromaDB는 RAG 검색을 위한 Vector DB로 사용된다.

단, 모든 후보 기사를 저장하지 않고 검증 기준을 통과한 기사만 저장한다.

### Excel

Excel 결과물은 수집가능성 검토표와 실행 진단 결과를 확인하기 위한 산출물이다.

## 운영화 시 보완 과제

- 중복 기사 제거
- AMP URL 정규화
- 작성일자 및 작성자 추출 고도화
- PostgreSQL 전환
- 스케줄링 적용
- API 서버화
- 모니터링 및 로깅 체계 구축

