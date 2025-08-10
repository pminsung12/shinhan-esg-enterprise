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
    
    def generate_historical_data(self, current_scores: Dict, periods: int = 24, company_name: str = None) -> pd.DataFrame:
        """과거 데이터 시뮬레이션 생성
        
        Args:
            current_scores: 현재 ESG 점수
            periods: 생성할 과거 기간 수 (월 단위)
            company_name: 기업명 (패턴 다양화용)
        
        Returns:
            시계열 데이터프레임
        """
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='M')
        
        # 기업별 다양한 패턴 정의 - 현재 성과 수준에 맞춰 조정
        company_patterns = {
            "삼성전자": {
                "trend_type": "steady_growth",  # 우수 기업의 안정적 성장
                "e_trend": 0.2, "s_trend": 0.15, "g_trend": 0.1,
                "volatility": 0.008, "seasonal_strength": 0.02,
                "shock_points": [],  # 안정적 운영
                "recovery_speed": 0.95
            },
            "SK하이닉스": {
                "trend_type": "declining_then_recovery",  # 저성과에서 회복 시도
                "e_trend": -0.3, "s_trend": -0.2, "g_trend": -0.1,
                "volatility": 0.035, "seasonal_strength": 0.06,
                "recovery_point": 12,
                "recovery_speed": 0.5
            },
            "KB금융그룹": {
                "trend_type": "rapid_improvement",  # 중상위 기업의 급속 개선
                "e_trend": 0.4, "s_trend": 0.3, "g_trend": 0.35,
                "volatility": 0.012, "seasonal_strength": 0.025,
                "acceleration_point": 8,
                "recovery_speed": 0.85
            },
            "신한금융그룹": {
                "trend_type": "plateau",
                "e_trend": 0.2, "s_trend": 0.2, "g_trend": 0.3,
                "volatility": 0.008, "seasonal_strength": 0.02,
                "plateau_start": 12,
                "recovery_speed": 0.95
            },
            "국민은행": {
                "trend_type": "volatile_growth",
                "e_trend": 0.35, "s_trend": 0.45, "g_trend": 0.25,
                "volatility": 0.03, "seasonal_strength": 0.06,
                "shock_frequency": 3,
                "recovery_speed": 0.5
            },
            "LG화학": {
                "trend_type": "s_curve",
                "e_trend": 0.7, "s_trend": 0.3, "g_trend": 0.2,
                "volatility": 0.02, "seasonal_strength": 0.04,
                "inflection_point": 12,
                "recovery_speed": 0.7
            },
            "현대자동차": {
                "trend_type": "stepwise",
                "e_trend": 0.3, "s_trend": 0.4, "g_trend": 0.35,
                "volatility": 0.012, "seasonal_strength": 0.03,
                "step_points": [6, 12, 18],
                "recovery_speed": 0.85
            },
            "포스코": {
                "trend_type": "declining_then_recovery",
                "e_trend": -0.2, "s_trend": 0.1, "g_trend": 0.15,
                "volatility": 0.018, "seasonal_strength": 0.04,
                "recovery_point": 14,
                "recovery_speed": 0.6
            },
            "네이버": {
                "trend_type": "volatile_growth",  # 중간 성과에서 변동성 있는 성장
                "e_trend": 0.25, "s_trend": 0.2, "g_trend": 0.3,
                "volatility": 0.025, "seasonal_strength": 0.04,
                "shock_frequency": 4,
                "recovery_speed": 0.7
            },
            "한화그룹": {
                "trend_type": "irregular",
                "e_trend": 0.25, "s_trend": 0.35, "g_trend": 0.3,
                "volatility": 0.04, "seasonal_strength": 0.07,
                "randomness": 0.5,
                "recovery_speed": 0.4
            }
        }
        
        # 기본 패턴 (기업명이 없거나 정의되지 않은 경우)
        default_pattern = {
            "trend_type": "steady_growth",
            "e_trend": 0.3, "s_trend": 0.3, "g_trend": 0.3,
            "volatility": 0.02, "seasonal_strength": 0.04,
            "recovery_speed": 0.7
        }
        
        # 기업별 패턴 선택
        pattern = company_patterns.get(company_name, default_pattern)
        
        # 랜덤 시드를 기업명 기반으로 설정 (일관성 유지하면서 다양성 확보)
        if company_name:
            np.random.seed(hash(company_name) % 2**32)
        else:
            np.random.seed(42)
        
        data = []
        
        # 초기 점수 설정 (현재 점수 기준으로 과거로 갈수록 낮게 설정)
        # 개선: 현재 점수에서 합리적인 범위 내에서 시작
        initial_reduction = 0.7 + np.random.uniform(0, 0.15)  # 70-85% 수준에서 시작
        e_score = current_scores['E'] * initial_reduction
        s_score = current_scores['S'] * initial_reduction
        g_score = current_scores['G'] * initial_reduction
        
        for i, date in enumerate(dates):
            progress = i / periods
            
            # 트렌드 타입별 처리
            if pattern["trend_type"] == "steady_growth":
                e_trend = pattern["e_trend"] * progress
                s_trend = pattern["s_trend"] * progress
                g_trend = pattern["g_trend"] * progress
                
            elif pattern["trend_type"] == "cyclical":
                cycle = np.sin(2 * np.pi * i / pattern.get("cycle_period", 8))
                e_trend = pattern["e_trend"] * progress + 0.1 * cycle
                s_trend = pattern["s_trend"] * progress + 0.08 * cycle
                g_trend = pattern["g_trend"] * progress + 0.05 * cycle
                
            elif pattern["trend_type"] == "rapid_improvement":
                if i > pattern.get("acceleration_point", 10):
                    acceleration = (i - pattern["acceleration_point"]) / periods
                    e_trend = pattern["e_trend"] * progress * (1 + acceleration)
                    s_trend = pattern["s_trend"] * progress * (1 + acceleration * 0.8)
                    g_trend = pattern["g_trend"] * progress * (1 + acceleration * 0.6)
                else:
                    e_trend = pattern["e_trend"] * progress * 0.3
                    s_trend = pattern["s_trend"] * progress * 0.3
                    g_trend = pattern["g_trend"] * progress * 0.3
                    
            elif pattern["trend_type"] == "plateau":
                if i < pattern.get("plateau_start", 12):
                    e_trend = pattern["e_trend"] * progress * 2
                    s_trend = pattern["s_trend"] * progress * 2
                    g_trend = pattern["g_trend"] * progress * 2
                else:
                    e_trend = pattern["e_trend"] * 0.5
                    s_trend = pattern["s_trend"] * 0.5
                    g_trend = pattern["g_trend"] * 0.5
                    
            elif pattern["trend_type"] == "volatile_growth":
                shock = 0
                if i % (periods // pattern.get("shock_frequency", 3)) == 0:
                    shock = np.random.uniform(-0.2, 0.2)
                e_trend = pattern["e_trend"] * progress + shock
                s_trend = pattern["s_trend"] * progress + shock * 0.8
                g_trend = pattern["g_trend"] * progress + shock * 0.6
                
            elif pattern["trend_type"] == "s_curve":
                x = (i - pattern.get("inflection_point", 12)) / 6
                sigmoid = 1 / (1 + np.exp(-x))
                e_trend = pattern["e_trend"] * sigmoid
                s_trend = pattern["s_trend"] * sigmoid
                g_trend = pattern["g_trend"] * sigmoid
                
            elif pattern["trend_type"] == "stepwise":
                step_value = 0
                for step_point in pattern.get("step_points", [6, 12, 18]):
                    if i >= step_point:
                        step_value += 0.2
                e_trend = pattern["e_trend"] * step_value
                s_trend = pattern["s_trend"] * step_value
                g_trend = pattern["g_trend"] * step_value
                
            elif pattern["trend_type"] == "declining_then_recovery":
                if i < pattern.get("recovery_point", 14):
                    e_trend = pattern["e_trend"] * (1 - progress * 0.5)
                    s_trend = pattern["s_trend"] * (1 - progress * 0.3)
                    g_trend = pattern["g_trend"] * (1 - progress * 0.2)
                else:
                    recovery_progress = (i - pattern["recovery_point"]) / (periods - pattern["recovery_point"])
                    e_trend = pattern["e_trend"] + 0.8 * recovery_progress
                    s_trend = pattern["s_trend"] + 0.6 * recovery_progress
                    g_trend = pattern["g_trend"] + 0.5 * recovery_progress
                    
            elif pattern["trend_type"] == "exponential":
                growth_rate = pattern.get("growth_rate", 0.1)
                e_trend = pattern["e_trend"] * (np.exp(growth_rate * progress) - 1)
                s_trend = pattern["s_trend"] * (np.exp(growth_rate * progress * 0.8) - 1)
                g_trend = pattern["g_trend"] * (np.exp(growth_rate * progress * 0.6) - 1)
                
            else:  # irregular
                e_trend = pattern["e_trend"] * progress + np.random.uniform(-0.1, 0.1)
                s_trend = pattern["s_trend"] * progress + np.random.uniform(-0.08, 0.08)
                g_trend = pattern["g_trend"] * progress + np.random.uniform(-0.06, 0.06)
            
            # 계절성 추가
            seasonal_e = np.sin(2 * np.pi * i / 4) * pattern["seasonal_strength"]
            seasonal_s = np.sin(2 * np.pi * i / 4 + np.pi/3) * pattern["seasonal_strength"] * 0.8
            seasonal_g = np.sin(2 * np.pi * i / 4 + 2*np.pi/3) * pattern["seasonal_strength"] * 0.6
            
            # 노이즈 추가
            noise_e = np.random.normal(0, pattern["volatility"])
            noise_s = np.random.normal(0, pattern["volatility"] * 0.8)
            noise_g = np.random.normal(0, pattern["volatility"] * 0.6)
            
            # 점수 계산 - 현재 점수를 향해 점진적으로 증가
            # 목표: 마지막 기간에 현재 점수에 근접하도록
            target_progress = (i + 1) / periods
            
            # 현재 점수를 향한 수렴
            e_target = current_scores['E']
            s_target = current_scores['S']
            g_target = current_scores['G']
            
            # 부드러운 수렴을 위한 가중치
            convergence_weight = target_progress ** 1.5
            
            # 트렌드, 계절성, 노이즈를 포함한 점수 계산
            e_score = e_score + (e_target - e_score) * convergence_weight * 0.1 + e_trend + seasonal_e * 2 + noise_e * 3
            s_score = s_score + (s_target - s_score) * convergence_weight * 0.1 + s_trend + seasonal_s * 2 + noise_s * 3
            g_score = g_score + (g_target - g_score) * convergence_weight * 0.1 + g_trend + seasonal_g * 2 + noise_g * 3
            
            # 충격 포인트 처리
            if pattern["trend_type"] == "steady_growth" and i in pattern.get("shock_points", []):
                shock_impact = np.random.uniform(-15, -5)
                e_score += shock_impact
                s_score += shock_impact * 0.7
                g_score += shock_impact * 0.5
            
            # 회복 속도 적용
            if i > 0:
                recovery = pattern["recovery_speed"]
                e_score = e_score * recovery + data[-1]['E'] * (1 - recovery)
                s_score = s_score * recovery + data[-1]['S'] * (1 - recovery)
                g_score = g_score * recovery + data[-1]['G'] * (1 - recovery)
            
            # 경계값 처리
            e_score = max(0, min(100, e_score))
            s_score = max(0, min(100, s_score))
            g_score = max(0, min(100, g_score))
            
            # 마지막 몇 개월은 현재 점수에 더 가깝게 조정
            if i >= periods - 3:
                final_weight = 0.7 + 0.1 * (i - (periods - 3))
                e_score = e_score * (1 - final_weight) + current_scores['E'] * final_weight
                s_score = s_score * (1 - final_weight) + current_scores['S'] * final_weight
                g_score = g_score * (1 - final_weight) + current_scores['G'] * final_weight
            
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
    
    def predict_future_scores(self, historical_data: pd.DataFrame, periods: int = 12, company_name: str = None) -> pd.DataFrame:
        """미래 ESG 점수 예측
        
        Args:
            historical_data: 과거 데이터
            periods: 예측 기간 (월 단위)
            company_name: 기업명 (예측 다양성용)
        
        Returns:
            예측 결과 데이터프레임
        """
        predictions = []
        last_date = historical_data['date'].max()
        
        # 기업별 예측 특성 정의 - 현재 성과 수준에 맞춰 조정
        company_prediction_traits = {
            "삼성전자": {"momentum": 0.85, "volatility": 0.08, "improvement_cap": 0.15},  # 우수: 안정적
            "SK하이닉스": {"momentum": 0.3, "volatility": 0.35, "improvement_cap": 0.6},  # 저성과: 높은 개선 가능성
            "KB금융그룹": {"momentum": 0.75, "volatility": 0.12, "improvement_cap": 0.3},  # 중상위: 꾸준한 개선
            "신한금융그룹": {"momentum": 0.85, "volatility": 0.08, "improvement_cap": 0.25},
            "국민은행": {"momentum": 0.4, "volatility": 0.3, "improvement_cap": 0.35},
            "LG화학": {"momentum": 0.8, "volatility": 0.2, "improvement_cap": 0.6},
            "현대자동차": {"momentum": 0.6, "volatility": 0.12, "improvement_cap": 0.4},
            "포스코": {"momentum": 0.3, "volatility": 0.18, "improvement_cap": 0.5},
            "네이버": {"momentum": 0.55, "volatility": 0.25, "improvement_cap": 0.4},  # 중간: 변동성 있는 성장
            "한화그룹": {"momentum": 0.2, "volatility": 0.4, "improvement_cap": 0.3}
        }
        
        traits = company_prediction_traits.get(company_name, {"momentum": 0.5, "volatility": 0.15, "improvement_cap": 0.4})
        
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
                    base_pred = self.models[target].predict(X_scaled)[0]
                    
                    # 기업별 특성 적용
                    last_value = extended_df[target].iloc[-1]
                    
                    # 모멘텀 효과 (이전 추세 반영)
                    if len(extended_df) >= 3:
                        recent_trend = extended_df[target].tail(3).diff().mean()
                        momentum_effect = recent_trend * traits['momentum']
                    else:
                        momentum_effect = 0
                    
                    # 변동성 추가
                    volatility_effect = np.random.normal(0, traits['volatility'] * 5)
                    
                    # 개선 한계 적용 (너무 급격한 개선 방지)
                    max_improvement = last_value * (1 + traits['improvement_cap'] / 12)
                    
                    # 최종 예측값 계산 - 모델 예측과 현재값의 가중 평균
                    # 초기에는 현재값에 더 가중치를 두고, 점진적으로 모델 예측에 가중치 증가
                    model_weight = min(0.7, i / periods)  # 최대 70%까지만 모델에 의존
                    current_weight = 1 - model_weight
                    
                    final_pred = (base_pred * model_weight + last_value * current_weight) + momentum_effect + volatility_effect
                    final_pred = min(final_pred, max_improvement)
                    
                    # 기업별 특수 조건
                    if company_name == "포스코" and i > 6:
                        # 회복 패턴
                        final_pred = final_pred * 1.05
                    elif company_name == "신한금융그룹" and final_pred > 85:
                        # 고점 정체
                        final_pred = final_pred * 0.98
                    elif company_name == "네이버":
                        # 지속적 혁신
                        final_pred = final_pred * 1.02
                    
                    pred_scores[target] = max(0, min(100, final_pred))
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
    
    def calculate_financial_impact(self, score_improvement: float, loan_amount: float = 1000) -> Dict:
        """ESG 개선의 금융적 영향 계산
        
        Args:
            score_improvement: 점수 개선 폭
            loan_amount: 대출 금액 (억원)
        
        Returns:
            금융적 영향 분석
        """
        # 점수별 금리 우대율 (선형 보간)
        def get_rate_discount(score):
            if score >= 90:
                return 2.7
            elif score >= 85:
                return 2.2
            elif score >= 80:
                return 1.8
            elif score >= 75:
                return 1.5
            elif score >= 70:
                return 1.2
            elif score >= 65:
                return 0.8
            else:
                return 0.4
        
        current_discount = get_rate_discount(score_improvement)
        
        # 연간 이자 절감액
        annual_savings = loan_amount * current_discount / 100
        
        # 5년간 누적 절감액
        cumulative_savings_5y = annual_savings * 5
        
        # ESG 투자 대비 수익률
        # (일반적으로 ESG 개선 비용은 대출액의 0.5-2%)
        estimated_esg_cost = loan_amount * 0.01  # 1% 가정
        roi_5y = (cumulative_savings_5y / estimated_esg_cost - 1) * 100 if estimated_esg_cost > 0 else 0
        
        return {
            'rate_discount': current_discount,
            'annual_savings': annual_savings,
            'cumulative_savings_5y': cumulative_savings_5y,
            'estimated_esg_cost': estimated_esg_cost,
            'roi_5y': roi_5y,
            'payback_period': estimated_esg_cost / annual_savings if annual_savings > 0 else float('inf')
        }
    
    def generate_scenario_analysis(self, current_scores: Dict, scenarios: List[Dict]) -> pd.DataFrame:
        """시나리오별 영향 분석
        
        Args:
            current_scores: 현재 ESG 점수
            scenarios: 시나리오 리스트
        
        Returns:
            시나리오 분석 결과
        """
        results = []
        
        for scenario in scenarios:
            # 시나리오별 점수 변화 계산
            new_scores = current_scores.copy()
            
            if 'improvements' in scenario:
                for improvement in scenario['improvements']:
                    area = improvement['area']
                    impact = improvement['impact']
                    new_scores[area] = min(100, new_scores[area] + impact)
            
            # 새로운 총점 계산
            new_scores['total'] = (
                new_scores['E'] * 0.35 +
                new_scores['S'] * 0.35 +
                new_scores['G'] * 0.3
            )
            
            # 금융적 영향 계산
            financial_impact = self.calculate_financial_impact(new_scores['total'])
            
            results.append({
                'scenario': scenario['name'],
                'new_score': new_scores['total'],
                'score_change': new_scores['total'] - current_scores['total'],
                'new_grade': self._score_to_grade(new_scores['total']),
                'rate_discount': financial_impact['rate_discount'],
                'annual_savings': financial_impact['annual_savings'],
                'investment': scenario.get('investment', 0),
                'roi': financial_impact['roi_5y']
            })
        
        return pd.DataFrame(results)
    
    def _score_to_grade(self, score: float) -> str:
        """점수를 등급으로 변환"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        else:
            return "C"
    
    def get_prediction_confidence(self, predictions: pd.DataFrame) -> Dict:
        """예측 신뢰도 계산
        
        Args:
            predictions: 예측 결과
        
        Returns:
            신뢰도 정보
        """
        # 예측 변동성 계산
        volatility = {
            'E': predictions['E'].std(),
            'S': predictions['S'].std(),
            'G': predictions['G'].std(),
            'total': predictions['total'].std()
        }
        
        # 신뢰 구간 계산 (95%)
        confidence_intervals = {}
        for col in ['E', 'S', 'G', 'total']:
            mean = predictions[col].mean()
            std = predictions[col].std()
            confidence_intervals[col] = {
                'lower': mean - 1.96 * std,
                'upper': mean + 1.96 * std
            }
        
        # 전체 신뢰도 점수 (0-100)
        avg_volatility = np.mean(list(volatility.values()))
        confidence_score = max(0, min(100, 100 - avg_volatility * 2))
        
        return {
            'confidence_score': confidence_score,
            'volatility': volatility,
            'confidence_intervals': confidence_intervals,
            'reliability': 'high' if confidence_score > 80 else 'medium' if confidence_score > 60 else 'low'
        }