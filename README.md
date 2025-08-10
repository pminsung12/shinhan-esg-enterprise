# ShinhanESG Enterprise

<img style="max-width:100%; height:auto;" src="https://private-user-images.githubusercontent.com/52368015/476365749-f8cb844b-3828-4ed1-aa68-19d4efd8a799.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ4NDAwNzgsIm5iZiI6MTc1NDgzOTc3OCwicGF0aCI6Ii81MjM2ODAxNS80NzYzNjU3NDktZjhjYjg0NGItMzgyOC00ZWQxLWFhNjgtMTlkNGVmZDhhNzk5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEwVDE1MjkzOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWVjMGZkNWIzYTkwNzA2OTQ0MmQ3NDZjYTRkMmZhOTgzZTUxZGRjMzU0OGFkZTk4OWIzOGU4OTNhM2I5ZWM5Y2YmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.enD7L3sVr2S6H2yNRdB86Mu5eZjKzDiquPFsJIL7IOM" />

> 평가부터 금융상품 매칭까지 One-Stop 솔루션

![ESG Platform](https://img.shields.io/badge/ESG-Platform-blue) ![AI Powered](https://img.shields.io/badge/AI-Powered-green) ![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-red)

## Live Demo

**애플리케이션 배포 완료!**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shinhan-esg-enterprise.streamlit.app/)

> **Live Demo**: https://shinhan-esg-enterprise.streamlit.app/  
> 실제 기업 데이터로 ESG 평가부터 AI 예측, 금융상품 매칭까지 전체 플로우를 체험할 수 있습니다.

## Quick Start

### Prerequisites
- Python 3.9+
- Git

### Installation & Run

```bash
# 1. 리포지토리 클론
git clone https://github.com/pminsung12/shinhan-esg-enterprise.git
cd shinhan-esg-enterprise

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 애플리케이션 실행
streamlit run app_v4.py
```

브라우저에서 자동으로 `http://localhost:8501` 열림

### 프레젠테이션 모드 실행
```bash
streamlit run src/presentation_report.py
```

## 목차

- [시스템 아키텍처](#-시스템-아키텍처)
- [핵심 기능](#-핵심-기능)
- [기술 학습 과정](#-기술-학습-과정)
- [AI 모델링](#-ai-모델링)
- [화면 구성](#-화면-구성)
- [기술 스택](#-기술-스택)
- [성능 최적화](#-성능-최적화)
- [API 문서](#-api-문서)
- [확장 계획](#-확장-계획)

## 시스템 아키텍처

```
shinhan-esg-enterprise/
├── app_v4.py                     # 메인 애플리케이션 엔트리포인트
├── requirements.txt              # Python 의존성
├── src/                          # 비즈니스 로직
│   ├── enterprise_esg_engine.py    # ESG 평가 엔진
│   ├── ai_prediction_finance.py    # AI 예측 모델
│   ├── financial_products.py       # 금융상품 매칭
│   ├── supply_chain_analysis.py    # 공급망 ESG 분석
│   └── presentation_report.py      # 보고서 자동 생성
├── data/
│   └── sample_enterprises.json     # 기업 데이터 저장소
└── assets/                       # UI 리소스
```

### 데이터 플로우
```
[기업 데이터] → [ESG 평가 엔진] → [AI 예측 모델] → [금융상품 매칭] → [보고서 생성]
```

## 핵심 기능

### 1. ESG 평가 시스템
```python
# 신한은행 7등급 체계
GRADE_MAPPING = {
    (90, 100): ("A+", 2.7),  # 등급, 금리우대(%)
    (85, 89):  ("A",  2.2),
    (80, 84):  ("A-", 1.8),
    (75, 79):  ("B+", 1.3),
    (70, 74):  ("B",  0.8),
    (65, 69):  ("B-", 0.3),
    (0,  64):  ("C",  0.0)
}
```

**평가 영역:**
- **Environmental (30%)**: 탄소배출, 재생에너지, 친환경 투자
- **Social (35%)**: 임직원 만족도, 지역사회 기여, 공급망 관리  
- **Governance (35%)**: 이사회 독립성, 투명성, 리스크 관리

### 2. AI 예측 엔진
```python
class ESGPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
    def create_features(self, data):
        """시계열 특성 생성"""
        features = []
        # 이동평균 (3, 6개월)
        for window in [3, 6]:
            features.append(data.rolling(window).mean())
        
        # 변화율 (momentum)  
        features.append(data.pct_change())
        
        # 계절성 (분기별 패턴)
        features.append(data.groupby(data.index.quarter).transform('mean'))
        
        return pd.concat(features, axis=1)
```

**기업별 예측 패턴:**
- **대기업**: 안정적 성장형 (volatility: 0.08)
- **중견기업**: 변동성 성장형 (volatility: 0.25) 
- **금융업**: 급속 개선형 (acceleration: 1.2)

### 3. 금융상품 자동 매칭
```python
FINANCIAL_PRODUCTS = {
    "green_loan": {
        "name": "친환경시설자금대출",
        "base_rate": 3.5,
        "esg_discount": True,
        "conditions": {
            "min_e_score": 75,
            "renewable_ratio": 0.3
        }
    },
    "sustainability_bond": {
        "name": "지속가능채권",
        "issuance_cost": 0.15,
        "esg_benefit": 0.05
    }
}
```

### 4. 공급망 ESG 분석
- **Scope 3 배출량 계산**: 협력사 네트워크 분석
- **리스크 전파 모델링**: ESG 리스크 시뮬레이션
- **개선 인센티브 매칭**: 협력사 ESG 향상 프로그램

## AI 모델링

### Feature Engineering
```python
def engineer_features(historical_data):
    """ESG 시계열 데이터 특성 추출"""
    
    # 1. 시간 기반 특성
    features = {
        'month': historical_data.index.month,
        'quarter': historical_data.index.quarter,
        'year': historical_data.index.year
    }
    
    # 2. 통계적 특성  
    for metric in ['E', 'S', 'G']:
        # 이동평균 (노이즈 제거)
        features[f'{metric}_ma3'] = data[metric].rolling(3).mean()
        features[f'{metric}_ma6'] = data[metric].rolling(6).mean()
        
        # 변동성 (표준편차)
        features[f'{metric}_std'] = data[metric].rolling(6).std()
        
        # 모멘텀 (변화율)
        features[f'{metric}_momentum'] = data[metric].pct_change(3)
    
    # 3. ESG 균형 지표
    features['esg_balance'] = data[['E','S','G']].std(axis=1)
    
    return pd.DataFrame(features)
```

### 예측 정확도
- **MAPE (평균 절대 백분율 오차)**: 8.5%
- **R² Score**: 0.87 (E), 0.83 (S), 0.85 (G)
- **예측 신뢰구간**: 95%

## 📱 화면 구성

### 메인 대시보드
<img src="https://private-user-images.githubusercontent.com/52368015/476371358-4fdcca93-db6e-4293-8adb-c44538ce68da.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ4NDUwODQsIm5iZiI6MTc1NDg0NDc4NCwicGF0aCI6Ii81MjM2ODAxNS80NzYzNzEzNTgtNGZkY2NhOTMtZGI2ZS00MjkzLThhZGItYzQ0NTM4Y2U2OGRhLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEwVDE2NTMwNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTVjZDI0M2U4OTJhMGFlN2Y4Y2ZiMjBlNzlkMWNiNzYzNWI1NWYxNzk2NTA3ODIxZDM3ZjA4NGMxNDU2MDExZGQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.EOKe-OMFtG-zGUHy5Yq0KVteIiDJiZlBr_efpK_r_HI" alt="메인 대시보드" style="width: 100%; max-width: 800px;">

- **ESG 종합 점수 게이지 차트**: 실시간 점수 업데이트
- **E-S-G 영역별 레이더 차트**: 균형잡힌 ESG 성과 시각화
- **업종 벤치마킹 비교**: 동종 업계 대비 상대적 위치

### AI 예측 분석
<img src="https://private-user-images.githubusercontent.com/52368015/476369757-53aec168-6b49-4b08-84f1-c4057b7d901d.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ4NDUwODQsIm5iZiI6MTc1NDg0NDc4NCwicGF0aCI6Ii81MjM2ODAxNS80NzYzNjk3NTctNTNhZWMxNjgtNmI0OS00YjA4LTg0ZjEtYzQwNTdiN2Q5MDFkLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEwVDE2NTMwNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWMyY2JlYjY0ZmUwZTYzODc3NDA3NjVjZjI1MjA4OTQ4M2U4NzVjZGEzNDBhNmI0OTkyOTdlMTY0NjBjOTRkZTYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.0lXN9Ielq_xmJAPJ9tN5hJ_rGZ7iPtjpOYBO02ap5NE" alt="AI 예측 분석" style="width: 100%; max-width: 800px;">

- **1년/3년 예측 시계열 차트**: 신뢰구간을 포함한 미래 성과 예측
- **시나리오별 ROI 계산**: 투자 대비 ESG 개선 효과 분석
- **개선 우선순위 히트맵**: 가장 효율적인 개선 영역 추천

### 금융상품 매칭
<img src="https://private-user-images.githubusercontent.com/52368015/476369767-377a5d3b-fd07-467b-a980-a8d2fa993c70.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ4NDUwODQsIm5iZiI6MTc1NDg0NDc4NCwicGF0aCI6Ii81MjM2ODAxNS80NzYzNjk3NjctMzc3YTVkM2ItZmQwNy00NjdiLWE5ODAtYThkMmZhOTkzYzcwLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEwVDE2NTMwNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTRlMmRjM2FlZDJmNzAzYTE5OGE2NjMyM2I3OWFiYzc2ZTA3M2ExOTZjNWQyNDE3YzUyYjI0ZWVhZjE4YjgwMzcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.bk1CButSXIrUz-m7suMGtT-L1xDcWPVQjiugQ23bRbg" alt="금융상품 매칭" style="width: 100%; max-width: 800px;">

- **등급별 금리 우대 계산기**: ESG 등급에 따른 실시간 금리 혜택 계산
- **상품 조건 매칭 현황**: 6개 ESG 연계 금융상품 자동 매칭
- **5년 누적 혜택 시뮬레이션**: 장기 금융 혜택 예측

### 프레젠테이션 모드
<img src="https://private-user-images.githubusercontent.com/52368015/476370022-98df46f2-9c99-4ac9-b583-8f67bd9d1639.gif?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ4NDUwODQsIm5iZiI6MTc1NDg0NDc4NCwicGF0aCI6Ii81MjM2ODAxNS80NzYzNzAwMjItOThkZjQ2ZjItOWM5OS00YWM5LWI1ODMtOGY2N2JkOWQxNjM5LmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEwVDE2NTMwNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWFjNDA4NjQ3Y2ZiMzViMDI5ZTg3ZTcyZTYxNjQ0ZTgzMzgxZGFmM2Y2OWVmYjkzNjY0YjkxMTlkZTE5ZTJhMGMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.II6pTUdqdT7WIb4PtkehIbcHqzoY9Vooi-KfIxH7Lnw" alt="프레젠테이션 모드" style="width: 100%; max-width: 800px;">

- **10페이지 자동 슬라이드 생성**: ESG 평가 결과를 경영진 보고용으로 변환
- **실시간 발표 모드**: 클릭 네비게이션으로 프레젠테이션 진행
- **PDF/Excel 다운로드**: 보고서 및 데이터 즉시 내보내기

## 기술 스택

| 계층 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **Frontend** | Streamlit | 1.31.1 | 웹 UI, 대시보드 |
| **Backend** | Python | 3.9+ | 비즈니스 로직 |
| **AI/ML** | scikit-learn | 1.4.0 | 머신러닝 모델 |
| **Data** | pandas, numpy | 2.2.3, 1.26.3 | 데이터 처리 |
| **Visualization** | Plotly | 5.18.0 | 인터랙티브 차트 |
| **Export** | openpyxl | 3.1.2 | Excel 리포트 |

### 학습 방법
- 유튜브 강의로 실전 활용 패턴과 키워드 위주 공부
- 키워드 검색으로 공식문서나 생성형 AI를 통한 정확한 개념 이해

### 핵심 의존성
```txt
streamlit==1.31.1      # 웹 애플리케이션 프레임워크
pandas==2.2.3          # 데이터 분석 및 조작
scikit-learn==1.4.0    # 머신러닝 모델
plotly==5.18.0         # 인터랙티브 시각화
numpy==1.26.3          # 수치 계산
openpyxl==3.1.2        # Excel 파일 처리

## API 문서

### ESG 평가 API
```python
def calculate_esg_score(company_data: dict) -> dict:
    """
    ESG 종합 점수 계산
    
    Args:
        company_data: {
            "name": str,
            "industry": str,
            "environmental": dict,
            "social": dict, 
            "governance": dict
        }
    
    Returns:
        {
            "total_score": float,
            "grade": str,
            "interest_discount": float,
            "breakdown": {
                "E": float, "S": float, "G": float
            }
        }
    """
```

### AI 예측 API
```python
def predict_esg_future(company_name: str, months: int) -> dict:
    """
    ESG 미래 성과 예측
    
    Args:
        company_name: 기업명
        months: 예측 기간 (12 or 36)
    
    Returns:
        {
            "predictions": {
                "E": [float], "S": [float], "G": [float]
            },
            "confidence_intervals": dict,
            "improvement_scenarios": dict
        }
    """
```

## 확장 계획

### Phase 1: 데이터 강화
- 외부 ESG 데이터 제공업체 API
- Isolation Forest 기반 데이터 품질 검증
- DB 마이그레이션

### Phase 2: AI 고도화
- LSTM 모델로 장기 시계열 예측 정확도 향상
- 앙상블 학습: RandomForest + XGBoost 결합
- AutoML: 기업별 최적 모델 자동 선택

### Phase 3: 플랫폼화
- RESTful API로 마이크로서비스 아키텍처
- 멀티테넌트: 기업별 독립 데이터 공간
- Prometheus + Grafana로 실시간 모니터링

## 성과 지표

### 기술적 성과
- **개발 기간**: 7일 (2024.08.03-08.10)
- **코드 라인**: 2,847줄 (주석 제외)
- **모델 정확도**: 85%+ (MAPE 8.5%)
- **응답 시간**: 평균 2.3초

### 비즈니스 성과 (예상)
- ESG 평가 시간 단축
- 컨설팅 비용 절약
- ESG 대출 상품 판매 등으로 수익

---

**Developer**: 박민성  
**Organization**: 신한은행 ICT 인턴  
**Period**: 2025.08.02 - 2025.08.10 