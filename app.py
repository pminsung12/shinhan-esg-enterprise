"""
ShinhanESG Enterprise - 메인 애플리케이션
대기업 ESG 통합관리 플랫폼
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
import os

# src 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 로컬 모듈 import
from src.enterprise_esg_engine import EnterpriseESGEngine
from src.data_loader import DataLoader
from src.ai_prediction_finance import AIPredictor

# 페이지 설정
st.set_page_config(
    page_title="ShinhanESG Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 전역 객체 초기화
@st.cache_resource
def init_systems():
    """시스템 초기화"""
    return EnterpriseESGEngine(), DataLoader(), AIPredictor()

engine, data_loader, ai_predictor = init_systems()

def main():
    # 헤더
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("ShinhanESG Enterprise")
        st.subheader("대기업 ESG 통합관리 플랫폼 with AI")
    with col2:
        st.metric("Platform Version", "2.0", "AI Enhanced")
    with col3:
        st.metric("Date", datetime.now().strftime("%Y-%m-%d"))
    
    # 사이드바
    with st.sidebar:
        st.header("평가 설정")
        
        # 기업 선택
        enterprise_list = data_loader.get_enterprise_list()
        if enterprise_list:
            selected_enterprise = st.selectbox(
                "평가 대상 기업",
                enterprise_list
            )
            
            # 기업 정보 표시
            enterprise_data = data_loader.get_enterprise_data(selected_enterprise)
            if enterprise_data:
                st.markdown("### 📊 기업 정보")
                basic_info = enterprise_data.get('basic_info', {})
                st.metric("업종", basic_info.get('industry', 'N/A'))
                st.metric("자산규모", f"{basic_info.get('asset_size', 0):,}억원")
                st.metric("직원수", f"{basic_info.get('employee_count', 0):,}명")
                
                st.markdown("---")
                
                # 평가 옵션
                st.markdown("### ⚙️ 평가 옵션")
                enable_ai = st.checkbox("AI 예측 분석 활성화", value=True)
                prediction_period = st.select_slider(
                    "예측 기간",
                    options=["3개월", "6개월", "1년", "3년"],
                    value="1년"
                )
                
                # 평가 실행 버튼
                if st.button("🚀 ESG 평가 실행", type="primary", use_container_width=True):
                    with st.spinner("평가 진행 중..."):
                        # 기본 평가
                        st.session_state.evaluation_result = engine.evaluate_enterprise(enterprise_data)
                        st.session_state.selected_enterprise = selected_enterprise
                        
                        # AI 예측
                        if enable_ai:
                            st.session_state.ai_enabled = True
                            st.session_state.prediction_period = prediction_period
                            # AI 예측 실행
                            perform_ai_prediction(st.session_state.evaluation_result)
                        else:
                            st.session_state.ai_enabled = False
        else:
            st.error("데이터를 로드할 수 없습니다.")
    
    # 메인 컨텐츠
    if 'evaluation_result' in st.session_state:
        display_evaluation_results(st.session_state.evaluation_result)
    else:
        display_welcome_screen()
    
    # 푸터
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("신한은행 ICT 인턴 프로젝트")
    with col2:
        st.caption("ShinhanESG Enterprise v2.0")
    with col3:
        st.caption("Powered by AI & Big Data")

def perform_ai_prediction(evaluation: Dict):
    """AI 예측 수행"""
    current_scores = evaluation['scores']
    
    # 과거 데이터 생성
    historical_data = ai_predictor.generate_historical_data(current_scores, periods=24)
    
    # 모델 학습
    ai_predictor.train_prediction_model(historical_data)
    
    # 예측 기간 설정
    period_map = {"3개월": 3, "6개월": 6, "1년": 12, "3년": 36}
    periods = period_map.get(st.session_state.prediction_period, 12)
    
    # 미래 예측
    predictions = ai_predictor.predict_future_scores(historical_data, periods=periods)
    
    # 개선 동인 분석
    target_grade = "A" if evaluation['grade'].startswith("B") else "A+"
    improvement_analysis = ai_predictor.analyze_improvement_drivers(current_scores, target_grade)
    
    # 세션에 저장
    st.session_state.ai_predictions = {
        'historical': historical_data,
        'predictions': predictions,
        'improvement_analysis': improvement_analysis,
        'confidence': ai_predictor.get_prediction_confidence(predictions)
    }

def display_welcome_screen():
    """환영 화면"""
    st.markdown("""
    ### 환영합니다!
    
    **ShinhanESG Enterprise 2.0**는 AI 기반 대기업 ESG 통합관리 플랫폼입니다.
    
    #### 🆕 v2.0 새로운 기능
    - **🤖 AI 예측 모델**: 머신러닝 기반 ESG 점수 예측
    - **📈 시계열 분석**: 과거 트렌드 분석 및 미래 전망
    - **💡 개선 동인 분석**: AI가 추천하는 ESG 개선 전략
    - **💰 ROI 시뮬레이션**: 투자 대비 수익률 분석
    
    #### 주요 기능
    - **신한은행 7등급 체계** 기반 정밀 평가
    - **업종별 맞춤형** 가중치 적용
    - **금융상품 자동 매칭** 및 혜택 계산
    - **규제 준수도** 실시간 모니터링
    
    #### 시작하기
    1. 좌측 사이드바에서 평가 대상 기업 선택
    2. AI 예측 옵션 설정
    3. "ESG 평가 실행" 버튼 클릭
    4. 상세 평가 결과 및 AI 인사이트 확인
    
    ---
    
    💡 **Tip**: AI 예측 기능을 활용하여 미래 ESG 성과를 예측하고 
    전략적 의사결정을 내리세요!
    """)
    
    # 샘플 차트
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(data=[
            go.Bar(name='현재', x=['E', 'S', 'G'], y=[75, 82, 88], marker_color='lightblue'),
            go.Bar(name='목표', x=['E', 'S', 'G'], y=[85, 90, 92], marker_color='darkblue')
        ])
        fig.update_layout(title="ESG 점수 목표", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(values=[30, 25, 20, 25], names=['재생에너지', '탄소감축', '거버넌스', '사회공헌'],
                    title="ESG 투자 포트폴리오")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def display_evaluation_results(evaluation: dict):
    """평가 결과 표시"""
    st.markdown("## ESG 평가 결과")
    
    # 메인 지표 표시
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "ESG 총점",
            f"{evaluation['scores']['total']:.1f}점",
            delta=None
        )
    
    with col2:
        grade = evaluation['grade']
        grade_color = engine.grade_system[grade]['color']
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 0.875rem; color: #666;">ESG 등급</div>
            <div style="font-size: 2rem; font-weight: 700; color: {grade_color}; margin-top: 0.5rem;">
                {grade}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        benefits = evaluation['financial_benefits']
        st.metric(
            "금리 우대",
            f"{benefits['discount_rate']}%p",
            delta=f"연 {benefits['annual_savings']:.0f}억원 절감"
        )
    
    with col4:
        compliance = evaluation['compliance']
        st.metric(
            "규제 준수도",
            f"{compliance['overall']:.0f}%"
        )
    
    with col5:
        if 'ai_predictions' in st.session_state:
            confidence = st.session_state.ai_predictions['confidence']['confidence_score']
            st.metric(
                "AI 신뢰도",
                f"{confidence:.0f}%",
                delta="예측 활성화"
            )
        else:
            st.metric("AI 상태", "비활성", delta=None)
    
    # 탭 구성
    if st.session_state.get('ai_enabled', False):
        tabs = st.tabs(["📊 상세 점수", "📈 AI 예측", "🎯 개선 전략", "💰 금융 혜택", "📋 개선 제안", "🔬 시나리오 분석"])
        
        with tabs[0]:
            display_detailed_scores(evaluation)
        
        with tabs[1]:
            display_ai_predictions()
        
        with tabs[2]:
            display_improvement_strategy()
        
        with tabs[3]:
            display_financial_benefits(evaluation)
        
        with tabs[4]:
            display_improvement_suggestions(evaluation)
        
        with tabs[5]:
            display_scenario_analysis(evaluation)
    else:
        tabs = st.tabs(["상세 점수", "영역별 분석", "금융 혜택", "개선 제안"])
        
        with tabs[0]:
            display_detailed_scores(evaluation)
        
        with tabs[1]:
            display_area_analysis(evaluation)
        
        with tabs[2]:
            display_financial_benefits(evaluation)
        
        with tabs[3]:
            display_improvement_suggestions(evaluation)

def display_ai_predictions():
    """AI 예측 결과 표시"""
    if 'ai_predictions' not in st.session_state:
        st.warning("AI 예측을 먼저 실행해주세요.")
        return
    
    predictions_data = st.session_state.ai_predictions
    historical = predictions_data['historical']
    predictions = predictions_data['predictions']
    confidence = predictions_data['confidence']
    
    st.markdown("### 📈 ESG 점수 예측")
    
    # 신뢰도 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("예측 신뢰도", f"{confidence['confidence_score']:.0f}%")
    with col2:
        st.metric("신뢰 수준", confidence['reliability'].upper())
    with col3:
        st.metric("예측 기간", st.session_state.prediction_period)
    
    # 시계열 차트
    fig = go.Figure()
    
    # 과거 데이터
    fig.add_trace(go.Scatter(
        x=historical['date'],
        y=historical['total'],
        mode='lines+markers',
        name='과거 실적',
        line=dict(color='blue', width=2),
        marker=dict(size=5)
    ))
    
    # 예측 데이터
    fig.add_trace(go.Scatter(
        x=predictions['date'],
        y=predictions['total'],
        mode='lines+markers',
        name='AI 예측',
        line=dict(color='red', width=2, dash='dash'),
        marker=dict(size=5)
    ))
    
    # 신뢰 구간
    confidence_interval = confidence['confidence_intervals']['total']
    fig.add_trace(go.Scatter(
        x=predictions['date'],
        y=[confidence_interval['upper']] * len(predictions),
        mode='lines',
        name='신뢰 상한',
        line=dict(color='rgba(255,0,0,0.2)', width=1),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=predictions['date'],
        y=[confidence_interval['lower']] * len(predictions),
        mode='lines',
        name='신뢰 하한',
        line=dict(color='rgba(255,0,0,0.2)', width=1),
        fill='tonexty',
        fillcolor='rgba(255,0,0,0.1)',
        showlegend=False
    ))
    
    fig.update_layout(
        title="ESG 총점 예측 (AI 기반)",
        xaxis_title="날짜",
        yaxis_title="ESG 점수",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 영역별 예측
    st.markdown("### 📊 영역별 예측")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_e = go.Figure()
        fig_e.add_trace(go.Scatter(x=historical['date'], y=historical['E'], name='과거', line=dict(color='green')))
        fig_e.add_trace(go.Scatter(x=predictions['date'], y=predictions['E'], name='예측', line=dict(color='lightgreen', dash='dash')))
        fig_e.update_layout(title="환경(E)", height=250, showlegend=False)
        st.plotly_chart(fig_e, use_container_width=True)
    
    with col2:
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(x=historical['date'], y=historical['S'], name='과거', line=dict(color='blue')))
        fig_s.add_trace(go.Scatter(x=predictions['date'], y=predictions['S'], name='예측', line=dict(color='lightblue', dash='dash')))
        fig_s.update_layout(title="사회(S)", height=250, showlegend=False)
        st.plotly_chart(fig_s, use_container_width=True)
    
    with col3:
        fig_g = go.Figure()
        fig_g.add_trace(go.Scatter(x=historical['date'], y=historical['G'], name='과거', line=dict(color='orange')))
        fig_g.add_trace(go.Scatter(x=predictions['date'], y=predictions['G'], name='예측', line=dict(color='lightsalmon', dash='dash')))
        fig_g.update_layout(title="거버넌스(G)", height=250, showlegend=False)
        st.plotly_chart(fig_g, use_container_width=True)
    
    # 예측 요약
    st.markdown("### 📋 예측 요약")
    
    final_prediction = predictions.iloc[-1]
    current_score = historical['total'].iloc[-1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **현재 상태**
        - 현재 점수: {current_score:.1f}점
        - 현재 등급: {engine._determine_grade(current_score)}
        """)
    
    with col2:
        predicted_grade = engine._determine_grade(final_prediction['total'])
        st.success(f"""
        **{st.session_state.prediction_period} 후 예측**
        - 예측 점수: {final_prediction['total']:.1f}점
        - 예측 등급: {predicted_grade}
        - 점수 변화: {final_prediction['total'] - current_score:+.1f}점
        """)

def display_improvement_strategy():
    """개선 전략 표시"""
    if 'ai_predictions' not in st.session_state:
        st.warning("AI 예측을 먼저 실행해주세요.")
        return
    
    improvement = st.session_state.ai_predictions['improvement_analysis']
    
    st.markdown("### 🎯 AI 추천 개선 전략")
    
    if improvement['status'] == 'already_achieved':
        st.success(improvement['message'])
    else:
        # 목표 및 현황
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("현재 점수", f"{improvement['current_score']:.1f}점")
        
        with col2:
            st.metric("목표 점수", f"{improvement['target_score']:.1f}점")
        
        with col3:
            st.metric("필요 개선", f"+{improvement['gap']:.1f}점")
        
        with col4:
            st.metric("예상 ROI", f"{improvement['roi']:.0f}%")
        
        # 추천 개선 사항
        st.markdown("### 📋 추천 개선 사항 (우선순위)")
        
        for idx, rec in enumerate(improvement['recommendations'], 1):
            priority_color = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }
            
            with st.expander(f"{priority_color[rec['priority']]} {idx}. {rec['factor'].replace('_', ' ').title()}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("예상 개선", f"+{rec['impact']:.1f}점")
                
                with col2:
                    st.metric("투자 비용", f"{rec['cost']}억원")
                
                with col3:
                    st.metric("소요 기간", f"{rec['time']}개월")
                
                st.markdown(f"**영역**: {rec['area'].capitalize()}")
                st.markdown(f"**우선순위**: {rec['priority'].upper()}")
        
        # 전체 요약
        st.markdown("### 💰 투자 요약")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("총 투자 비용", f"{improvement['total_cost']}억원")
        
        with col2:
            st.metric("예상 소요 기간", f"{improvement['estimated_time']}개월")
        
        with col3:
            st.metric("예상 점수 개선", f"+{improvement['expected_improvement']:.1f}점")

def display_scenario_analysis(evaluation: Dict):
    """시나리오 분석"""
    st.markdown("### 🔬 시나리오 분석")
    
    # 시나리오 정의
    scenarios = [
        {
            'name': '보수적 개선',
            'improvements': [
                {'area': 'E', 'impact': 5},
                {'area': 'S', 'impact': 3},
                {'area': 'G', 'impact': 2}
            ],
            'investment': 200
        },
        {
            'name': '중도적 개선',
            'improvements': [
                {'area': 'E', 'impact': 10},
                {'area': 'S', 'impact': 8},
                {'area': 'G', 'impact': 7}
            ],
            'investment': 500
        },
        {
            'name': '공격적 개선',
            'improvements': [
                {'area': 'E', 'impact': 20},
                {'area': 'S', 'impact': 15},
                {'area': 'G', 'impact': 15}
            ],
            'investment': 1000
        }
    ]
    
    # 시나리오 분석 실행
    current_scores = evaluation['scores']
    scenario_results = ai_predictor.generate_scenario_analysis(current_scores, scenarios)
    
    # 결과 표시
    st.dataframe(
        scenario_results.style.format({
            'new_score': '{:.1f}',
            'score_change': '+{:.1f}',
            'rate_discount': '{:.1f}%',
            'annual_savings': '{:.0f}억원',
            'investment': '{:.0f}억원',
            'roi': '{:.0f}%'
        }),
        use_container_width=True
    )
    
    # 시각화
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=scenario_results['scenario'],
        y=scenario_results['score_change'],
        name='점수 개선',
        marker_color='lightblue',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=scenario_results['scenario'],
        y=scenario_results['roi'],
        name='ROI (%)',
        marker_color='red',
        yaxis='y2',
        mode='lines+markers',
        line=dict(width=3)
    ))
    
    fig.update_layout(
        title="시나리오별 개선 효과 및 ROI",
        yaxis=dict(title="점수 개선", side='left'),
        yaxis2=dict(title="ROI (%)", overlaying='y', side='right'),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 최적 시나리오 추천
    best_scenario = scenario_results.loc[scenario_results['roi'].idxmax()]
    
    st.success(f"""
    ### 🏆 최적 시나리오: {best_scenario['scenario']}
    - 예상 점수: {best_scenario['new_score']:.1f}점 (+{best_scenario['score_change']:.1f})
    - 새로운 등급: {best_scenario['new_grade']}
    - 투자 금액: {best_scenario['investment']:.0f}억원
    - 5년 ROI: {best_scenario['roi']:.0f}%
    - 연간 금리 절감: {best_scenario['annual_savings']:.0f}억원
    """)

def display_detailed_scores(evaluation: dict):
    """상세 점수 표시"""
    scores = evaluation['scores']
    
    # ESG 점수 시각화
    fig = go.Figure()
    
    categories = ['환경(E)', '사회(S)', '거버넌스(G)']
    values = [scores['E'], scores['S'], scores['G']]
    colors = ['#00D67A', '#0046FF', '#FFB800']
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f"{v:.1f}" for v in values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="ESG 영역별 점수",
        yaxis_title="점수",
        yaxis_range=[0, 110],
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 규제 준수 현황
    st.markdown("### 규제 준수 현황")
    compliance = evaluation['compliance']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status = compliance['K-Taxonomy']['status']
        color = "#00D67A" if status == "준수" else "#FF4757"
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; border: 2px solid {color}; border-radius: 8px;">
            <div style="font-weight: 600;">K-Taxonomy</div>
            <div style="color: {color}; font-size: 1.2rem; margin-top: 0.5rem;">{status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status = compliance['TCFD']['status']
        color = "#00D67A" if status == "준수" else "#FF4757"
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; border: 2px solid {color}; border-radius: 8px;">
            <div style="font-weight: 600;">TCFD</div>
            <div style="color: {color}; font-size: 1.2rem; margin-top: 0.5rem;">{status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status = compliance['GRI']['status']
        color = "#00D67A" if status == "준수" else "#FF4757"
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; border: 2px solid {color}; border-radius: 8px;">
            <div style="font-weight: 600;">GRI</div>
            <div style="color: {color}; font-size: 1.2rem; margin-top: 0.5rem;">{status}</div>
        </div>
        """, unsafe_allow_html=True)

def display_area_analysis(evaluation: dict):
    """영역별 분석"""
    details = evaluation['details']
    
    # 환경(E) 분석
    st.markdown("### 🌱 환경(E) 상세 분석")
    e_details = details['E']
    
    col1, col2 = st.columns(2)
    with col1:
        for key, value in list(e_details.items())[:2]:
            if isinstance(value, dict) and 'score' in value:
                st.metric(
                    key.replace('_', ' ').title(),
                    f"{value['score']:.1f}점"
                )
    with col2:
        for key, value in list(e_details.items())[2:]:
            if isinstance(value, dict) and 'score' in value:
                st.metric(
                    key.replace('_', ' ').title(),
                    f"{value['score']:.1f}점"
                )
    
    # 사회(S) 분석
    st.markdown("### 👥 사회(S) 상세 분석")
    s_details = details['S']
    
    col1, col2 = st.columns(2)
    with col1:
        for key, value in list(s_details.items())[:2]:
            if isinstance(value, dict) and 'score' in value:
                st.metric(
                    key.replace('_', ' ').title(),
                    f"{value['score']:.1f}점"
                )
    with col2:
        for key, value in list(s_details.items())[2:]:
            if isinstance(value, dict) and 'score' in value:
                st.metric(
                    key.replace('_', ' ').title(),
                    f"{value['score']:.1f}점"
                )
    
    # 거버넌스(G) 분석
    st.markdown("### 🏛️ 거버넌스(G) 상세 분석")
    g_details = details['G']
    
    col1, col2 = st.columns(2)
    with col1:
        for key, value in list(g_details.items())[:2]:
            if isinstance(value, dict) and 'score' in value:
                st.metric(
                    key.replace('_', ' ').title(),
                    f"{value['score']:.1f}점"
                )
    with col2:
        for key, value in list(g_details.items())[2:]:
            if isinstance(value, dict) and 'score' in value:
                st.metric(
                    key.replace('_', ' ').title(),
                    f"{value['score']:.1f}점"
                )

def display_financial_benefits(evaluation: dict):
    """금융 혜택 표시"""
    benefits = evaluation['financial_benefits']
    
    st.markdown("### 💰 ESG 등급별 금융 혜택")
    
    # 현재 혜택
    st.info(f"""
    #### 현재 {benefits['grade']}등급 혜택
    - **기준 금리**: {benefits['base_rate']}%
    - **우대 할인**: -{benefits['discount_rate']}%p
    - **최종 금리**: **{benefits['final_rate']}%**
    - **대출 금액**: {benefits['loan_amount']:,}억원
    - **연간 절감액**: **{benefits['annual_savings']:.0f}억원**
    """)
    
    # 등급별 혜택 비교
    st.markdown("### 📊 등급별 금리 우대 비교")
    
    grades = []
    discounts = []
    colors = []
    
    for grade, info in engine.grade_system.items():
        grades.append(grade)
        discounts.append(info['rate_discount'])
        colors.append(info['color'])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grades,
        y=discounts,
        marker_color=colors,
        text=[f"{d}%p" for d in discounts],
        textposition='outside'
    ))
    
    # 현재 등급 표시
    current_idx = grades.index(benefits['grade'])
    fig.add_shape(
        type="rect",
        x0=current_idx-0.4, x1=current_idx+0.4,
        y0=0, y1=discounts[current_idx],
        line=dict(color="red", width=3)
    )
    
    fig.update_layout(
        title="ESG 등급별 금리 우대율",
        xaxis_title="ESG 등급",
        yaxis_title="금리 우대 (%p)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_improvement_suggestions(evaluation: dict):
    """개선 제안 표시"""
    st.markdown("### 📋 ESG 개선 제안")
    
    improvement_areas = evaluation.get('improvement_areas', [])
    
    if improvement_areas:
        for idx, area in enumerate(improvement_areas, 1):
            st.info(f"{idx}. {area}")
    
    # 등급 상승 시뮬레이션
    st.markdown("### 🎯 등급 상승 시뮬레이션")
    
    current_score = evaluation['scores']['total']
    current_grade = evaluation['grade']
    
    # 다음 등급까지 필요한 점수 계산
    next_grade_score = None
    next_grade = None
    
    grade_list = list(engine.grade_system.keys())
    current_idx = grade_list.index(current_grade)
    
    if current_idx > 0:
        next_grade = grade_list[current_idx - 1]
        next_grade_score = engine.grade_system[next_grade]['min']
        gap = next_grade_score - current_score
        
        st.markdown(f"""
        현재 **{current_grade}등급** ({current_score:.1f}점) → 
        목표 **{next_grade}등급** ({next_grade_score}점)
        
        **필요 점수: +{gap:.1f}점**
        """)
        
        # 개선 시나리오
        st.markdown("#### 개선 시나리오")
        scenarios = [
            {"name": "재생에너지 50% 전환", "impact": 10},
            {"name": "ESG 위원회 설립", "impact": 15},
            {"name": "공급망 ESG 평가 확대", "impact": 8},
            {"name": "다양성 정책 강화", "impact": 5}
        ]
        
        total_impact = 0
        for scenario in scenarios:
            checked = st.checkbox(scenario['name'], key=f"scenario_{scenario['name']}")
            if checked:
                total_impact += scenario['impact']
        
        if total_impact > 0:
            new_score = current_score + total_impact
            new_grade = engine._determine_grade(new_score)
            
            st.success(f"""
            **시뮬레이션 결과**
            - 예상 점수: {new_score:.1f}점 (+{total_impact}점)
            - 예상 등급: {new_grade}
            - 추가 금리 우대: {engine.grade_system[new_grade]['rate_discount'] - engine.grade_system[current_grade]['rate_discount']:.1f}%p
            """)
    else:
        st.success("축하합니다! 이미 최고 등급입니다.")

if __name__ == "__main__":
    main()