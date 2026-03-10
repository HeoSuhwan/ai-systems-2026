---
title: 용어집
description: AI 시스템 2026 강의 주요 용어 정의
---

## 용어집

이 강의에서 사용하는 핵심 용어를 알파벳순으로 정리했다.

---

**Agentic System (에이전틱 시스템)**
: 파일 수정, 코드 실행, API 호출 등 실제 행동을 자율적으로 수행하는 AI 시스템. 단순 텍스트 생성을 넘어 환경과 상호작용한다.

**Backpressure (백프레셔)**
: Ralph 루프에서 에이전트 출력이 기준에 맞지 않을 때 시스템이 자동으로 거부하고 재시도를 강제하는 메커니즘. 컴파일러, 타입 체커, 테스트 스위트가 대표적 백프레셔 구성 요소.

**Context Rot (컨텍스트 부패)**
: 장기 실행 에이전트에서 컨텍스트 창이 실패 시도와 오래된 코드로 채워져 추론 품질이 저하되는 현상.

**Context Window (컨텍스트 창)**
: LLM이 한 번에 처리할 수 있는 최대 토큰 수. Claude Sonnet 4.6 기준 약 200K 토큰.

**CUD Operations**
: Create, Update, Delete 작업. HOTL 거버넌스에서 High Risk로 분류되어 Hard Interrupt가 필요한 작업.

**DeepSeek V3**
: DeepSeek의 685B MoE 모델. 37B 활성 파라미터로 수학/추론/코딩 최상위권 성능. 8×H100 급 클러스터 필요.

**DGX H100**
: NVIDIA의 엔터프라이즈급 AI 서버. 제주한라대학교 AI 실습실에 설치된 모델. H100 GPU 8개 탑재.

**Garbage Collection (가비지 컬렉션)**
: Ralph 루프에서 에이전트가 생성한 잘못된 코드를 `git checkout .`으로 완전히 제거하고 저장소를 클린 상태로 복원하는 과정.

**Governance-as-Code**
: 거버넌스 정책(누가 어떤 행동을 할 수 있는가)을 소프트웨어 코드로 구현하여 자동으로 강제하는 접근법.

**Hard Interrupt**
: 에이전트가 High Risk 작업(CUD)을 시도할 때 반드시 인간의 명시적 승인을 받아야 하는 강제 정지 메커니즘.

**Harness (하네스)**
: Ralph 루프를 둘러싸는 결정론적 외부 시스템. 백프레셔, 가비지 컬렉션, 상태 추적 등을 포함. 에이전트의 비결정적 출력을 통제한다.

**Harness Engineering (하네스 엔지니어링)**
: 비결정적 AI 에이전트를 제어하는 결정론적 외부 시스템을 설계하는 공학 분야. 더 강력한 모델보다 더 강력한 하네스를 만드는 것을 목표로 한다.

**HIC (Human-in-Command)**
: AI 시스템의 최상위 거버넌스 계층. 인간이 전체 전략과 경계 조건을 설정하며 AI는 전술적 실행을 담당.

**HITL (Human-in-the-Loop)**
: AI가 행동하기 전 반드시 인간의 승인이 필요한 아키텍처. 안전하지만 느리고 확장성이 낮음.

**HOTL (Human-on-the-Loop)**
: AI가 자율적으로 실행하고 인간은 텔레메트리를 모니터링하며 필요시 개입하는 아키텍처. 속도와 확장성이 높음.

**Instructional Tuning (인스트럭션 튜닝)**
: 모델 가중치를 재훈련하지 않고 PROMPT.md에 구체적 지시를 추가하여 에이전트의 반복 오류를 교정하는 방법.

**LLM-as-Judge**
: LLM을 사용하여 다른 LLM의 출력 품질을 자동으로 평가하는 방법론. 인간 평가자를 부분적으로 대체.

**MCP (Model Context Protocol)**
: 에이전트와 외부 도구(파일시스템, Git, 데이터베이스 등)를 연결하는 표준화된 프로토콜. Anthropic이 개발.

**MIG (Multi-Instance GPU)**
: NVIDIA GPU를 독립적인 인스턴스로 분할하는 기술. H100에서 최대 7개 인스턴스 생성 가능. 하드웨어 수준 격리 제공.

**MiniMax M2.1**
: MiniMax의 230B MoE 모델 (10B 활성). 코딩 에이전트와 도구 사용에 특화. 가중치 완전 공개.

**MoE (Mixture of Experts)**
: LLM 아키텍처 중 하나. 전체 파라미터 중 일부만 활성화하여 추론 효율성을 높임. Qwen3-Coder, DeepSeek V3, MiniMax M2.1 등에 적용.

**Qwen3-Coder**
: Alibaba의 235B MoE 코딩 특화 모델 (22B 활성, 128K 컨텍스트). SWE-bench에서 상용 모델에 근접하는 성능. Apache 2.0 라이선스.

**GLM-4.7**
: Zhipu AI의 ~32B Dense 코딩 모델. Interleaved Thinking 기능으로 추론 품질이 높음. 단일 GPU 구동 가능. HuggingFace/ModelScope 공개.

**SGLang**
: vLLM과 함께 대표적인 오픈소스 LLM 추론 프레임워크. RadixAttention 기반 KV 캐시 재사용으로 높은 처리량 제공.

**PagedAttention**
: vLLM의 핵심 기술. OS의 가상 메모리 페이징을 KV 캐시에 적용하여 메모리 낭비를 4% 이하로 줄임.

**AI 코딩 CLI (AI Coding CLI)**
: 터미널에서 AI 에이전트를 실행하는 명령줄 도구의 총칭. Claude Code, Gemini CLI, Codex CLI, OpenCode 등이 해당. 헤드리스 모드로 Ralph 루프에서 자동화 가능.

**Ralph Loop (Ralph 루프)**
: Geoffrey Huntley가 2025년 대중화한 에이전틱 개발 방법론. `while :; do cat PROMPT.md | <ai-coding-cli>; done` 형태의 단순 지속 루프. `<ai-coding-cli>`에는 `claude`, `gemini`, `codex` 등을 사용할 수 있다.

**/loop (Claude Code Loop)**
: Claude Code의 공식 스케줄 기반 자율 에이전트 루프 명령. `claude /loop "<지시>" --every <간격> --for <기간>` 형태로 실행. 매 반복마다 git worktree를 생성하여 격리 실행하고, CLAUDE.md를 다시 읽어 최신 컨텍스트를 반영한다. 최대 3일 만료 — 잊혀진 에이전트의 컨텍스트 드리프트를 방지하기 위한 의도적 설계. Ralph 루프의 범용 패턴을 Claude Code 전용으로 제품화한 것.

**Ralphthon**
: Ralph 루프 방법론을 중심으로 한 해커톤 형식의 집중 개발 이벤트. 이 강의 캡스톤 프로젝트의 이름.

**SDLC (Software Development Lifecycle)**
: 소프트웨어 개발 생애주기. 요구사항 분석 → 설계 → 구현 → 테스트 → 배포 → 유지보수.

**Telemetry (텔레메트리)**
: 실행 중인 시스템의 성능 지표(메트릭), 로그, 추적(트레이스) 데이터를 실시간으로 수집하는 기술.

**vLLM**
: 오픈소스 고처리량 LLM 추론 라이브러리. PagedAttention 알고리즘으로 GPU 메모리 효율성을 극대화.
