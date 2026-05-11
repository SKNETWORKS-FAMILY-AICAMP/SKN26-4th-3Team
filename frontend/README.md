# Olfít Connect: AI-Driven Fragrance Matching Platform

나만의 시각적 아우라와 향기 취향을 연결하여 최적의 향수를 제안하는 **Olfít Connect** 프로젝트의 공식 풀스택 저장소입니다.

## 🌟 Overview

Olfít Connect는 사용자가 업로드한 이미지(OOTD, 공간, 무드 등)를 **NVIDIA NIM (Gemma VLM)**으로 정밀 분석하고, 사용자의 명시적 성분 취향을 결합하여 개인화된 '향기 아우라'를 도출합니다. 800여 개의 실제 향수 데이터를 기반으로 한 다차원 벡터 매칭 알고리즘을 통해 감성과 데이터의 완벽한 연결(Connect)을 제공합니다.

## 🏗️ Architecture

본 저장소는 프론트엔드와 백엔드가 통합된 모노레포 구조로 설계되었습니다.

```text
4th_olfit_connect_playground/
├── frontend/           # React + TypeScript + TailwindCSS + Vite
│   ├── src/            # UI 컴포넌트 및 클라이언트 로직
│   └── Dockerfile      # Vite 개발 서버 컨테이너
├── backend/            # Django 6 + Django REST Framework
│   ├── app/            # Django 소스 및 지능형 추천 엔진 (scent_engine)
│   └── requirements.txt # 백엔드 의존성 통합 관리
├── database/           # MySQL 8.4 Docker 설정 및 초기화 SQL
├── docker-compose.yml  # 전체 시스템 오케스트레이션
└── .env                # NVIDIA API 키 및 DB 자격 증명 (통합 관리)
```

## 🚀 Getting Started

### 1. 환경 변수 설정
루트 디렉토리(`.env`)에 필요한 키를 입력합니다.
```env
NVIDIA_API_KEY=your_nvidia_api_key_here
SQL_DB_PASSWORD=your_db_password
```

### 2. 전체 시스템 가동 (Docker)
Docker Compose를 통해 프론트엔드, 백엔드, 데이터베이스를 한 번에 구축합니다. 데이터베이스 마이그레이션 및 초기 데이터(800+ 향수) 적재가 자동으로 진행됩니다.
```powershell
docker compose up -d --build
```
*   **Frontend Web**: `http://localhost:3000`
*   **Backend API**: `http://localhost:8000`
*   **Database Host**: `localhost:3307` (External Access)

## 🧠 Key Features

- **AI Emotional Mapping**: 이미지에서 색상, 사물, 무드를 추출하여 5축(Floral, Woody, Oriental, Fresh, Gourmand) 아우라 스코어 산출.
- **Symmetric Scent Search**: 100% 한글화된 대칭형 쿼리를 생성하여 이미지의 감성과 향수의 노트를 직관적으로 매칭.
- **High-Resolution Insights**: 분석 결과를 레이더 차트와 함께 고해상도 이미지 리포트로 캡처 및 공유.
- **Hybrid Storage Strategy**: 관계형 메타데이터와 유연한 JSON 상세 정보를 결합한 고성능 하이브리드 아키텍처.

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Zustand, TailwindCSS, Framer Motion, html2canvas.
- **Backend**: Python 3.12, Django 6, DRF, OpenAI SDK (NVIDIA NIM).
- **AI/ML**: NVIDIA NIM (google/gemma-3n-e4b-it), NumPy, Scikit-learn.
- **Infrastructure**: Docker Compose, MySQL 8.4.

## 📝 License
이 프로젝트는 MIT License를 따릅니다.
