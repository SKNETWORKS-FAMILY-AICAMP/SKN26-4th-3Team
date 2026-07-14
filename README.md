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

## 🖥️ 서비스 화면

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
| html2canvas | 1.4.1 | 분석 리포트 이미지 캡처 |
| Tailwind CSS | 3.4.19 | 유틸리티 기반 스타일링 |
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

## 한계점

### 1. 데이터 커버리지
 
- 현재 13개 프리미엄 브랜드, 860여 종의 향수 데이터만 보유하고 있어 틈새 브랜드나 신제품 향수는 추천 대상에서 제외됩니다.
- 외부 크롤링 데이터 기반이기 때문에 원본 사이트 구조 변경 시 파이프라인 재정비가 필요합니다.

### 2. 추천 알고리즘
 
- 아우라 가중치(V_visual 0.6 / V_pref 0.4, 재랭킹 w1·w2 각 0.5)는 팀 내 실험을 통해 설정한 값으로, 개인마다 최적 비율이 다를 수 있습니다.
- 사용자가 선호 노트를 선택하지 않으면 V_pref가 0 벡터가 되어 이미지 분석 결과에만 의존합니다. — 최솟값 0.1 보정으로 Cold Start를 방지하고 있으나 완전한 해결책은 아닙니다.
- 현재 추천 다양성(Diversity) 보장 로직이 없어 Top 5가 유사한 계열로 쏠릴 가능성이 존재합니다.

### 3. 서버 및 인프라
 
- Django `runserver` 기반의 동기 처리 방식으로 운영 중이어서, 동시 요청이 몰릴 경우 응답 지연이 발생할 수 있습니다.
- NVIDIA NIM API의 분당 요청 제한(RPM 40)으로 인해 트래픽이 집중되는 상황에서 병목이 생길 수 있습니다.

---

## 확장 방향

### Near Term
 
**공간 향기 추천으로 서비스 범위 확장**
 
개인 OOTD 이미지에서 공간 이미지로 입력 범위를 넓히는 방향을 계획하고 있습니다. 카페, 호텔, 쇼룸 같은 실내 공간의 무드 이미지를 입력하면 그 공간에 어울리는 디퓨저·캔들 향을 추천하는 기능으로, 개인 향수 추천에서 공간 향기 큐레이션으로 서비스 범위를 확장합니다.
 
**Gunicorn 전환으로 서버 성능 개선**
 
현재 Django `runserver`(동기) 방식을 Gunicorn으로 전환해 프론트엔드의 비동기 요청에 효율적으로 대응하고 처리량을 높일 계획입니다. Docker Compose 환경에서 Gunicorn + Nginx 구조로의 전환이 다음 개선 목표입니다.
 
### Mid Term
 
**Few-shot 기반 자연어 검색 쿼리 강화**
 
현재는 이미지에서 추출한 시각 정보를 벡터화해 검색합니다. 이를 확장해 "봄날 소풍 같은 향", "고요한 서재 분위기"처럼 추상적인 자연어 표현을 아우라 벡터로 변환해 정밀 검색이 가능한 텍스트 입력 모드를 추가할 계획입니다. Few-shot 프롬프트를 통해 LLM이 향수 평론가처럼 서술형 쿼리를 생성하는 방식으로 RAG 검색 품질을 높입니다.
 
**추천 다양성 보장 로직 도입**
 
Top 5 추천이 동일 계열·브랜드로 쏠리는 문제를 방지하기 위해 Maximal Marginal Relevance(MMR) 기반 다양성 재랭킹을 도입할 예정입니다.
 
### Long Term
 
**대화형 향기 탐색 인터페이스**
 
"나는 나무 냄새가 좋고 무겁지 않은 향이 좋아"처럼 자유로운 자연어 대화로 향수를 탐색하는 챗봇 형식의 인터페이스를 목표로 합니다. 사용자의 감성 표현을 연속 대화로 수집해 점진적으로 아우라 벡터를 정교화하고, 최종 추천으로 이어지는 대화형 개인 조향사 경험을 제공합니다.
 
**데이터 확장 및 실시간 업데이트 파이프라인**
 
현재 860여 종에서 벗어나 국내외 브랜드 전반으로 데이터를 확장하고, 신제품 출시에 맞춰 자동으로 데이터를 수집·적재·인덱싱하는 실시간 ETL 파이프라인 구축을 목표로 합니다.

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

프로젝트의 상세한 정보 및 가이드는 아래 문서에서 확인하실 수 있습니다.

- [**🧰 기술 스택 상세**](./wiki/src/tech-stack.md)
- [**📏 개발 컨벤션**](./wiki/src/conventions.md)
- [**📌 요구사항 정의서**](./docs/Olfit_요구사항정의서.pdf)
- [**🏗️ 시스템 구성도**](./docs/system_architecture.pdf)
- [**🧩 ERD 설계 및 데이터 모델링**](./wiki/src/backend/data/erd_design.md)
- [**📥 데이터 정규화 및 전처리 파이프라인**](./wiki/src/backend/pipeline/data_ingestion_pipeline.md)
- [**🧭 백엔드 아키텍처 개요**](./wiki/src/backend/architecture/overview.md)
- [**🎨 프론트엔드 아키텍처 상세**](./wiki/src/frontend/architecture/FRONTEND_ARCHITECTURE.md)
- [**📖 전체 테스트 계획** ](./wiki/src/tests/test-plan.md)
- [**📖 RAG 테스트 계획** ](./wiki/src/tests/rag-test.md)
- [**📖 이미지 업로드 테스트 계획** ](./wiki/src/tests/image-upload-tests.md)
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
            <td style="border: 1px solid #ddd; padding: 10px;">
            이번 프로젝트에서 저는 백엔드와 vector DB 적재 파이프라인 구축을 담당하며 시스템의 안정성과 추천 로직의 완성도를 높이는데 집중했습니다.
            가장 의미 있었던 도전은 초기 기획 단계에서 프론트엔드의 취향 시각화 용도로만 고려되었던 ‘향수 계열 5축 벡터’ 개념을 백엔드 중심의 정교한 추천 로직으로 확장한 점입니다. 사용자 취향 분석 결과와 개별 향수 제품 데이터를 동일한 5축 차원의 벡터로 변환하고, 두 벡터 간의 ‘아우라 유사도’를 계산하여 최종 추천 리스트의 리랭킹 알고리즘에 반영하도록 로직을 고도화했습니다. 이를 위해 향수의 세부 어코드와 노트를 5대 대표 어코드 계열로 분류하는 ‘매핑 사전’을 직접 정의 및 구축하여 데이터 연산의 기반을 마련했습니다. 프로젝트 일정상 정밀한 가중치 튜닝을 하지 않고 휴리스틱한 설계에 머문 점은 아쉬움으로 남지만, 비정형 데이터를 서비스 핵심 도메인 지식과 결합하여 고유한 알고리즘 파이프라인으로 완성해 낸 값진 경험이었습니다
            DB 적재 및 검색 성능 최적화 측면에서는 RAG 시스템의 기반을 다지는 데 주력했습니다.  향수 성분 데이터와 LLM 기반 키워드를 유기적으로 결합하여 RAG 검색 효율을 극대화할 수 있는 최적의 쿼리를 설계했고, 생성된 임베딩 벡터를 DB에 안정적으로 적재했습니다. 이 과정에서 시스템 운영 비용을 의식하여 해시값을 활용한 데이터 변경 감지 로직을 도입했습니다. 소스 텍스트가 변경되지 않았다면 고비용의 임베딩 모델 API 호출을 원천 차단하도록 설계함으로써, 불필요한 비용을 획기적으로 절감하고 전체 데이터 파이프라인의 처리 효율을 높였습니다. 결과적으로 이번 프로젝트는 데이터 모델링부터 비용 최적화까지 백엔드 AI 엔지니어로서의 종합적인 시야를 넓힐 수 있었던 계기가 되었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            이번 프로젝트에서는 LLM 및 RAG 추천 로직 구현을 중심으로 작업했습니다.
            착장 이미지를 향수 추천으로 연결하기 위해 Vision 기반 분석 결과를 자연어 쿼리로 변환하고, Pinecone 기반 semantic retrieval과 재랭킹 구조를 설계하며 추천 품질을 높이고자 했습니다.
            특히 단순 검색이 아니라 착장의 분위기와 향수 description 간의 의미적 연결을 어떻게 만들지 고민하며, Aura 벡터와 semantic similarity를 함께 활용하는 하이브리드 구조를 구현한 경험이 가장 인상 깊었습니다.
            이번 프로젝트를 통해 LLM 활용 자체보다, 검색·추천 구조를 어떻게 설계하느냐가 서비스 품질에 더 중요하다는 점을 배울 수 있었습니다.
            </td>
        </tr>
            <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전승권</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
             이번 프로젝트를 진행하면서 팀 활동방향을 이해하는거에 집중을 했습니다. jira 스프린트를 접해보면서 계획 수립과 실행관련으로 문서화하여 명확히 명시를 통해
            프로젝트 전반의 진행률을 알수있는걸 처음 봤고 그걸 녹여내는 과정에 어려움은 있었으나 익숙해 지면되므로 노력을 했습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            olfit 프로젝트를 진행하며, 디자인 템플릿과, 프론트엔드 UI/UX의 고도화를 경험해보며, 기술 스택과 디자인에 있어서 발전을 한 계기라고 생각합니다. 사이트의 목적에 따라 디자인을 어디까지 고도화할 수 있는지 깨닫게 되었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            이번 프로젝트에서 저는 데이터 파이프라인과 팀에서 개발한 프로그램의 테스트를 담당했습니다. 단순히 버그를 찾는 데 그치지 않고, 데이터 품질 문제를 조기에 잡아내 팀원들이 개발에 집중할 수 있도록 품질 게이트 역할을 맡았습니다.
            데이터 정제. 크롤링한 향수 데이터가 브랜드별로 제대로 분리되지 않는 문제가 있었습니다. 정규식과 조건문을 활용해 브랜드 단위로 데이터를 분리했고, 크롤링 과정에서 누락된 값은 HTML 태그 구조를 다시 확인해 필요한 데이터를 재취득한 뒤 반영했습니다.
            테스트와 피드백 루프. 테스트 중 발생한 에러나 의도대로 동작하지 않는 기능을 팀원들에게 구체적으로 전달해, 기능이 원하는 대로 수정·반영되도록 했습니다. RAG의 경우 검색 조건을 걸었을 때 의도한 대로 결과가 나오는지 반복 검증하며 동작을 확인했습니다.
            이 과정에서 AI 프로젝트에서 데이터 품질이 결과를 좌우한다는 점을 체감했습니다. 초반 데이터가 부실한 상태에서는 모델이 쉽게 할루시네이션에 빠졌고, 원하는 답변을 얻기까지 반복 질의가 늘어났습니다. 데이터를 정제하고 RAG 적용 여부를 직접 비교하면서, RAG의 유무가 LLM 답변 품질을 크게 좌우한다는 것을 개념이 아니라 실제 경험으로 이해하게 되었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;">이전 프로젝트에서 PL을 맡으며 ‘체계적인 이슈 관리가 팀의 속도를 결정한다’는 것을 체감했기에, 이번에는 PM을 자원했고 향수 데이터 크롤링에도 참여했다. 기술 명세서를 MECE 분류 → WBS → Jira 에픽/스토리 구조로 체계화해, 10개 에픽·44개 스토리를 PR·커밋 단위로 추적되도록 설계했다. 이슈/PR 템플릿과 GitHub-Jira-Discord 연동을 세팅하고, 커밋 이슈 키와 Closes로 PR과 지라 이슈가 자동 연동·종료되도록 컨벤션을 통일했다. 크롤링에서는 사이트마다 다른 HTML 구조를 분석해 추천 엔진이 쓸 수 있는 형태로 정리했다. 그 결과 데일리 스크럼으로 작업 의존성을 빠르게 조율하고 진행 상황을 투명하게 확인할 수 있었다. 일정 관리를 넘어 협업 구조 자체를 설계하면 팀의 속도가 달라진다는 것을 직접 확인하며 성장할 수 있었다. 다만 PM에 집중하느라 개발 경험을 더 쌓지 못한 점은 아쉬웠다. 다음에는 PM과 기술 구현을 병행하며 한 단계 더 성장하고 싶다.
            </td>
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
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            few-shot 프롬포트 기법을 통해 VLM이 추출한 원시 스타일 키워드를 목적에 맞게 정제하고 고도화하는 로직을 실험해 주셨습니다. 더불어, 동물 실험 등 브랜드의 ‘윤리성’ 지표에 대해서도 조사해 주셨습니다. 비록 해당 결과가 실제 서비스에 직접 반영되지 못했지만, 할당받은 테스크를 끝까지 잘 완수해 주셨습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            이번 프로젝트에서 RAG 설계·구현과 백엔드를 담당한 팀원에게 특히 감사를 전하고 싶습니다. 우리가 서비스로 전달하려던 의도를 정확히 이해하고 그 방향대로 RAG를 설계·구현해 주었습니다. 특히 리트리버 구현의 완성도가 높아, LLM의 할루시네이션을 효과적으로 억제하고 향수 추천 서비스의 답변 품질을 끌어올릴 수 있었습니다.
            테스트를 담당한 입장에서, 검색 결과가 조건과 맞지 않거나, 관련 없는 향수가 딸려 나오거나, 정작 원하는 향수가 누락되는 문제를 발견하면 그때그때 전달했습니다. 그러면 팀원이 원인을 파악해 빠르게 수정·반영해 주었고, 이런 피드백을 여러 차례 주고받으며 검색 정확도·노이즈·재현율을 함께 다듬어 나갔습니다. 그 과정을 거치며 리트리버의 검색 성능이 점차 안정화되었고, 서비스 품질도 꾸준히 끌어올릴 수 있었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            추천 엔진과 RAG 검색 파이프라인의 전 과정을 설계·구현하며 기술적으로 까다로운 과제들을 해결해 주셨습니다. 단순한 벡터 검색에 그치지 않고, Pinecone으로 Top 30 후보를 추출한 뒤 재랭킹을 거쳐 Top 5를 추리는 다단계 추천 로직을 정교하게 설계해, 사용자에게 어울리는 향수를 정확하게 제안할 수 있도록 만들어 주셨습니다. 또한 추천 근거를 설명하는 ExplainService로 결과에 설득력을 더하고, LangSmith 기반으로 RAG의 실행 속도와 검색 품질을 직접 측정·검증하며 파이프라인을 끊임없이 개선해 주셨습니다. 덕분에 추천 엔진이라는 프로젝트의 핵심 가치를 안정적으로 구현해낼 수 있게 되었습니다.
            </td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            VLM을 활용하여 사용자가 업로드한 이미지로부터 향수 관련 키워드를 자동으로 추출하고, 5축 벡터 계산을 위한 기초 점수 산정 매핑 로직을 구현해 주셨습니다. 이에 더해 RAG 기반 추천 로직의 초안을 작성하여 이후 추천 알고리즘 고도화 작업 및 백엔드 시스템으로 이식 과정에서 시행착오를 줄이고 전체적인 개발 시간을 크게 단축할 수 있었습니다. 
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            향수 추천에 필요한 임베딩 벡터를 구축하면서, 꼭 필요한 파트를 빠르고, 책임감 있게 해내주셔서 프로젝트 개발 속도에 박차를 가할 수 있었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            LLM 개발을 담당한 팀원의 기여도 그만큼 중요했습니다. VLM 모델을 선정해 이미지를 읽고 향수를 추천하는 파이프라인을 간결하게 구축했고, 에러로 중단되어야 할 예외 상황이 잘 방어되도록 설계해 테스트 과정에서 큰 문제가 없었습니다. 특히 NVIDIA NIM의 VLM 모델은 분당 호출 40회 제한이 있어 초과 시 일정 시간 뒤 재호출되도록 대응해야 했는데, 이 부분을 미리 견고하게 처리해 준 덕분에 관련 테스트를 한 번에 통과할 수 있었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            AI 파이프라인 전반을 고도화하며 서비스의 핵심인 ‘향 추천 정확도’를 끌어올려 주셨습니다. 사용자의 옷차림 이미지를 향 특성으로 변환하는 룰셋을 고도화하고 스타일 카테고리를 확장해, 시각 정보가 향으로 정교하게 이어지도록 만들어 주셨습니다. 특히 기존 키워드 기반 검색을 Pinecone 임베딩 기반 유사도 검색으로 전환하는 큰 구조 변경을 주도하시고, 향수 문서를 직접 임베딩해 벡터로 업로드하는 과정까지 정확하게 구축해 검색 품질을 한 단계 끌어올려 주셨습니다. 프롬프트를 반복 개선하며 응답 품질을 끝까지 다듬어 주신 덕분에, AI 파이프라인이 프로젝트의 완성도를 높이는 결정적인 역할을 수행하셨습니다.
            </td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            Olfit 서비스의 프론트엔드 전반을 총괄하여, ‘향수 추천’ 이라는 서비스의 정체성이 직관적으로 드러나도록 UI/UX를 크게 향상해 주었습니다.  또한 UI 개발에 머무르지 않고 AWS EC2로의 배포 작업까지 성공적으로 완수해 주었습니다. 개발 초기 프로토타입에서 발생한 크고 작은 버그들을 AI 에이전트를 적극적으로 활용해 해결하고, backend에서 반환하는 데이터 스키마의 변경사항에 대해 바로 반영을 해 주는 등 긴밀한 협업을 할 수 있었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            프론트엔드 구현과 UI 구성 과정에서 사용자 흐름을 자연스럽게 연결해주었습니다. 이미지 업로드부터 추천 결과 표시까지 실제 서비스처럼 동작할 수 있도록 세부적인 화면 구성과 사용자 경험 개선에 신경 써주었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            프론트엔드를 담당한 팀원은 사용자 관점에서 UI/UX를 설계하고 개발해 주었습니다. 제가 바쁠 때는 AWS 클라우드 배포를 도맡아 처리해 주어 큰 부담을 덜 수 있었습니다. 제가 오랜만에 프론트 E2E 테스트를 맡아 막히는 부분이 있을 때마다 방향을 짚어 주었고, 제가 향수 도메인에 익숙하지 않은 부분도 어떤 데이터가 있으면 LLM이 더 잘 검색할 수 있는지 알려 주어 데이터 파이프라인 설계·구현에 큰 도움을 받았습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            서비스의 얼굴이 되는 프론트엔드 전 화면을 구현하고, API 실연동부터 AWS 배포까지 사용자 경험의 처음과 끝을 책임지셨습니다. 아우라 진단 결과를 Recharts 5축 레이더 차트로 시각화하고 추천 카드·정렬·로딩·오류 재시도 UI까지 촘촘하게 설계해, 막힘없이 자연스러운 사용자 경험을 만들어 주셨습니다. 특히 추천·분석 API를 실제로 연동하고 전체 플로우를 직접 QA하며 E2E 테스트에서 발견된 이슈까지 즉시 수정해 주신 덕분에, 백엔드와 프론트가 실제 환경에서 안정적으로 맞물릴 수 있었습니다. 나아가 AWS 프로덕션 배포까지 직접 챙기시며, 프로젝트가 데모를 넘어 실제로 동작하는 서비스로 완성되는 데 결정적인 역할을 수행하셨습니다.
            </td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            Olfit 서비스를 위한 Dockerfile을 작성하고, DB 설계를 함께 담당했습니다. 또한 Front/Back/LLM 전반에 대한 Test를 작성하여 서비스에 대한 성능 평가를 진행하고 파트별로 결과를 기록해 주었습니다. 이를 통해 우리의 시스템 파이프라인이 문제 없이 동작하며, 나아가 ‘RAG 검색 성능’과 ‘추천 성능’ 역시 검증할 수 있었습니다. 코드 리펙토링에 있어서도 Fallback 로직 등 놓친 디테일을 보완하여 완성도를 더욱 높였습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            인프라 및 배포 환경 구성 과정에서 프로젝트가 안정적으로 실행될 수 있도록 많은 역할을 맡아주었습니다. Docker, AWS 환경 세팅과 배포 과정에서 발생하는 문제들을 빠르게 해결하며 전체 개발 환경 안정화에 기여했습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            인프라 구축과 CI/CD 로 개발 환경에 통일을 담당해주셨습니다. 저 혼자만 다른 개발 환경에서 개발했지만, 환경의 차이에서 오는 오류를 사전에 방지했습니다. 
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            서비스를 실제로 동작하게 만드는 백엔드 API 서버와 인프라 전반을 도맡아, 프로젝트의 토대를 단단하게 받쳐 주셨습니다. 추천·향 정보 API를 설계·구현하고 통합 테스트로 다듬은 뒤, 응답 캐싱과 Pinecone 쿼리 비동기 처리까지 최적화해 무거운 AI 연산 속에서도 사용자가 빠르고 안정적인 응답을 받을 수 있도록 만들어 주셨습니다. 특히 이미지 분석 후 즉시 삭제하는 로직을 끝까지 확인하며 개인정보 보호까지 챙겨 주신 점이 인상 깊었습니다. 나아가 전 개발 도메인의 환경 세팅부터 배포 환경 구성, ETL 정규화, E2E 통합 테스트와 문서화로 품질 기준까지 세워 주신 덕분에, 프로젝트가 실제 환경에서 끝까지 동작하는 서비스로 완성될 수 있었습니다.
            </td>
        </tr>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd; padding: 10px;">최수아</td>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            3차 프로젝트때 경험을 바탕으로, Jira를 통한 일정 관리 및 기술 명세서 등 문서 작업, 발표를 맡아 주었습니다. 또한 Front 디자인에 대한 피드백과 표준화된 성분명 등을 조사해 주었습니다. 각자가 해야할 작업들이 명확하게 정의되어 있어 해당 jira issue를 가지고 commit을 날리며 관리할 수 있어 코드 관리도 편했던 것 같습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">장한재</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            PM 역할로 프로젝트 일정과 진행 상황을 체계적으로 관리해주었습니다. 발표 자료 구성과 전체 흐름 정리에서도 프로젝트 핵심 메시지가 잘 전달될 수 있도록 조율해주었고, 팀원 간 커뮤니케이션이 원활하게 이어질 수 있도록 중심을 잘 잡아주었습니다.
            </td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">전종혁</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
            일정 관리를 체계적으로 정리해주셔서 프로젝트 진행 중에 있어서 소통의 부재나, 팀원 간 소통을 원활하게 해주어서 프로젝트 기능 개발에만 몰두할 수 있었습니다.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd; padding: 10px;">조동휘</td>
            <td style="border: 1px solid #ddd; padding: 10px;">
             PM을 맡은 팀원은 프로젝트에서 가장 까다로운 일정 관리를 도맡았습니다. 각 파트의 진행 상황을 지속적으로 파악하고 우선순위를 조율해, 개발이 계획한 일정에서 벗어나지 않도록 이끌어 주었습니다. 덕분에 팀원 각자가 일정 부담 없이 자신의 개발에 집중할 수 있었습니다. 또한 향수 도메인에 대한 이해를 바탕으로, 데이터 수집 단계에서 여성 사용자가 주로 찾는 향수 브랜드가 무엇인지 짚어 주어 데이터 방향을 잡는 데 도움을 주었고, 향수 데이터를 어떤 형태로 출력해야 사용자에게 올바르게 전달되는지도 알려 주었습니다. 이런 디테일 덕분에 향수 추천 서비스가 사용자 관점에서 완성도 있는 결과물이 될 수 있었습니다.
            </td>
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
