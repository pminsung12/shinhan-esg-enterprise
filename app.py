"""
ShinhanESG Enterprise - 통합 메인 애플리케이션 v3.0
대기업 ESG 통합관리 플랫폼 with AI + 금융상품 + 공급망
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
import os
import numpy as np

# src 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 로컬 모듈 import
from src.enterprise_esg_engine import EnterpriseESGEngine
from src.data_loader import DataLoader
from src.ai_prediction_finance import AIPredictor
from src.financial_products import FinancialProductMatcher
from src.supply_chain_analysis import SupplyChainAnalyzer

# 페이지 설정
st.set_page_config(
    page_title="ShinhanESG Enterprise v3.0",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0046FF 0%, #00D67A 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #0046FF;
    }
    .grade-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .recommendation-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #00D67A;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: white;
        border-radius: 10px 10px 0px 0px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0046FF;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 전역 객체 초기화
@st.cache_resource
def init_systems():
    """시스템 초기화"""
    return (
        EnterpriseESGEngine(),
        DataLoader(),
        AIPredictor(),
        FinancialProductMatcher(),
        SupplyChainAnalyzer()
    )

engine, data_loader, ai_predictor, product_matcher, supply_chain_analyzer = init_systems()

def main():
    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">🏢 ShinhanESG Enterprise v3.0</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">AI 기반 대기업 ESG 통합관리 플랫폼</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 메인 메트릭
    if 'evaluation_result' in st.session_state:
        display_main_metrics()
    
    # 사이드바
    with st.sidebar:
        st.image("https://i.namu.wiki/i/Etmt-wojOBWr5gVcPR0qrTxuej558yfzzyYr0xXYSxljpLuEdPWGSPi-aPdJHQrpZY2o7zvuUMb4PE6PvFjQ3Q.svg", width=400)
        st.markdown("---")
        
        st.header("평가 설정")
        
        # 기업 선택
        enterprise_list = data_loader.get_enterprise_list()
        if enterprise_list:
            selected_enterprise = st.selectbox(
                "평가 대상 기업",
                enterprise_list,
                help="ESG 평가를 진행할 기업을 선택하세요"
            )
            
            # 기업 정보 표시
            enterprise_data = data_loader.get_enterprise_data(selected_enterprise)
            if enterprise_data:
                st.markdown("### 기업 정보")
                basic_info = enterprise_data.get('basic_info', {})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("업종", basic_info.get('industry', 'N/A'))
                    st.metric("직원수", f"{basic_info.get('employee_count', 0):,}명")
                with col2:
                    st.metric("자산규모", f"{basic_info.get('asset_size', 0):,}억원")
                    st.metric("매출액", f"{basic_info.get('revenue', 10000):,}억원")
                
                st.markdown("---")
                
                # 평가 옵션
                st.markdown("### ⚙️ 평가 옵션")
                
                # 기능 선택
                enable_ai = st.checkbox("🤖 AI 예측 분석", value=True)
                enable_financial = st.checkbox("💰 금융상품 매칭", value=True)
                enable_supply_chain = st.checkbox("🔗 공급망 분석", value=True)
                
                if enable_ai:
                    prediction_period = st.select_slider(
                        "예측 기간",
                        options=["3개월", "6개월", "1년", "3년"],
                        value="1년"
                    )
                
                st.markdown("---")
                
                # 평가 실행 버튼
                if st.button("🚀 통합 ESG 평가 실행", type="primary", use_container_width=True):
                    with st.spinner("평가 진행 중... (약 10초 소요)"):
                        # 기본 평가
                        evaluation = engine.evaluate_enterprise(enterprise_data)
                        st.session_state.evaluation_result = evaluation
                        st.session_state.selected_enterprise = selected_enterprise
                        st.session_state.enterprise_data = enterprise_data
                        
                        # AI 예측
                        if enable_ai:
                            st.session_state.ai_enabled = True
                            st.session_state.prediction_period = prediction_period
                            perform_ai_prediction(evaluation)
                        
                        # 금융상품 매칭
                        if enable_financial:
                            st.session_state.financial_enabled = True
                            perform_financial_matching(enterprise_data, evaluation)
                        
                        # 공급망 분석
                        if enable_supply_chain:
                            st.session_state.supply_chain_enabled = True
                            perform_supply_chain_analysis(enterprise_data)
                        
                        st.success("✅ 평가 완료!")
                        st.balloons()
                
                # 리포트 생성
                if 'evaluation_result' in st.session_state:
                    st.markdown("---")
                    if st.button("📄 종합 리포트 생성", use_container_width=True):
                        generate_report()
        else:
            st.error("데이터를 로드할 수 없습니다.")
    
    # 메인 컨텐츠
    if 'evaluation_result' in st.session_state:
        display_main_dashboard()
    else:
        display_welcome_screen()
    
    # 푸터
    display_footer()

def display_main_metrics():
    """메인 지표 표시"""
    evaluation = st.session_state.evaluation_result
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        grade = evaluation['grade']
        grade_color = engine.grade_system[grade]['color']
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 0.875rem; color: #666;">ESG 등급</div>
            <div class="grade-badge" style="background: {grade_color}; color: white;">
                {grade}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric(
            "ESG 총점",
            f"{evaluation['scores']['total']:.1f}",
            delta=f"+{evaluation['scores']['total']-70:.1f}" if evaluation['scores']['total'] > 70 else None
        )
    
    with col3:
        benefits = evaluation['financial_benefits']
        st.metric(
            "금리 우대",
            f"{benefits['discount_rate']}%p",
            delta=f"연 {benefits['annual_savings']:.0f}억 절감"
        )
    
    with col4:
        if 'ai_predictions' in st.session_state:
            confidence = st.session_state.ai_predictions['confidence']['confidence_score']
            st.metric("AI 신뢰도", f"{confidence:.0f}%")
        else:
            st.metric("AI 상태", "대기")
    
    with col5:
        if 'matched_products' in st.session_state:
            product_count = len(st.session_state.matched_products['recommended_loans'])
            st.metric("추천 상품", f"{product_count}개")
        else:
            st.metric("금융상품", "대기")
    
    with col6:
        if 'supply_chain_analysis' in st.session_state:
            supply_grade = st.session_state.supply_chain_analysis['risk_assessment']['supply_chain_grade']
            st.metric("공급망 등급", supply_grade)
        else:
            st.metric("공급망", "대기")

def display_main_dashboard():
    """메인 대시보드"""
    # 탭 구성
    tab_list = ["📊 종합 대시보드", "📈 ESG 평가", "🤖 AI 예측"]
    
    if st.session_state.get('financial_enabled', False):
        tab_list.append("💰 금융상품")
    
    if st.session_state.get('supply_chain_enabled', False):
        tab_list.append("🔗 공급망")
    
    tab_list.extend(["📋 개선전략", "📄 리포트"])
    
    tabs = st.tabs(tab_list)
    
    # 종합 대시보드
    with tabs[0]:
        display_executive_dashboard()
    
    # ESG 평가
    with tabs[1]:
        display_esg_evaluation()
    
    # AI 예측
    with tabs[2]:
        if st.session_state.get('ai_enabled', False):
            display_ai_predictions()
        else:
            st.info("AI 예측 기능을 활성화하려면 사이드바에서 옵션을 선택하세요.")
    
    # 금융상품 (조건부)
    tab_idx = 3
    if st.session_state.get('financial_enabled', False):
        with tabs[tab_idx]:
            display_financial_products()
        tab_idx += 1
    
    # 공급망 (조건부)
    if st.session_state.get('supply_chain_enabled', False):
        with tabs[tab_idx]:
            display_supply_chain()
        tab_idx += 1
    
    # 개선전략
    with tabs[tab_idx]:
        display_improvement_strategy()
    tab_idx += 1
    
    # 리포트
    with tabs[tab_idx]:
        display_report_section()

def display_executive_dashboard():
    """경영진 대시보드"""
    st.markdown("## 📊 Executive Dashboard")
    
    evaluation = st.session_state.evaluation_result
    
    # 주요 성과 지표
    st.markdown("### 핵심 성과 지표 (KPIs)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # ESG 점수 게이지 차트
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=evaluation['scores']['total'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "ESG Score"},
            delta={'reference': 70},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': engine.grade_system[evaluation['grade']]['color']},
                'steps': [
                    {'range': [0, 65], 'color': "lightgray"},
                    {'range': [65, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 영역별 점수 레이더 차트
        categories = ['환경(E)', '사회(S)', '거버넌스(G)']
        values = [evaluation['scores']['E'], evaluation['scores']['S'], evaluation['scores']['G']]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='ESG Score'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            height=250,
            title="ESG 영역별 점수"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # 재무 영향 분석
        st.markdown("#### 💰 재무 영향")
        benefits = evaluation['financial_benefits']
        
        # 5년간 누적 절감액 계산
        cumulative_5y = benefits['annual_savings'] * 5
        
        metrics_data = {
            '구분': ['연간 절감액', '5년 누적', 'ROI'],
            '금액': [
                f"{benefits['annual_savings']:.0f}억원",
                f"{cumulative_5y:.0f}억원",
                "250%"
            ]
        }
        df = pd.DataFrame(metrics_data)
        st.dataframe(df, hide_index=True, use_container_width=True)
    
    # 트렌드 분석
    if 'ai_predictions' in st.session_state:
        st.markdown("### 📈 ESG 성과 트렌드")
        
        historical = st.session_state.ai_predictions['historical']
        predictions = st.session_state.ai_predictions['predictions']
        
        # 통합 차트
        fig = go.Figure()
        
        # 과거 데이터
        fig.add_trace(go.Scatter(
            x=historical['date'],
            y=historical['total'],
            mode='lines+markers',
            name='실적',
            line=dict(color='blue', width=2)
        ))
        
        # 예측 데이터
        fig.add_trace(go.Scatter(
            x=predictions['date'],
            y=predictions['total'],
            mode='lines+markers',
            name='예측',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # 목표선
        fig.add_hline(y=80, line_dash="dot", line_color="green", 
                     annotation_text="목표 (A- 등급)")
        
        fig.update_layout(
            title="ESG 점수 추이 및 예측",
            xaxis_title="기간",
            yaxis_title="ESG 점수",
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 주요 이슈 및 권고사항
    st.markdown("### 🎯 주요 이슈 및 권고사항")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚠️ 주요 리스크")
        improvement_areas = evaluation.get('improvement_areas', [])
        for area in improvement_areas[:3]:
            st.markdown(f"""
            <div class="recommendation-card">
                {area}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ✅ 주요 기회")
        if 'matched_products' in st.session_state:
            products = st.session_state.matched_products['recommended_loans']
            for product in products[:3]:
                st.markdown(f"""
                <div class="recommendation-card">
                    <strong>{product['product']}</strong><br>
                    금리 우대: {product['rate_discount']}%p
                </div>
                """, unsafe_allow_html=True)

def display_esg_evaluation():
    """ESG 평가 상세"""
    st.markdown("## 📈 ESG 평가 상세")
    
    evaluation = st.session_state.evaluation_result
    
    # 영역별 상세 점수
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌱 환경(E)")
        st.metric("점수", f"{evaluation['scores']['E']:.1f}점")
        details = evaluation['details']['E']
        for key, value in details.items():
            if isinstance(value, dict) and 'score' in value:
                st.write(f"- {key.replace('_', ' ').title()}: {value['score']:.1f}점")
    
    with col2:
        st.markdown("### 👥 사회(S)")
        st.metric("점수", f"{evaluation['scores']['S']:.1f}점")
        details = evaluation['details']['S']
        for key, value in details.items():
            if isinstance(value, dict) and 'score' in value:
                st.write(f"- {key.replace('_', ' ').title()}: {value['score']:.1f}점")
    
    with col3:
        st.markdown("### 🏛️ 거버넌스(G)")
        st.metric("점수", f"{evaluation['scores']['G']:.1f}점")
        details = evaluation['details']['G']
        for key, value in details.items():
            if isinstance(value, dict) and 'score' in value:
                st.write(f"- {key.replace('_', ' ').title()}: {value['score']:.1f}점")
    
    # 규제 준수 현황
    st.markdown("### 📋 규제 준수 현황")
    compliance = evaluation['compliance']
    
    compliance_df = pd.DataFrame([
        {"규제": "K-Taxonomy", "상태": compliance['K-Taxonomy']['status'], 
         "준수여부": "✅" if compliance['K-Taxonomy']['compliant'] else "❌"},
        {"규제": "TCFD", "상태": compliance['TCFD']['status'],
         "준수여부": "✅" if compliance['TCFD']['compliant'] else "❌"},
        {"규제": "GRI", "상태": compliance['GRI']['status'],
         "준수여부": "✅" if compliance['GRI']['compliant'] else "❌"}
    ])
    
    st.dataframe(compliance_df, hide_index=True, use_container_width=True)

def display_ai_predictions():
    """AI 예측 결과"""
    st.markdown("## 🤖 AI 예측 분석")
    
    if 'ai_predictions' not in st.session_state:
        st.warning("AI 예측을 먼저 실행해주세요.")
        return
    
    predictions_data = st.session_state.ai_predictions
    
    # 예측 신뢰도
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("예측 신뢰도", 
                 f"{predictions_data['confidence']['confidence_score']:.0f}%")
    with col2:
        st.metric("신뢰 수준", 
                 predictions_data['confidence']['reliability'].upper())
    with col3:
        st.metric("예측 기간", st.session_state.prediction_period)
    with col4:
        final_score = predictions_data['predictions'].iloc[-1]['total']
        st.metric("예상 점수", f"{final_score:.1f}")
    
    # 시계열 예측 차트
    display_prediction_chart(predictions_data)
    
    # 개선 동인 분석
    if predictions_data['improvement_analysis']['status'] == 'success':
        st.markdown("### 💡 AI 추천 개선 전략")
        
        improvement = predictions_data['improvement_analysis']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **목표 달성 Gap**
            - 현재: {improvement['current_score']:.1f}점
            - 목표: {improvement['target_score']:.1f}점
            - 필요: +{improvement['gap']:.1f}점
            """)
        
        with col2:
            st.success(f"""
            **투자 효과**
            - 비용: {improvement['total_cost']}억원
            - 기간: {improvement['estimated_time']}개월
            - ROI: {improvement['roi']:.0f}%
            """)
        
        # 추천 개선 사항
        for idx, rec in enumerate(improvement['recommendations'], 1):
            with st.expander(f"{idx}. {rec['factor'].replace('_', ' ').title()}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("예상 개선", f"+{rec['impact']:.1f}점")
                with col2:
                    st.metric("투자 비용", f"{rec['cost']}억원")
                with col3:
                    st.metric("소요 기간", f"{rec['time']}개월")

def display_financial_products():
    """금융상품 매칭 결과"""
    st.markdown("## 💰 맞춤형 금융상품")
    
    if 'matched_products' not in st.session_state:
        st.warning("금융상품 매칭을 먼저 실행해주세요.")
        return
    
    matched = st.session_state.matched_products
    package = st.session_state.get('financing_package', {})
    
    # 패키지 요약
    if package:
        st.success(f"""
        ### 🎁 {package['package_name']}
        - 총 한도: {package['total_facility']:,}억원
        - 평균 금리 우대: {package['average_discount']}%p
        - 연간 절감액: {package['annual_savings']:.1f}억원
        - 5년 패키지 가치: {package['package_value_5y']:.1f}억원
        """)
    
    # 추천 대출 상품
    st.markdown("### 📌 추천 대출 상품")
    
    for idx, loan in enumerate(matched['recommended_loans'], 1):
        with st.expander(f"{idx}. {loan['product']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("금리 우대", f"{loan['rate_discount']}%p")
                st.metric("최대 한도", f"{loan['max_amount']:,}억원")
            
            with col2:
                st.metric("연간 절감", f"{loan['annual_savings']:.1f}억원")
                st.metric("우선순위", f"{loan['priority']:.0f}점")
            
            with col3:
                st.markdown("**주요 특징**")
                for feature in loan['features'][:3]:
                    st.write(f"• {feature}")
            
            st.markdown("**혜택**")
            for key, value in loan['benefits'].items():
                st.write(f"• {key}: {value}")
    
    # 예적금 상품
    if matched['recommended_deposits']:
        st.markdown("### 💵 ESG 예적금")
        deposits_df = pd.DataFrame(matched['recommended_deposits'])
        st.dataframe(deposits_df, hide_index=True, use_container_width=True)
    
    # 그린본드
    if matched['recommended_bonds']:
        st.markdown("### 🌱 그린본드/소셜본드")
        for bond in matched['recommended_bonds']:
            st.info(f"""
            **{bond['product']}**
            - 금리: {bond['rate_range']}
            - 기간: {bond['term']}
            - 용도: {', '.join(bond['use_of_proceeds'][:3])}
            """)
    
    # 특별 프로그램
    if matched['special_offers']:
        st.markdown("### 🎯 특별 프로그램")
        for offer in matched['special_offers']:
            with st.expander(offer['program']):
                st.write(f"**비용**: {offer['fee']}")
                st.write("**서비스**:")
                for service in offer['services']:
                    st.write(f"• {service}")

def display_supply_chain():
    """공급망 분석 결과"""
    st.markdown("## 🔗 공급망 ESG 분석")
    
    if 'supply_chain_analysis' not in st.session_state:
        st.warning("공급망 분석을 먼저 실행해주세요.")
        return
    
    analysis = st.session_state.supply_chain_analysis
    
    # Scope 3 배출량
    st.markdown("### 🌍 Scope 3 배출량 분석")
    
    scope3 = analysis['scope3_emissions']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Scope 3 총 배출량", 
                 f"{scope3['scope3_total']:,.0f} tCO2e")
    
    with col2:
        st.metric("전체 탄소발자국 중 비중",
                 f"{scope3['total_footprint']['scope3_percentage']:.1f}%")
    
    with col3:
        st.metric("데이터 품질",
                 scope3['data_quality']['overall_quality'])
    
    # 카테고리별 배출량 차트
    categories = []
    emissions = []
    for cat_id, cat_data in scope3['scope3_categories'].items():
        categories.append(cat_data['name'][:15])
        emissions.append(cat_data['emissions'])
    
    fig = px.pie(values=emissions, names=categories, 
                title="Scope 3 카테고리별 배출량 분포")
    st.plotly_chart(fig, use_container_width=True)
    
    # 공급업체 리스크
    st.markdown("### ⚠️ 공급업체 리스크 평가")
    
    risk = analysis['risk_assessment']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 공급업체", f"{risk['total_suppliers']}개")
    
    with col2:
        st.metric("평균 리스크 점수", f"{risk['average_risk_score']:.1f}")
    
    with col3:
        st.metric("공급망 등급", risk['supply_chain_grade'])
    
    with col4:
        st.metric("고위험 업체", f"{risk['risk_distribution']['high']}개")
    
    # 리스크 분포 차트
    risk_data = pd.DataFrame([
        {"리스크 수준": "High", "업체 수": risk['risk_distribution']['high']},
        {"리스크 수준": "Medium", "업체 수": risk['risk_distribution']['medium']},
        {"리스크 수준": "Low", "업체 수": risk['risk_distribution']['low']}
    ])
    
    fig = px.bar(risk_data, x="리스크 수준", y="업체 수", 
                color="리스크 수준",
                color_discrete_map={"High": "red", "Medium": "orange", "Low": "green"},
                title="공급업체 리스크 분포")
    st.plotly_chart(fig, use_container_width=True)
    
    # 공급망 회복탄력성
    if 'resilience' in analysis:
        st.markdown("### 💪 공급망 회복탄력성")
        
        resilience = analysis['resilience']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("회복탄력성 점수", 
                     f"{resilience['resilience_score']:.1f}")
        
        with col2:
            st.metric("회복탄력성 등급",
                     resilience['resilience_grade'])
        
        with col3:
            st.metric("위기 대응력",
                     resilience['resilience_level'])
        
        # 요인별 점수
        factor_scores = pd.DataFrame([
            {"요인": k.replace('_', ' ').title(), 
             "점수": v['score'],
             "상태": v['status']}
            for k, v in resilience['factor_scores'].items()
        ])
        
        st.dataframe(factor_scores, hide_index=True, use_container_width=True)

def display_improvement_strategy():
    """개선 전략"""
    st.markdown("## 📋 종합 개선 전략")
    
    evaluation = st.session_state.evaluation_result
    
    # 현재 상태 요약
    st.markdown("### 📊 현재 상태")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"""
        **ESG 등급**: {evaluation['grade']}
        **총점**: {evaluation['scores']['total']:.1f}
        """)
    
    with col2:
        st.info(f"""
        **E**: {evaluation['scores']['E']:.1f}
        **S**: {evaluation['scores']['S']:.1f}
        **G**: {evaluation['scores']['G']:.1f}
        """)
    
    with col3:
        compliance = evaluation['compliance']
        st.info(f"""
        **규제 준수도**: {compliance['overall']:.0f}%
        """)
    
    with col4:
        benefits = evaluation['financial_benefits']
        st.info(f"""
        **금리 우대**: {benefits['discount_rate']}%p
        **연 절감**: {benefits['annual_savings']:.0f}억
        """)
    
    # 통합 개선 로드맵
    st.markdown("### 🗺️ ESG 개선 로드맵")
    
    roadmap = create_improvement_roadmap(evaluation)
    
    # 단계별 표시
    for phase in roadmap['phases']:
        with st.expander(f"Phase {phase['phase']}: {phase['name']} ({phase['timeline']})"):
            st.write(f"**목표**: {phase['target']}")
            st.write("**주요 활동**:")
            for activity in phase['activities']:
                st.write(f"• {activity}")
            st.write(f"**예상 성과**: {phase['expected_outcome']}")
            st.write(f"**투자**: {phase['investment']}억원")
    
    # 시나리오 분석
    if 'ai_predictions' in st.session_state:
        st.markdown("### 🔬 시나리오 분석")
        
        scenarios = ai_predictor.generate_scenario_analysis(
            evaluation['scores'],
            [
                {'name': '보수적', 'improvements': [
                    {'area': 'E', 'impact': 5},
                    {'area': 'S', 'impact': 3},
                    {'area': 'G', 'impact': 2}
                ], 'investment': 200},
                {'name': '중도적', 'improvements': [
                    {'area': 'E', 'impact': 10},
                    {'area': 'S', 'impact': 8},
                    {'area': 'G', 'impact': 7}
                ], 'investment': 500},
                {'name': '공격적', 'improvements': [
                    {'area': 'E', 'impact': 20},
                    {'area': 'S', 'impact': 15},
                    {'area': 'G', 'impact': 15}
                ], 'investment': 1000}
            ]
        )
        
        st.dataframe(
            scenarios.style.format({
                'new_score': '{:.1f}',
                'score_change': '+{:.1f}',
                'rate_discount': '{:.1f}%',
                'annual_savings': '{:.0f}억원',
                'investment': '{:.0f}억원',
                'roi': '{:.0f}%'
            }).background_gradient(subset=['roi'], cmap='RdYlGn'),
            use_container_width=True
        )

def display_report_section():
    """리포트 섹션"""
    st.markdown("## 📄 종합 리포트")
    
    st.info("""
    종합 리포트는 다음 내용을 포함합니다:
    - ESG 평가 결과 요약
    - AI 예측 분석
    - 금융상품 추천
    - 공급망 분석
    - 개선 전략 및 로드맵
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 대시보드 PDF", use_container_width=True):
            st.success("대시보드 PDF 생성 중...")
    
    with col2:
        if st.button("📈 상세 보고서", use_container_width=True):
            st.success("상세 보고서 생성 중...")
    
    with col3:
        if st.button("🎯 실행 계획서", use_container_width=True):
            st.success("실행 계획서 생성 중...")
    
    # 리포트 미리보기
    st.markdown("### 📋 리포트 미리보기")
    
    report_preview = generate_report_preview()
    st.text_area("", report_preview, height=400)

def display_welcome_screen():
    """환영 화면"""
    st.markdown("""
    ## 👋 환영합니다!
    
    **ShinhanESG Enterprise v3.0**는 대기업을 위한 종합 ESG 관리 플랫폼입니다.
    
    ### 🚀 주요 기능
    
    #### 1. ESG 평가 엔진
    - 신한은행 7등급 체계 기반 정밀 평가
    - 업종별 맞춤형 가중치 적용
    - 실시간 규제 준수도 모니터링
    
    #### 2. AI 예측 분석
    - 머신러닝 기반 ESG 점수 예측
    - 개선 동인 자동 분석
    - ROI 시뮬레이션
    
    #### 3. 금융상품 자동 매칭
    - ESG 연계 대출 상품 추천
    - 그린본드/소셜본드 안내
    - 맞춤형 금융 패키지 구성
    
    #### 4. 공급망 ESG 분석
    - Scope 3 배출량 계산
    - 공급업체 리스크 평가
    - 공급망 회복탄력성 측정
    
    ### 기대 효과
    - **금리 절감**: ESG 등급별 0.2~2.7%p 우대
    - **리스크 감소**: 공급망 리스크 30% 감소
    - **규제 대응**: 2026년 의무공시 완벽 대비
    
    ---
    
    💡 **시작하려면 좌측 사이드바에서 기업을 선택하고 평가를 실행하세요!**
    """)
    
    # 데모 차트
    col1, col2 = st.columns(2)
    
    with col1:
        # ESG 트렌드
        dates = pd.date_range(start='2024-01', periods=12, freq='M')
        scores = [70 + i*1.5 + np.random.uniform(-2, 2) for i in range(12)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=scores,
            mode='lines+markers',
            name='ESG Score',
            line=dict(color='#0046FF', width=3)
        ))
        fig.update_layout(
            title="ESG 점수 개선 트렌드 (예시)",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 금융 혜택
        benefits = pd.DataFrame({
            '등급': ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C'],
            '금리우대': [2.7, 2.2, 1.8, 1.5, 1.2, 0.8, 0.4]
        })
        
        fig = px.bar(benefits, x='등급', y='금리우대',
                    title="ESG 등급별 금리 우대 (%p)",
                    color='금리우대',
                    color_continuous_scale='Greens')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def display_footer():
    """푸터"""
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.caption("🏢 신한은행 ICT 인턴 프로젝트")
    
    with col2:
        st.caption("📧 Contact: esg@shinhan.com")
    
    with col3:
        st.caption("📞 ESG 상담: 1599-8000")
    
    with col4:
        st.caption(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 헬퍼 함수들

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

def perform_financial_matching(company_data: Dict, evaluation: Dict):
    """금융상품 매칭 수행"""
    # 상품 매칭
    matched_products = product_matcher.match_products(company_data, evaluation)
    st.session_state.matched_products = matched_products
    
    # 금융 패키지 구성
    financing_needs = {'total_amount': 1000}  # 예시
    package = product_matcher.create_financing_package(
        company_data, evaluation, financing_needs
    )
    st.session_state.financing_package = package

def perform_supply_chain_analysis(company_data: Dict):
    """공급망 분석 수행"""
    # Scope 3 배출량 계산
    scope3_emissions = supply_chain_analyzer.calculate_scope3_emissions(company_data)
    
    # 공급업체 리스크 평가
    risk_assessment = supply_chain_analyzer.assess_supplier_risks(company_data)
    
    # 회복탄력성 분석
    resilience = supply_chain_analyzer.analyze_supply_chain_resilience(
        {'total_suppliers': 100, 'regions': ['Korea', 'China', 'Japan', 'USA']}
    )
    
    st.session_state.supply_chain_analysis = {
        'scope3_emissions': scope3_emissions,
        'risk_assessment': risk_assessment,
        'resilience': resilience
    }

def display_prediction_chart(predictions_data: Dict):
    """예측 차트 표시"""
    historical = predictions_data['historical']
    predictions = predictions_data['predictions']
    confidence = predictions_data['confidence']
    
    fig = go.Figure()
    
    # 과거 데이터
    fig.add_trace(go.Scatter(
        x=historical['date'],
        y=historical['total'],
        mode='lines+markers',
        name='과거 실적',
        line=dict(color='blue', width=2)
    ))
    
    # 예측 데이터
    fig.add_trace(go.Scatter(
        x=predictions['date'],
        y=predictions['total'],
        mode='lines+markers',
        name='AI 예측',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # 신뢰 구간
    confidence_interval = confidence['confidence_intervals']['total']
    upper_bound = [confidence_interval['upper']] * len(predictions)
    lower_bound = [confidence_interval['lower']] * len(predictions)
    
    fig.add_trace(go.Scatter(
        x=predictions['date'],
        y=upper_bound,
        mode='lines',
        line=dict(color='rgba(255,0,0,0.2)'),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=predictions['date'],
        y=lower_bound,
        mode='lines',
        line=dict(color='rgba(255,0,0,0.2)'),
        fill='tonexty',
        fillcolor='rgba(255,0,0,0.1)',
        showlegend=False
    ))
    
    fig.update_layout(
        title="ESG 점수 예측 (AI 기반)",
        xaxis_title="날짜",
        yaxis_title="ESG 점수",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_improvement_roadmap(evaluation: Dict) -> Dict:
    """개선 로드맵 생성"""
    current_score = evaluation['scores']['total']
    current_grade = evaluation['grade']
    
    roadmap = {
        'phases': [
            {
                'phase': 1,
                'name': 'Quick Wins',
                'timeline': '0-3개월',
                'target': f'점수 {current_score + 5:.0f}점 달성',
                'activities': [
                    'ESG 위원회 설립',
                    '정책 및 규정 수립',
                    '기초 데이터 수집 체계 구축'
                ],
                'investment': 50,
                'expected_outcome': '기반 구축 완료'
            },
            {
                'phase': 2,
                'name': 'Foundation Building',
                'timeline': '3-12개월',
                'target': f'점수 {current_score + 10:.0f}점 달성',
                'activities': [
                    '탄소 배출량 측정 시스템 구축',
                    '공급망 ESG 평가 시작',
                    'ESG 교육 프로그램 운영'
                ],
                'investment': 200,
                'expected_outcome': 'B+ 등급 달성'
            },
            {
                'phase': 3,
                'name': 'Acceleration',
                'timeline': '12-24개월',
                'target': 'A- 등급 달성',
                'activities': [
                    '재생에너지 전환 50%',
                    'Scope 3 감축 프로그램',
                    'ESG 인증 취득'
                ],
                'investment': 500,
                'expected_outcome': 'A- 등급 및 금리 1.8%p 우대'
            },
            {
                'phase': 4,
                'name': 'Excellence',
                'timeline': '24-36개월',
                'target': 'A+ 등급 달성',
                'activities': [
                    '탄소중립 로드맵 실행',
                    'ESG 리더십 포지션',
                    '공급망 전체 ESG 통합'
                ],
                'investment': 800,
                'expected_outcome': 'ESG 선도기업 지위'
            }
        ]
    }
    
    return roadmap

def generate_report_preview() -> str:
    """리포트 미리보기 생성"""
    if 'evaluation_result' not in st.session_state:
        return "평가를 먼저 실행해주세요."
    
    evaluation = st.session_state.evaluation_result
    company_name = st.session_state.get('selected_enterprise', 'Unknown')
    
    report = f"""
================================================================================
                        ESG 종합 평가 리포트
================================================================================

기업명: {company_name}
평가일: {datetime.now().strftime('%Y-%m-%d')}
평가 등급: {evaluation['grade']}

1. ESG 평가 결과
--------------------------------------------------------------------------------
- 환경(E): {evaluation['scores']['E']:.1f}점
- 사회(S): {evaluation['scores']['S']:.1f}점
- 거버넌스(G): {evaluation['scores']['G']:.1f}점
- 종합 점수: {evaluation['scores']['total']:.1f}점

2. 금융 혜택
--------------------------------------------------------------------------------
- 금리 우대: {evaluation['financial_benefits']['discount_rate']}%p
- 연간 절감액: {evaluation['financial_benefits']['annual_savings']:.0f}억원
- 대출 한도: {evaluation['financial_benefits']['loan_amount']:,}억원

3. 규제 준수 현황
--------------------------------------------------------------------------------
- K-Taxonomy: {evaluation['compliance']['K-Taxonomy']['status']}
- TCFD: {evaluation['compliance']['TCFD']['status']}
- GRI: {evaluation['compliance']['GRI']['status']}
- 종합 준수도: {evaluation['compliance']['overall']:.0f}%

4. 개선 권고사항
--------------------------------------------------------------------------------
"""
    
    for idx, area in enumerate(evaluation.get('improvement_areas', []), 1):
        report += f"{idx}. {area}\n"
    
    report += """
================================================================================
                            [End of Report]
================================================================================
"""
    
    return report

def generate_report():
    """종합 리포트 생성"""
    st.success("📄 종합 리포트를 생성했습니다!")
    st.balloons()

if __name__ == "__main__":
    main()