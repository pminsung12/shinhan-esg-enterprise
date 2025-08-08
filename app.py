"""
ShinhanESG Enterprise - 메인 애플리케이션
대기업 ESG 통합관리 플랫폼
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# src 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 로컬 모듈 import
from src.enterprise_esg_engine import EnterpriseESGEngine
from src.data_loader import DataLoader

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
    return EnterpriseESGEngine(), DataLoader()

engine, data_loader = init_systems()

def main():
    # 헤더
    st.title("ShinhanESG Enterprise")
    st.subheader("대기업 ESG 통합관리 플랫폼")
    
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
                
                # 평가 실행 버튼
                if st.button("🚀 ESG 평가 실행", type="primary", use_container_width=True):
                    st.session_state.evaluation_result = engine.evaluate_enterprise(enterprise_data)
                    st.session_state.selected_enterprise = selected_enterprise
        else:
            st.error("데이터를 로드할 수 없습니다.")
    
    # 메인 컨텐츠
    if 'evaluation_result' in st.session_state:
        display_evaluation_results(st.session_state.evaluation_result)
    else:
        display_welcome_screen()
    
    # 푸터
    st.markdown("---")
    st.caption("신한은행 ICT 인턴 프로젝트 | ShinhanESG Enterprise v1.0")

def display_welcome_screen():
    """환영 화면"""
    st.markdown("""
    ### 환영합니다!
    
    **ShinhanESG Enterprise**는 대기업의 ESG 성과를 종합적으로 평가하고 
    맞춤형 금융 솔루션을 제공하는 통합 플랫폼입니다.
    
    #### 주요 기능
    - **신한은행 7등급 체계** 기반 정밀 평가
    - **업종별 맞춤형** 가중치 적용
    - **AI 기반** 미래 성과 예측
    - **금융상품 자동 매칭** 및 혜택 계산
    
    #### 시작하기
    1. 좌측 사이드바에서 평가 대상 기업 선택
    2. "ESG 평가 실행" 버튼 클릭
    3. 상세 평가 결과 확인
    
    ---
    
    💡 **Tip**: 2026년부터 시행되는 ESG 공시 의무화에 대비하여 
    지금부터 체계적인 ESG 관리를 시작하세요!
    """)

def display_evaluation_results(evaluation: dict):
    """평가 결과 표시"""
    st.markdown("## ESG 평가 결과")
    
    # 메인 지표 표시
    col1, col2, col3, col4 = st.columns(4)
    
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
    
    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["상세 점수", "영역별 분석", "금융 혜택", "개선 제안"])
    
    with tab1:
        display_detailed_scores(evaluation)
    
    with tab2:
        display_area_analysis(evaluation)
    
    with tab3:
        display_financial_benefits(evaluation)
    
    with tab4:
        display_improvement_suggestions(evaluation)

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

def show_environment_check():
    """환경 설정 확인 (기존 함수 유지)"""
    st.header("✅ 환경 설정 확인")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("패키지 버전")
        
        packages = {
            "Streamlit": st.__version__,
            "Pandas": pd.__version__,
            "Python": f"{datetime.now().year}.x"
        }
        
        for name, version in packages.items():
            st.metric(name, version)
    
    with col2:
        st.subheader("시스템 상태")
        st.success("✅ 모든 패키지가 정상적으로 로드되었습니다.")
        st.info(f"현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()