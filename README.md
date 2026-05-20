<div align="center">

# 🌸 Olfít

### 나만의 시각적 아우라와 향기 취향을 연결하여 최적의 향수를 제안하는

**AI 기반 개인화 향수 추천 서비스**

사용자가 업로드한 OOTD 이미지를 AI로 분석하고, <br/>사용자의 명시적 성분 취향을 결합하여 개인화된 '향기 아우라'를 도출합니다. <br/>800여 개의 실제 향수 데이터를 기반으로 한 벡터 매칭 알고리즘을 통해 감성과 데이터의 완벽한 연결을 제공합니다.

<br/>

[🚀 설치 & 실행](#-설치--실행) · [🧠 주요 기능](#-주요-기능) · [🏗️ 아키텍처](#️-아키텍처)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

</div>

---

## 👥 팀원

> **조라에몽의 만능 도구들** 팀 — SK Networks 26기 4차 프로젝트

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/Gloveman.png" width="110px;" /><br />
      <b>이창우</b><br />
      <a href="https://github.com/Gloveman">@Gloveman</a>
    </td>
    <td align="center">
      <img src="https://github.com/rusidian.png" width="110px;" /><br />
      <b>장한재</b><br />
      <a href="https://github.com/rusidian">@rusidian</a>
    </td>
    <td align="center">
      <img src="https://github.com/eaent.png" width="110px;" /><br />
      <b>전승권</b><br />
      <a href="https://github.com/eaent">@eaent</a>
    </td>
    <td align="center">
      <img src="https://github.com/jjonyeok2.png" width="110px;" /><br />
      <b>전종혁</b><br />
      <a href="https://github.com/jjonyeok2">@jjonyeok2</a>
    </td>
    <td align="center">
      <img src="https://github.com/nobrain711.png" width="110px;" /><br />
      <b>조동휘</b><br />
      <a href="https://github.com/nobrain711">@nobrain711</a>
    </td>
    <td align="center">
      <img src="https://github.com/sooa02.png" width="110px;" /><br />
      <b>최수아</b><br />
      <a href="https://github.com/sooa02">@sooa02</a>
    </td>
    <td align="center">
      <img src="https://github.com/dhksrlghd.png" width="110px;" /><br />
      <b>홍완기</b><br />
      <a href="https://github.com/dhksrlghd">@dhksrlghd</a>
    </td>
  </tr>
</table>

---

## ✨ 주요 기능

| 기능 | 설명 | 기술 특징 |
|---|---|---|
| 🖼️ **AI 이미지 분석** | OOTD 이미지에서 색상·감성을 추출하여 5축 아우라 스코어 산출 (Floral / Woody / Amber / Fresh / Gourmand) | AI Emotional Mapping — NVIDIA NIM(Gemma VLM) 기반 |
| 🎯 **향수 매칭** | 이미지 감성과 사용자의 명시적 성분 취향을 결합한 다차원 벡터 매칭으로 최적 향수 추천 | Symmetric Scent Search — 한글화 대칭형 쿼리로 직관적 매칭 |
| 📊 **인사이트 리포트** | 분석 결과를 레이더 차트와 함께 고해상도 이미지 리포트로 캡처 및 공유 | High-Resolution Insights — html2canvas 기반 이미지 캡처 |
| 🛡️ **개인정보 동의 흐름** | 서비스 이용 전 개인정보 수집 동의 프로세스 및 익명 세션 기반 분석 | Hybrid Storage Strategy — 관계형 메타데이터 + JSON 하이브리드 |

---

## 🖥️ 서비스 화면 (이미지 추가)

**개인정보 동의 화면**
<div align="center">
  <img src="./docs/images/olfit_popup.png" width="70%" alt="olfit-popup">
</div>

**메인 화면**
<div align="center">
  <img src="./docs/images/olfit_header.png" width="70%" alt="olfit-header">
</div>

**설명 화면**
<div align="center">
  <img src="./docs/images/olfit_philosophy.png" width="70%" alt="olfit-philosophy">
</div>

**향수 용어 설명 화면**
<div align="center">
  <img src="./docs/images/olfit_education.png" width="70%" alt="olfit-education">
</div>

**향수 원료 설명 화면**
<div align="center">
  <img src="./docs/images/olfit_concent.png" width="70%" alt="olfit-concent">
</div>

**탑, 미들, 베이스 노트 설정 화면**
<div align="center">
  <img src="./docs/images/olfit_pyramid.png" width="70%" alt="olfit-pyramid">
</div>

**분석 전 화면**
<div align="center">
  <img src="./docs/images/olfit_banalyze.png" width="70%" alt="olfit-beforeAnalyze">
</div>

**분석 후 화면**
<div align="center">
  <img src="./docs/images/olfit_aanalyze.png" width="70%" alt="olfit-AfterAnalyze">
</div>

**리포트 화면 1**
<div align="center">
  <img src="./docs/images/olfit_report1.png" width="70%" alt="olfit-ScentBlueprint">
</div>

**리포트 화면 2**
<div align="center">
  <img src="./docs/images/olfit_report2.png" width="70%" alt="olfit-Aura">
</div>

**리포트 화면 3**
<div align="center">
  <img src="./docs/images/olfit_report3.png" width="70%" alt="olfit-MatchingToggle">
</div>

**리포트 화면 4**
<div align="center">
  <img src="./docs/images/olfit_report4.png" width="70%" alt="olfit-RecommendPerfume">
</div>

**리포트 화면 5**
<div align="center">
  <img src="./docs/images/olfit_report5.png" width="70%" alt="olfit-sharebtn">
</div>

**실 데이터와 기능 설명**
<div align="center">
  <img src="./docs/images/olfit_trust.png" width="70%" alt="olfit-sharebtn">
</div>

**하단 이동 버튼과 부가 기능**
<div align="center">
  <img src="./docs/images/olfit_footer.png" width="70%" alt="olfit-footer">
</div>


---

## 🛠️ 기술 스택

### Language & Framework

| 분류 | 기술 | 버전 | 용도 |
|---|---|---|---|
| Language | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) | 3.12 / 5.9 | 백엔드(Python) · 프론트엔드(TypeScript) |
| Frontend | ![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black) | 19.2.0 | UI 컴포넌트 구성 |
| Build Tool | ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white) | 7.x | 개발 서버 및 번들링 |
| Backend | ![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white) | 6.0.5 | REST API 서버 |
| Backend | ![DRF](https://img.shields.io/badge/DRF-ff1709?style=flat-square&logo=django&logoColor=white) | 3.17.1 | REST API 구현 |

### Database

| 분류 | 기술 | 용도 |
|---|---|---|
| RDBMS | ![MySQL](https://img.shields.io/badge/MySQL_8.4-4479A1?style=flat-square&logo=mysql&logoColor=white) | 향수 메타데이터, 사용자 정보 |
| JSON Column | ![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white) models.JSONField | 향수 상세 정보, 노트, 아우라 프로필 등 반정형 데이터 |

### AI / ML

| 분류 | 모델 / 라이브러리 | 용도 |
|---|---|---|
| VLM | **NVIDIA NIM (google/gemma-3n-e4b-it)** | 이미지 감성 분석 및 아우라 스코어 산출 |
| 유사도 | NumPy + scikit-learn | 아우라 벡터 연산 및 코사인 유사도 기반 추천 점수 계산 |

### Frontend 라이브러리

| 기술 | 버전 | 용도 |
|---|---|---|
| Zustand | 5.0.13 | 전역 상태 관리 |
| Axios | 1.16.0 | API 통신 |
| Recharts | 2.15.4 | 레이더 차트 등 데이터 시각화 |
| html2canvas | 1.4.1 | 분석 리포트 이미지 캡처 |
| Tailwind CSS | 3.4.19 | 유틸리티 기반 스타일링 |
| Radix UI | `@radix-ui/react-*` | 접근성 기반 headless UI 컴포넌트 |
| Lucide React | 0.562.0 | 아이콘 |
| Embla Carousel | 8.6.0 | 캐러셀 UI |

### Infrastructure

| 기술 | 용도 |
|---|---|
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | 컨테이너 환경 구성 |
| ![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white) | 프론트엔드 · 백엔드 · DB 멀티 컨테이너 오케스트레이션 |

### Co-Tools

| 기술 | 용도 |
|---|---|
| ![Jira](https://img.shields.io/badge/Jira-0052CC?style=flat&logo=Jira&logoColor=white) | 애자일 프로젝트 스프린트 설정 및 관리 |
| ![Notion](https://img.shields.io/badge/Notion-000000?style=flat&logo=notion&logoColor=white) | 업무 및 프로젝트 관리 |
| ![Discord](https://img.shields.io/badge/Discord-5865F2?style=flat&logo=discord&logoColor=white) | 업무 메신저 |

---

## 🏗️ 아키텍처

### 시스템 구성도
<div align="center">
  <img src="./docs/images/infra_diagram.png" width="90%" alt="System Diagram">
</div>

### 파이프라인
**전체 파이프라인**
<div align="center">
  <img src="./docs/images/sequence_diagram.png" width="90%" alt="Entire pipeline">
</div>

**프론트 파이프라인 상세**
<div align="center">
  <img src="./docs/images/frontend_flow.png" width="90%" alt="Data pipeline">
</div>

**백엔드 파이프라인 상세**
<div align="center">
  <img src="./docs/images/data_flow.png" width="70%" alt="Data pipeline">
</div>

### 데이터베이스 설계

<div align="center">
  <img src="./docs/images/olfit_erd.png" width="90%" alt="Database ERD">
</div>

---

## 📁 프로젝트 구조

```text
olfit/
├── .github/                # GitHub 이슈 템플릿 및 CI/CD 워크플로우
├── backend/                # Django REST Framework 기반 백엔드
│   ├── app/                # Django 프로젝트 메인 소스
│   │   ├── app/            # Django 프로젝트 설정 및 기본 구성
│   │   ├── data/raw/       # 크롤링한 향수 raw 데이터
│   │   ├── perfumes/       # 향수 도메인 (모델, API, 시리얼라이저)
│   │   │   ├── data/       # 향수 데이터 매핑 사전
│   │   │   ├── management/ # Django 커스텀 커맨드 (데이터 초기화 및 마이그레이션 도구)
│   │   │   ├── services/   # 추천 엔진 및 비즈니스 로직
│   │   │   └── tests/      # 백엔드 단위 및 통합 테스트
│   │   ├── scent_engine/   # VLM 연동 및 프롬프트 관리 로직
│   │   └── static/         # 백엔드 정적 자산 (향수 이미지 등)
│   ├── Dockerfile          # 백엔드 컨테이너 빌드 설정
│   └── requirements.txt    # 파이썬 의존성 패키지 목록
├── frontend/               # Vite + React + TypeScript 기반 프론트엔드
│   ├── src/
│   │   ├── components/     # UI 컴포넌트 (Shadcn UI 기반)
│   │   ├── hooks/          # 커스텀 훅 (리포트 캡처, 상태 관리 등)
│   │   ├── services/       # API 통신 및 추천 엔진 연동
│   │   ├── store/          # Zustand 기반 전역 상태 관리
│   │   ├── data/           # 프론트엔드 정적 데이터 (노트 정보 등)
│   │   └── types/          # TypeScript 타입 정의
│   ├── public/             # 정적 이미지 및 자산
│   └── Dockerfile          # 프론트엔드 컨테이너 빌드 설정
├── database/               # MySQL 설정 및 초기화 스크립트
│   ├── conf.d/             # MySQL 사용자 정의 설정
│   └── init/               # DB 초기 데이터 및 스키마 스크립트
├── models/                 # 브랜드별 윤리도, 스타일 프로파일링 등 확장 실험
├── docs/                   # 시스템 설계도, README 이미지, ERD 및 프로젝트 산출물
├── wiki/                   # MdBook 기반 프로젝트 기술 위키
├── docker-compose.yml      # 전체 서비스 컨테이너 오케스트레이션
├── .env.example            # 환경 변수 설정 템플릿
└── README.md
```

---

## 🚀 설치 & 실행

### 사전 요구사항

- **Docker & Docker Compose**: 컨테이너 환경 실행을 위해 필수입니다.
- **Git**: 레포지토리 클론 및 소스 관리를 위해 필요합니다.
- **NVIDIA API Key**: NVIDIA NIM VLM 이미지 분석 API 접근을 위해 필요합니다.

### 방법: Clone하여 실행을 권장

```bash
# 1. 레포지토리 클론
git clone https://github.com/Joraemon-s-Secret-Gadgets/olfit.git
cd olfit

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 필요한 값을 입력 (아래 환경 변수 섹션 참고)

# 3. Docker Compose로 전체 서비스 실행
docker compose up -d --build

# 4. 서비스 접속
# Frontend Web : http://localhost:3000
# Backend API  : http://localhost:8000
# Database     : localhost:3307 (External Access)
```

### 환경 변수 설정 (`.env`)

```env
# NVIDIA NIM
NVIDIA_API_KEY=your_nvidia_api_key_here

# Database
SQL_DB_PASSWORD=your_db_password
```

### 서비스 상태 확인

```bash
# 전체 컨테이너 상태 확인
docker compose ps

# 로그 확인
docker compose logs -f

# 특정 서비스 로그만 확인
docker compose logs -f backend
docker compose logs -f frontend
```

### 서비스 종료

```bash
# 컨테이너 종료
docker compose down

# 컨테이너 + 볼륨 삭제 (DB 데이터 포함)
docker compose down -v
```

---

## 📖 사용 가이드

### 1. 개인정보 동의

서비스 접속 시 AI 분석을 위한 개인정보 수집 동의 절차를 진행합니다. 동의 후 익명 세션 ID가 발급됩니다.

### 2. 향기 노트 선택

선호하는 향기 노트(베르가못, 장미, 샌달우드 등)를 직접 선택합니다. 이미지 분석 결과와 결합하여 최종 추천에 반영됩니다.

### 3. 이미지 업로드 & AI 분석

OOTD 이미지를 업로드합니다. NVIDIA NIM(Gemma VLM)이 이미지를 분석하여 5축 아우라 스코어를 산출합니다.

| 축 | 설명 |
|---|---|
| 🌸 Floral | 꽃향기 계열 감성 |
| 🌲 Woody | 우드·어스 계열 감성 |
| 🍂 Amber | 오리엔탈·앰버 계열 감성 |
| 🍃 Fresh | 시트러스·아쿠아 계열 감성 |
| 🍫 Gourmand | 달콤·구르망 계열 감성 |

### 4. 인사이트 리포트 확인

분석 결과를 레이더 차트와 함께 확인하고, 추천 향수 리스트를 탐색합니다. 리포트는 이미지로 캡처하여 공유할 수 있습니다.

---

## 한계 (작성 필요)

---

## 확장 방향 (작성 필요)

#### 비건·크루얼티 프리
- 현재는 윤리적·비윤리적 브랜드 구분 없이 메이저 향수 브랜드 크롤링. 이후 비건·크루얼티 프리에 해당하는 브랜드를 확보/적재 해 사용자가 윤리적 브랜드를 선택해 결과를 필터링할 수 있도록 확장

---

## 🔍 사전 조사 레포지토리

본 프로젝트를 위해 팀원들이 각자 진행한 사전 기술 조사 및 프로토타입 레포지토리입니다.

| 레포지토리 | 담당자 | 내용 |
|---|---|---|
| [4th_perfume_crawling_playground](https://github.com/Joraemon-s-Secret-Gadgets/4th_perfume_crawling_playground) | [![이창우](https://img.shields.io/badge/이창우-Gloveman-181717?style=flat-square&logo=github)](https://github.com/Gloveman) | 향수 데이터 사전조사 및 크롤링 (Bulgari, Dior) |
| [4th_data_playgroud](https://github.com/Joraemon-s-Secret-Gadgets/4th_data_playgroud) | [![장한재](https://img.shields.io/badge/장한재-rusidian-181717?style=flat-square&logo=github)](https://github.com/rusidian) | 향수 데이터 크롤링 (Tom Ford, Diptyque) 및 이미지 키워드 추출, 향수 키워드 변환 사전조사 |
| [4th_data_ground](https://github.com/Joraemon-s-Secret-Gadgets/4th_data_ground) | [![전승권](https://img.shields.io/badge/전승권-eaent-181717?style=flat-square&logo=github)](https://github.com/eaent) | 향수 데이터 사전조사 및 크롤링 (Giorgio Armani, Maison Francis Kurkdjian) |
| [4th_data_playground](https://github.com/Joraemon-s-Secret-Gadgets/4th_data_playground) | [![조동휘](https://img.shields.io/badge/조동휘-nobrain711-181717?style=flat-square&logo=github)](https://github.com/nobrain711) | 향수 데이터 사전조사 및 크롤링 (Lush, Jo Malone, Chanel) |
| [4th_fragrance_data_playground](https://github.com/Joraemon-s-Secret-Gadgets/4th_fragrance_data_playground) | [![최수아](https://img.shields.io/badge/최수아-sooa02-181717?style=flat-square&logo=github)](https://github.com/sooa02) | 향수 데이터 사전조사 및 크롤링 (Creed, Granhand) |
| [4th_olfit_connect_playground](https://github.com/Joraemon-s-Secret-Gadgets/4th_olfit_connect_playground) | [![이창우](https://img.shields.io/badge/이창우-Gloveman-181717?style=flat-square&logo=github)](https://github.com/Gloveman) | Frontend와 Vision 분석 코드 통합 Backend 로직 사전조사 |
| [4th_olfif_Embedding_playground](https://github.com/Joraemon-s-Secret-Gadgets/4th_olfif_Embedding_playground) | [![장한재](https://img.shields.io/badge/장한재-rusidian-181717?style=flat-square&logo=github)](https://github.com/rusidian) | Pinecone 기반 RAG 추천 로직, 향수 임베딩 인덱싱과 5축 아우라 유사도 기반 재정렬 로직 사전조사 |
| [4th_react_ts_playground](https://github.com/Joraemon-s-Secret-Gadgets/4th_react_ts_playground) | [![전종혁](https://img.shields.io/badge/전종혁-jjonyeok2-181717?style=flat-square&logo=github)](https://github.com/jjonyeok2) | Frontend React 및 TypeScript 사전조사 |
| [djongo_rest_framework_playground](https://github.com/Joraemon-s-Secret-Gadgets/djongo_rest_framework_playground) | [![조동휘](https://img.shields.io/badge/조동휘-nobrain711-181717?style=flat-square&logo=github)](https://github.com/nobrain711) | Django REST Framework 사전조사 |

---

## 🔗 관련 문서

프로젝트의 상세한 기술 정보 및 가이드는 아래 문서에서 확인하실 수 있습니다.

- [**🧰 기술 스택 상세**](./wiki/src/tech-stack.md)
- [**📏 개발 컨벤션**](./wiki/src/conventions.md)
- [**🏗️ 시스템 구성도**](./docs/system_architecture.pdf)
- [**🧩 ERD 설계 및 데이터 모델링**](./wiki/src/backend/data/erd_design.md)
- [**📥 데이터 정규화 및 전처리 파이프라인**](./wiki/src/backend/pipeline/data_ingestion_pipeline.md)
- [**🧭 백엔드 아키텍처 개요**](./wiki/src/backend/architecture/overview.md)
- [**🎨 프론트엔드 아키텍처 상세**](./wiki/src/frontend/architecture/FRONTEND_ARCHITECTURE.md)
- [**✅ 전체 테스트 결과**](./wiki/src/tests/test-results.md)

---

## 프로젝트 회고

### 개인 회고

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
    <thead>
        <tr style="background-color: #f8f9fa;">
            <th style="width: 20%; border: 1px solid #ddd; padding: 10px;">이름</th>
            <th style="border: 1px solid #ddd; padding: 10px;">회고</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
            <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전승권</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
    </tbody>
</table>

---

### 팀원 회고

<details>
<summary>팀원 회고 펼치기</summary>

<br/>

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom: 30px;">
    <thead>
        <tr style="background-color: #f8f9fa;">
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">대상자</th>
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">작성자</th>
            <th style="border: 1px solid #ddd; padding: 10px;">회고 내용</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전승권</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전승권</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">전승권</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전승권</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전승권</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전승권</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;"></td>
        </tr>
    </tbody>
</table>

</details>

---

## 📜 License

본 프로젝트는 **MIT License**를 따릅니다.<br/>
모든 소스 코드 및 관련 문서의 사용 및 배포 규정은 [LICENSE](./LICENSE) 파일에서 확인하실 수 있습니다.

<div align="center">
Copyright (c) 2026 SK Networks 26th 조라에몽의 만능 도구들 팀 (Team Joraemon-s-Secret-Gadgets)
</div>
