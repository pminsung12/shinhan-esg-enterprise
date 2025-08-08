"""
AI 기반 ESG 예측 및 금융 분석 모듈
시계열 예측, 개선 동인 분석, ROI 시뮬레이션
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class AIPredictor:
    """AI 기반 ESG 예측 엔진"""
    
    def __init__(self):
        """초기화"""
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        
        # 예측 기간 설정
        self.prediction_periods = {
            "1Q": 3,
            "2Q": 6,
            "1Y": 12,
            "3Y": 36
        }
        
        # ESG 개선 요인별 영향도
        self.improvement_factors = {
            "environmental": {
                "renewable_energy_transition": {"impact": 15, "cost": 500, "time": 12},
                "carbon_reduction_tech": {"impact": 20, "cost": 800, "time": 18},
                "waste_management": {"impact": 10, "cost": 200, "time": 6},
                "water_efficiency": {"impact": 8, "cost": 150, "time": 9},
                "green_certification": {"impact": 5, "cost": 50, "time": 3}
            },
            "social": {
                "diversity_program": {"impact": 12, "cost": 100, "time": 6},
                "safety_enhancement": {"impact": 15, "cost": 300, "time": 9},
                "employee_wellbeing": {"impact": 10, "cost": 200, "time": 6},
                "community_engagement": {"impact": 8, "cost": 150, "time": 3},
                "supply_chain_audit": {"impact": 10, "cost": 250, "time": 12}
            },
            "governance": {
                "esg_committee": {"impact": 20, "cost": 50, "time": 3},
                "board_diversity": {"impact": 15, "cost": 30, "time": 6},
                "transparency_enhancement": {"impact": 12, "cost": 100, "time": 6},
                "risk_management": {"impact": 10, "cost": 200, "time": 9},
                "compliance_system": {"impact": 8, "cost": 300, "time": 12}
            }
        }
    
    def generate_historical_data(self, current_scores: Dict, periods: int = 24) -> pd.DataFrame:
        """과거 데이터 시뮬레이션 생성
        
        Args:
            current_scores: 현재 ESG 점수
            periods: 생성할 과거 기간 수 (월 단위)
        
        Returns:
            시계열 데이터프레임
        """
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='M')
        
        # 트렌드와 계절성을 포함한 시뮬레이션
        np.random.seed(42)
        
        data = []
        for i, date in enumerate(dates):
            # 기본 트렌드 (점진적 개선)
            trend_factor = i / periods
            
            # 계절성 (분기별 변동)
            seasonal_factor = np.sin(2 * np.pi * i / 4) * 0.05
            
            # 랜덤 노이즈
            noise = np.random.normal(0, 0.02)
            
            # 각 영역별 점수 생성
            e_score = current_scores['E'] * (0.7 + 0.3 * trend_factor) + seasonal_factor * 10 + noise * 5
            s_score = current_scores['S'] * (0.75 + 0.25 * trend_factor) + seasonal_factor * 8 + noise * 4
            g_score = current_scores['G'] * (0.8 + 0.2 * trend_factor) + seasonal_factor * 5 + noise * 3
            
            # 경계값 처리
            e_score = max(0, min(100, e_score))
            s_score = max(0, min(100, s_score))
            g_score = max(0, min(100, g_score))
            
            data.append({
                'date': date,
                'E': e_score,
                'S': s_score,
                'G': g_score,
                'total': (e_score * 0.35 + s_score * 0.35 + g_score * 0.3)
            })
        
        return pd.DataFrame(data)
    
    def train_prediction_model(self, historical_data: pd.DataFrame) -> Dict:
        """예측 모델 학습
        
        Args:
            historical_data: 과거 ESG 데이터
        
        Returns:
            학습된 모델 정보
        """
        # 특성 엔지니어링
        df = historical_data.copy()
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['trend'] = range(len(df))
        
        # 이동 평균 특성
        for col in ['E', 'S', 'G']:
            df[f'{col}_ma3'] = df[col].rolling(window=3, min_periods=1).mean()
            df[f'{col}_ma6'] = df[col].rolling(window=6, min_periods=1).mean()
        
        # 변화율 특성
        for col in ['E', 'S', 'G']:
            df[f'{col}_change'] = df[col].pct_change().fillna(0)
        
        # 학습 데이터 준비
        feature_cols = ['month', 'quarter', 'trend'] + \
                      [f'{x}_ma3' for x in ['E', 'S', 'G']] + \
                      [f'{x}_ma6' for x in ['E', 'S', 'G']] + \
                      [f'{x}_change' for x in ['E', 'S', 'G']]
        
        X = df[feature_cols].fillna(0)
        
        # 각 ESG 영역별 모델 학습
        for target in ['E', 'S', 'G', 'total']:
            y = df[target]
            
            # Random Forest 모델 사용
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            
            # 스케일링
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # 모델 학습
            model.fit(X_scaled, y)
            
            # 모델 저장
            self.models[target] = model
            self.scalers[target] = scaler
            
            # 특성 중요도 저장
            self.feature_importance[target] = dict(zip(feature_cols, model.feature_importances_))
        
        return {
            'status': 'success',
            'models_trained': list(self.models.keys()),
            'feature_count': len(feature_cols)
        }
    
    def predict_future_scores(self, historical_data: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
        """미래 ESG 점수 예측
        
        Args:
            historical_data: 과거 데이터
            periods: 예측 기간 (월 단위)
        
        Returns:
            예측 결과 데이터프레임
        """
        predictions = []
        last_date = historical_data['date'].max()
        
        # 학습 시와 동일한 특성 컬럼 정의
        feature_cols = ['month', 'quarter', 'trend'] + \
                      [f'{x}_ma3' for x in ['E', 'S', 'G']] + \
                      [f'{x}_ma6' for x in ['E', 'S', 'G']] + \
                      [f'{x}_change' for x in ['E', 'S', 'G']]
        
        # 확장된 데이터프레임 생성
        extended_df = historical_data.copy()
        
        for i in range(1, periods + 1):
            pred_date = last_date + timedelta(days=30 * i)
            
            # 특성 생성
            features = {
                'month': pred_date.month,
                'quarter': (pred_date.month - 1) // 3 + 1,
                'trend': len(extended_df) + i
            }
            
            # 이동 평균 계산
            for col in ['E', 'S', 'G']:
                recent_values = extended_df[col].tail(6).values
                features[f'{col}_ma3'] = np.mean(recent_values[-3:]) if len(recent_values) >= 3 else recent_values[-1]
                features[f'{col}_ma6'] = np.mean(recent_values) if len(recent_values) >= 6 else np.mean(recent_values)
                
                # 변화율
                if len(recent_values) >= 2:
                    features[f'{col}_change'] = (recent_values[-1] - recent_values[-2]) / recent_values[-2] if recent_values[-2] != 0 else 0
                else:
                    features[f'{col}_change'] = 0
            
            # 예측
            pred_scores = {}
            for target in ['E', 'S', 'G']:
                if target in self.models:
                    # 학습 시와 동일한 순서로 특성 생성
                    X_pred = pd.DataFrame([features])[feature_cols]
                    X_scaled = self.scalers[target].transform(X_pred)
                    pred_scores[target] = max(0, min(100, self.models[target].predict(X_scaled)[0]))
                else:
                    pred_scores[target] = extended_df[target].iloc[-1]
            
            # 총점 계산
            pred_scores['total'] = (
                pred_scores['E'] * 0.35 +
                pred_scores['S'] * 0.35 +
                pred_scores['G'] * 0.3
            )
            
            pred_scores['date'] = pred_date
            predictions.append(pred_scores)
            
            # 예측값을 다음 예측의 입력으로 사용
            extended_df = pd.concat([
                extended_df,
                pd.DataFrame([pred_scores])
            ], ignore_index=True)
        
        return pd.DataFrame(predictions)
    
    def analyze_improvement_drivers(self, current_scores: Dict, target_grade: str) -> Dict:
        """개선 동인 분석
        
        Args:
            current_scores: 현재 ESG 점수
            target_grade: 목표 등급
        
        Returns:
            개선 동인 분석 결과
        """
        # 목표 점수 계산 (등급별 최소 점수)
        grade_thresholds = {
            "A+": 90, "A": 85, "A-": 80,
            "B+": 75, "B": 70, "B-": 65,
            "C": 60
        }
        
        target_score = grade_thresholds.get(target_grade, 75)
        current_total = current_scores['total']
        gap = target_score - current_total
        
        if gap <= 0:
            return {
                'status': 'already_achieved',
                'message': f'이미 {target_grade} 등급 달성 가능한 점수입니다.'
            }
        
        # 각 영역별 개선 기회 분석
        recommendations = []
        total_cost = 0
        total_time = 0
        expected_improvement = 0
        
        # 영역별 가중치
        weights = {'E': 0.35, 'S': 0.35, 'G': 0.3}
        
        for area in ['environmental', 'social', 'governance']:
            area_key = area[0].upper()
            current_area_score = current_scores[area_key]
            
            # 개선 여지가 큰 영역 우선
            if current_area_score < 80:
                for factor, details in self.improvement_factors[area].items():
                    if expected_improvement < gap:
                        impact = details['impact'] * weights[area_key]
                        recommendations.append({
                            'area': area,
                            'factor': factor,
                            'impact': impact,
                            'cost': details['cost'],
                            'time': details['time'],
                            'priority': 'high' if current_area_score < 70 else 'medium'
                        })
                        total_cost += details['cost']
                        total_time = max(total_time, details['time'])
                        expected_improvement += impact
        
        # 우선순위 정렬
        recommendations.sort(key=lambda x: x['impact'] / x['cost'], reverse=True)
        
        return {
            'status': 'success',
            'current_score': current_total,
            'target_score': target_score,
            'gap': gap,
            'recommendations': recommendations[:5],  # 상위 5개 추천
            'total_cost': total_cost,
            'estimated_time': total_time,
            'expected_improvement': expected_improvement,
            'roi': (expected_improvement / total_cost * 100) if total_cost > 0 else 0
        }
    
   