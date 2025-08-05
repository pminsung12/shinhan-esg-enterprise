# ShinhanESG Enterprise

대기업 ESG 통합관리 플랫폼 - 신한은행 ICT 인턴 프로젝트

## 프로젝트 개요

2026년 ESG 의무공시에 대응하는 대기업을 위한 AI 기반 ESG 평가 및 금융상품 연계 플랫폼입니다.

### 주요 기능

- 🤖 **AI 기반 자동 평가**: 신한은행 7등급 체계 적용
- 📈 **미래 예측**: 12개월 ESG 점수 예측
- 💰 **금융상품 자동 매칭**: 등급별 최대 2.7%p 금리 우대
- 🔗 **공급망 분석**: Scope 3 배출량 자동 계산
- 📋 **규제 대응**: K-Taxonomy, TCFD, GRI 자동 매핑

## 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Machine Learning**: scikit-learn

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/your-repo/shinhan-esg-enterprise.git
cd shinhan-esg-enterprise
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

## 실행 방법

### 메인 대시보드
```bash
streamlit run app.py
```

### 프레젠테이션 모드
```bash
streamlit run src/executive_presentation.py
```

## 프로젝트 구조

```
shinhan-esg-enterprise/
├── app.py                      # 메인 애플리케이션
├── requirements.txt            # 의존성 패키지
├── README.md                  # 프로젝트 문서
├── .gitignore                 # Git 제외 파일
├── src/                       # 소스 코드
│   ├── __init__.py
│   ├── enterprise_esg_engine.py    # ESG 평가 엔진
│   ├── ai_prediction_finance.py    # AI 예측 및 금융상품 매칭
│   ├── data_collector.py           # 데이터 수집
│   └── executive_presentation.py   # 프레젠테이션 모드
├── data/                      # 데이터 파일
│   ├── sample_enterprises.json     # 샘플 기업 데이터
│   └── financial_products.json     # 금융상품 데이터
└── assets/                    # 정적 자원
    └── style.css              # 커스텀 스타일

```

## 사용 방법

1. 애플리케이션 실행 후 좌측 사이드바에서 평가 대상 기업 선택
2. "ESG 평가 실행" 버튼 클릭
3. 평가 결과 확인:
   - 상세 분석: ESG 영역별 점수
   - AI 예측: 향후 12개월 점수 예측
   - 금융상품: 맞춤형 상품 추천
   - 개선 로드맵: 단계별 실행 계획

## 개발자 정보

- 프로젝트명: ShinhanESG Enterprise
- 개발 기간: 2024.01 (1주일)
- 개발 목적: 신한은행 ICT 인턴 프로젝트

## 라이선스

This project is proprietary and confidential.