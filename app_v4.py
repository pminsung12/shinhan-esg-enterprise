"""
ShinhanESG Enterprise - 최종 통합 애플리케이션 v4.0
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
import numpy as np
import time

# src 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 로컬 모듈 import
from src.enterprise_esg_engine import EnterpriseESGEngine
from src.data_loader import DataLoader
from src.ai_prediction_finance import AIPredictor
from src.financial_products import FinancialProductMatcher
from src.supply_chain_analysis import SupplyChainAnalyzer
from src.presentation_report import PresentationMode, ReportGenerator

# 페이지 설정
st.set_page_config(
    page_title="ShinhanESG Enterprise",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 개선된 CSS 스타일
st.markdown("""
<style>
    /* 폰트 설정 - 시스템 폰트 사용 */
    * {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 메인 컨테이너 */
    .main > div {
        padding-top: 0rem;
    }
    
    /* 헤더 디자인 */
    .hero-header {
        background: linear-gradient(135deg, #0046FF 0%, #0072CE 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 70, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 40%;
        height: 200%;
        background: rgba(255, 255, 255, 0.05);
        transform: rotate(35deg);
    }
    
    .hero-title {
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        color: white;
    }
    
    .hero-subtitle {
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-weight: 300;
        color: white;
    }
    
    /* 액션 버튼 그룹 */
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .action-btn {
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.1);
        color: white;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        cursor: pointer;
        font-size: 0.95rem;
    }
    
    .action-btn:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .action-btn-primary {
        background: white;
        color: #0046FF;
        border-color: white;
    }
    
    .action-btn-primary:hover {
        background: rgba(255, 255, 255, 0.95);
    }
    
    /* 메트릭 카드 */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #f0f0f0;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a1a;
        line-height: 1;
    }
    
    .metric-delta {
        font-size: 0.8rem;
        color: #00C896;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* 등급 배지 */
    .grade-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        border-radius: 16px;
        font-weight: 700;
        font-size: 1.8rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        color: white;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 8px;
        border-radius: 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        padding: 0 24px;
        background-color: transparent;
        border-radius: 12px;
        color: #666;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 70, 255, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0046FF, #0072CE);
        color: white;
        box-shadow: 0 4px 12px rgba(0, 70, 255, 0.3);
    }
    
    /* 정보 카드 */
    .info-card {
        background: linear-gradient(135deg, #0046FF, #0072CE);
        border: 1px solid #0046FF;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
    }
    
    .info-card h4 {
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    /* 버튼 스타일 개선 */
    .stButton > button {
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 70, 255, 0.3);
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff, #f8f9fa);
    }
    
    /* 프레젠테이션 모드 스타일 */
    .presentation-mode {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: #f8f9fa;
        z-index: 9999;
        display: flex;
        flex-direction: column;
    }
    
    .presentation-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 10000;
    }
    
    .presentation-content {
        flex: 1;
        overflow-y: auto;
        padding-top: 80px;
        padding-bottom: 100px;
    }
    
    .slide-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .slide-content {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        min-height: 500px;
    }
    
    .presentation-controls {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem 2rem;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        z-index: 10000;
    }
    
    .control-button {
        background: #0046FF;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 70, 255, 0.3);
    }
    
    .control-button:hover {
        background: #0072CE;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0, 70, 255, 0.4);
    }
    
    .control-button-secondary {
        background: #f8f9fa;
        color: #333;
        border: 1px solid #ddd;
    }
    
    .control-button-secondary:hover {
        background: #e9ecef;
    }
    
    .control-button-danger {
        background: #dc3545;
        color: white;
    }
    
    .control-button-danger:hover {
        background: #c82333;
    }
    
    /* 리포트 프리뷰 */
    .report-preview {
        background: white;
        padding: 2rem;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* 추천 카드 */
    .recommendation-card {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #0046FF;
        transition: all 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* 반응형 미디어 쿼리 */
    @media (max-width: 768px) {
        .hero-header {
            padding: 1.5rem;
            border-radius: 16px;
        }
        
        .action-buttons {
            flex-direction: column;
        }
        
        .action-btn {
            width: 100%;
            text-align: center;
        }
        
        .metric-grid {
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 0.75rem;
        }
    }
    
    /* 애니메이션 */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* 프린트 스타일 */
    @media print {
        .no-print {
            display: none !important;
        }
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
        SupplyChainAnalyzer(),
        PresentationMode(),
        ReportGenerator()
    )

engine, data_loader, ai_predictor, product_matcher, supply_chain_analyzer, presentation_mode, report_generator = init_systems()

def main():
    # 프레젠테이션 모드 체크
    if st.session_state.get('presentation_mode', False):
        display_presentation_mode()
        return
    
    # 일반 모드
    display_normal_mode()

def display_normal_mode():
    """일반 모드 표시"""
    
    # 모던 헤더
    display_modern_header()
    
    # 메인 메트릭 (평가 완료시)
    if 'evaluation_result' in st.session_state:
        display_modern_metrics()
    
    # 사이드바
    setup_sidebar()
    
    # 메인 컨텐츠
    if 'evaluation_result' in st.session_state:
        display_main_dashboard()
    else:
        display_welcome_screen()
    
    # 푸터
    display_modern_footer()

def display_modern_header():
    """모던 헤더 디자인"""
    if 'evaluation_result' in st.session_state:
        header_html = """
        <div class="hero-header fade-in">
            <div style="position: relative; z-index: 1;">
                <h1 class="hero-title">ShinhanESG Enterprise</h1>
                <p class="hero-subtitle">AI 기반 대기업 ESG 통합관리 플랫폼 | Powered by Minseong Park</p>
            </div>
        </div>
        """
    else:
        header_html = """
        <div class="hero-header fade-in">
            <div style="position: relative; z-index: 1;">
                <h1 class="hero-title">ShinhanESG Enterprise</h1>
                <p class="hero-subtitle">AI 기반 대기업 ESG 통합관리 플랫폼 | Powered by Minseong Park</p>
            </div>
        </div>
        """
    
    st.markdown(header_html, unsafe_allow_html=True)
    
    # 버튼 액션 처리 (평가 완료시 - 헤더 아래에 버튼 배치)
    if 'evaluation_result' in st.session_state:
        col1, col2, col3, col4 = st.columns([1.2, 1, 1, 4])
        
        with col1:
            if st.button("프레젠테이션", key="header_pres_btn", use_container_width=True, type="primary"):
                st.session_state.presentation_mode = True
                st.session_state.current_slide = 0
                st.rerun()
        
        with col2:
            if st.button("리포트 생성", key="header_report_btn", use_container_width=True):
                st.session_state.show_report_modal = True
                st.rerun()
        
        with col3:
            if st.button("대시보드", key="header_dash_btn", use_container_width=True):
                # 리포트 모달 닫기
                st.session_state.show_report_modal = False
                # 대시보드로 스크롤 (자바스크립트 사용)
                st.markdown("""
                <script>
                    var element = document.querySelector('[data-testid="stTabs"]');
                    if (element) {
                        element.scrollIntoView({behavior: 'smooth', block: 'start'});
                    }
                </script>
                """, unsafe_allow_html=True)
                st.rerun()
        
        # 리포트 모달
        if st.session_state.get('show_report_modal', False):
            display_report_modal()

def display_modern_metrics():
    """모던 메트릭 카드"""
    evaluation = st.session_state.evaluation_result
    
    # 컬럼으로 메트릭 표시
    cols = st.columns(6)
    
    # ESG 등급
    with cols[0]:
        grade = evaluation['grade']
        grade_color = engine.grade_system[grade]['color']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ESG 등급</div>
            <div class="grade-badge" style="background: {grade_color}; color: white;">
                {grade}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ESG 총점
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ESG 총점</div>
            <div class="metric-value">{evaluation['scores']['total']:.1f}</div>
            <div class="metric-delta">▲ {evaluation['scores']['total']-70:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 금리 우대
    with cols[2]:
        benefits = evaluation['financial_benefits']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">금리 우대</div>
            <div class="metric-value">{benefits['discount_rate']}%p</div>
            <div class="metric-delta">연 {benefits['annual_savings']:.0f}억 절감</div>
        </div>
        """, unsafe_allow_html=True)
    
    # AI 신뢰도
    with cols[3]:
        if 'ai_predictions' in st.session_state:
            confidence = st.session_state.ai_predictions['confidence']['confidence_score']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">AI 신뢰도</div>
                <div class="metric-value">{confidence:.0f}%</div>
                <div class="metric-delta">예측 활성화</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">AI 신뢰도</div>
                <div class="metric-value">-</div>
                <div class="metric-delta">대기</div>
            </div>
            """, unsafe_allow_html=True)
    
    # 금융상품
    with cols[4]:
        if 'matched_products' in st.session_state:
            product_count = len(st.session_state.matched_products['recommended_loans'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">추천 상품</div>
                <div class="metric-value">{product_count}개</div>
                <div class="metric-delta">매칭 완료</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">추천 상품</div>
                <div class="metric-value">-</div>
                <div class="metric-delta">대기</div>
            </div>
            """, unsafe_allow_html=True)
    
    # 공급망
    with cols[5]:
        if 'supply_chain_analysis' in st.session_state:
            supply_grade = st.session_state.supply_chain_analysis['risk_assessment']['supply_chain_grade']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">공급망 등급</div>
                <div class="metric-value">{supply_grade}</div>
                <div class="metric-delta">분석 완료</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">공급망 등급</div>
                <div class="metric-value">-</div>
                <div class="metric-delta">대기</div>
            </div>
            """, unsafe_allow_html=True)

def setup_sidebar():
    """사이드바 설정"""
    with st.sidebar:
        # 로고
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="https://i.namu.wiki/i/Etmt-wojOBWr5gVcPR0qrTxuej558yfzzyYr0xXYSxljpLuEdPWGSPi-aPdJHQrpZY2o7zvuUMb4PE6PvFjQ3Q.svg" 
                 style="width: 100%; max-width: 200px;">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 평가 설정
        st.markdown("### 평가 설정")
        
        # 기업 선택
        enterprise_list = data_loader.get_enterprise_list()
        if enterprise_list:
            selected_enterprise = st.selectbox(
                "평가 대상 기업",
                enterprise_list,
                help="ESG 평가를 진행할 기업을 선택하세요"
            )
            
            # 기업 정보
            enterprise_data = data_loader.get_enterprise_data(selected_enterprise)
            if enterprise_data:
                display_company_info(enterprise_data)
                
                st.markdown("---")
                
                # 평가 옵션
                st.markdown("### 평가 옵션")
                
                col1, col2 = st.columns(2)
                with col1:
                    enable_ai = st.checkbox("AI 예측", value=True)
                    enable_supply = st.checkbox("공급망", value=True)
                
                with col2:
                    enable_fin = st.checkbox("금융상품", value=True)
                    enable_report = st.checkbox("리포트", value=True)
                
                if enable_ai:
                    prediction_period = st.select_slider(
                        "예측 기간",
                        options=["3개월", "6개월", "1년", "3년"],
                        value="1년"
                    )
                
                st.markdown("---")
                
                # 실행 버튼
                if st.button("통합 ESG 평가 실행", 
                           type="primary", 
                           use_container_width=True,
                           key="execute_btn"):
                    execute_evaluation(
                        enterprise_data, 
                        selected_enterprise,
                        enable_ai, 
                        enable_fin, 
                        enable_supply,
                        prediction_period if enable_ai else "1년"
                    )
        else:
            st.error("데이터를 로드할 수 없습니다.")

def display_company_info(enterprise_data):
    """기업 정보 표시"""
    basic_info = enterprise_data.get('basic_info', {})
    
    st.markdown(f"""
    <div class="info-card">
        <h4>기업 정보</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1.5rem;">
            <div style="background: rgba(255, 255, 255, 0.15); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.2);">
                <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; font-weight: 500; margin-bottom: 0.5rem;">업종</div>
                <div style="color: white; font-size: 1.4rem; font-weight: 600;">{basic_info.get('industry', 'N/A')}</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.15); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.2);">
                <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; font-weight: 500; margin-bottom: 0.5rem;">직원수</div>
                <div style="color: white; font-size: 1.4rem; font-weight: 600;">{basic_info.get('employee_count', 0):,}명</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.15); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.2);">
                <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; font-weight: 500; margin-bottom: 0.5rem;">자산</div>
                <div style="color: white; font-size: 1.4rem; font-weight: 600;">{basic_info.get('asset_size', 0):,}억</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.15); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.2);">
                <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem; font-weight: 500; margin-bottom: 0.5rem;">매출</div>
                <div style="color: white; font-size: 1.4rem; font-weight: 600;">{basic_info.get('revenue', 10000):,}억</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_report_modal():
    """리포트 생성 모달"""
    evaluation = st.session_state.evaluation_result
    company_name = st.session_state.get('selected_enterprise', 'Unknown')
    
    # 리포트 생성 옵션
    with st.expander("리포트 생성 옵션", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("대시보드 PDF", use_container_width=True):
                with st.spinner("PDF 생성 중..."):
                    html_report = report_generator.generate_html_report(
                        evaluation,
                        company_name,
                        st.session_state.get('ai_predictions'),
                        st.session_state.get('matched_products'),
                        st.session_state.get('supply_chain_analysis')
                    )
                    
                    download_link = report_generator.create_pdf_download_link(
                        html_report,
                        f"ESG_Report_{company_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
                    )
                    
                    st.markdown(download_link, unsafe_allow_html=True)
                    st.success("리포트가 생성되었습니다!")
        
        with col2:
            if st.button("Excel 데이터", use_container_width=True):
                with st.spinner("Excel 생성 중..."):
                    excel_data = report_generator.generate_excel_report(
                        evaluation,
                        company_name
                    )
                    
                    st.download_button(
                        label="Excel 다운로드",
                        data=excel_data,
                        file_name=f"ESG_Data_{company_name}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("Excel 파일이 생성되었습니다!")
    
    # 리포트 미리보기
    st.markdown("### 리포트 미리보기")
    
    preview_html = f"""
    <div class="report-preview">
        <h2 style="color: #0046FF; margin-bottom: 1rem;">ESG 종합 평가 리포트</h2>
        <p><strong>기업명:</strong> {company_name}</p>
        <p><strong>평가일:</strong> {datetime.now().strftime('%Y년 %m월 %d일')}</p>
        <hr style="margin: 1.5rem 0;">
        <h3 style="color: #333;">주요 결과</h3>
        <ul>
            <li>ESG 등급: <strong style="color: {engine.grade_system[evaluation['grade']]['color']};">{evaluation['grade']}</strong></li>
            <li>종합 점수: <strong>{evaluation['scores']['total']:.1f}점</strong></li>
            <li>금리 우대: <strong>{evaluation['financial_benefits']['discount_rate']}%p</strong></li>
            <li>연간 절감: <strong>{evaluation['financial_benefits']['annual_savings']:.0f}억원</strong></li>
        </ul>
        <hr style="margin: 1.5rem 0;">
        <h3 style="color: #333;">영역별 점수</h3>
        <ul>
            <li>환경(E): {evaluation['scores']['E']:.1f}점</li>
            <li>사회(S): {evaluation['scores']['S']:.1f}점</li>
            <li>거버넌스(G): {evaluation['scores']['G']:.1f}점</li>
        </ul>
    </div>
    """
    
    st.markdown(preview_html, unsafe_allow_html=True)
    
    # 닫기 버튼
    if st.button("닫기", use_container_width=True, key="close_report_modal"):
        st.session_state.show_report_modal = False
        st.rerun()

def display_main_dashboard():
    """메인 대시보드 - 트렌디한 탭 디자인"""
    tabs = st.tabs([
        "종합 대시보드",
        "ESG 평가",
        "AI 예측",
        "금융상품",
        "공급망",
        "개선전략"
    ])
    
    with tabs[0]:
        display_executive_dashboard()
    
    with tabs[1]:
        display_esg_evaluation()
    
    with tabs[2]:
        if st.session_state.get('ai_enabled', False):
            display_ai_predictions()
        else:
            st.info("AI 예측 기능을 활성화하려면 사이드바에서 옵션을 선택하세요.")
    
    with tabs[3]:
        if st.session_state.get('financial_enabled', False):
            display_financial_products()
        else:
            st.info("금융상품 매칭을 활성화하려면 사이드바에서 옵션을 선택하세요.")
    
    with tabs[4]:
        if st.session_state.get('supply_chain_enabled', False):
            display_supply_chain()
        else:
            st.info("공급망 분석을 활성화하려면 사이드바에서 옵션을 선택하세요.")
    
    with tabs[5]:
        display_improvement_strategy()

def display_executive_dashboard():
    """경영진 대시보드"""
    st.markdown("## 대시보드")
    
    evaluation = st.session_state.evaluation_result
    
    # 상단 요약
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="info-card" style="text-align: center;">
            <h3 style="margin: 0 0 1rem 0; color: white;"></h3>
            <p style="font-size: 1.1rem; margin: 0;">
                귀사는 현재 <strong>{evaluation['grade']} 등급</strong>으로 평가되었으며,
                이는 <strong>연간 {evaluation['financial_benefits']['annual_savings']:.0f}억원</strong>의 금융비용 절감 효과를 가져옵니다.
                지속적인 ESG 개선을 통해 더 큰 가치를 창출할 수 있습니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 주요 지표 카드
    st.markdown("### 핵심 성과 지표")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # ESG 점수 게이지
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
        # 영역별 레이더 차트
        categories = ['E', 'S', 'G']
        values = [evaluation['scores']['E'], evaluation['scores']['S'], evaluation['scores']['G']]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=['환경', '사회', '거버넌스', '환경'],
            fill='toself',
            name='ESG Score'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=250,
            title="영역별 균형"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # 재무 영향
        st.markdown("#### 재무 영향")
        cumulative_5y = evaluation['financial_benefits']['annual_savings'] * 5
        
        metrics_html = f"""
        <div style="padding: 10px;">
            <div style="margin: 10px 0;">
                <span style="color: #666;">연간 절감:</span>
                <span style="float: right; font-weight: bold;">{evaluation['financial_benefits']['annual_savings']:.0f}억원</span>
            </div>
            <div style="margin: 10px 0;">
                <span style="color: #666;">5년 누적:</span>
                <span style="float: right; font-weight: bold;">{cumulative_5y:.0f}억원</span>
            </div>
            <div style="margin: 10px 0;">
                <span style="color: #666;">예상 ROI:</span>
                <span style="float: right; font-weight: bold;">250%</span>
            </div>
        </div>
        """
        st.markdown(metrics_html, unsafe_allow_html=True)
    
    # 트렌드 차트
    if 'ai_predictions' in st.session_state:
        st.markdown("### 성과 트렌드 및 예측")
        
        historical = st.session_state.ai_predictions['historical']
        predictions = st.session_state.ai_predictions['predictions']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=historical['date'], y=historical['total'],
            mode='lines+markers', name='실적',
            line=dict(color='blue', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=predictions['date'], y=predictions['total'],
            mode='lines+markers', name='AI 예측',
            line=dict(color='red', width=2, dash='dash')
        ))
        fig.add_hline(y=80, line_dash="dot", line_color="green",
                     annotation_text="목표 (A- 등급)")
        
        fig.update_layout(
            xaxis_title="기간", yaxis_title="ESG 점수",
            height=300, showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

def display_esg_evaluation():
    """ESG 평가 상세"""
    st.markdown("## ESG 평가 상세")
    
    evaluation = st.session_state.evaluation_result
    
    # 점수 요약
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("환경(E)", f"{evaluation['scores']['E']:.1f}점",
                 "우수" if evaluation['scores']['E'] >= 80 else "보통")
    with col2:
        st.metric("사회(S)", f"{evaluation['scores']['S']:.1f}점",
                 "우수" if evaluation['scores']['S'] >= 80 else "보통")
    with col3:
        st.metric("거버넌스(G)", f"{evaluation['scores']['G']:.1f}점",
                 "우수" if evaluation['scores']['G'] >= 80 else "보통")
    with col4:
        st.metric("종합", f"{evaluation['scores']['total']:.1f}점",
                 evaluation['grade'])
    
    # 상세 분석
    st.markdown("### 영역별 상세 분석")
    
    tab1, tab2, tab3 = st.tabs(["환경", "사회", "거버넌스"])
    
    with tab1:
        display_environmental_details(evaluation['details']['E'])
    
    with tab2:
        display_social_details(evaluation['details']['S'])
    
    with tab3:
        display_governance_details(evaluation['details']['G'])
    
    # 규제 준수
    st.markdown("### 규제 준수 현황")
    display_compliance_status(evaluation['compliance'])

def display_ai_predictions():
    """AI 예측 결과"""
    st.markdown("## AI 예측 분석")
    
    if 'ai_predictions' not in st.session_state:
        st.warning("AI 예측을 먼저 실행해주세요.")
        return
    
    predictions_data = st.session_state.ai_predictions
    
    # 예측 요약
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
    
    # 예측 차트
    display_prediction_chart(predictions_data)
    
    # 개선 전략
    display_ai_improvement_strategy(predictions_data)

def display_financial_products():
    """금융상품 매칭"""
    st.markdown("## 맞춤형 금융상품")
    
    if 'matched_products' not in st.session_state:
        st.warning("금융상품 매칭을 먼저 실행해주세요.")
        return
    
    matched = st.session_state.matched_products
    package = st.session_state.get('financing_package', {})
    
    # 패키지 요약
    if package:
        st.success(f"""
        ### {package['package_name']}
        - **총 한도**: {package['total_facility']:,}억원
        - **평균 우대**: {package['average_discount']}%p
        - **연간 절감**: {package['annual_savings']:.1f}억원
        - **5년 가치**: {package['package_value_5y']:.1f}억원
        """)
    
    # 상품 목록
    display_product_list(matched)

def display_supply_chain():
    """공급망 분석"""
    st.markdown("## 공급망 ESG 분석")
    
    if 'supply_chain_analysis' not in st.session_state:
        st.warning("공급망 분석을 먼저 실행해주세요.")
        return
    
    analysis = st.session_state.supply_chain_analysis
    
    # Scope 3 분석
    display_scope3_analysis(analysis['scope3_emissions'])
    
    # 공급업체 리스크
    display_supplier_risks(analysis['risk_assessment'])
    
    # 회복탄력성
    if 'resilience' in analysis:
        display_supply_resilience(analysis['resilience'])

def display_improvement_strategy():
    """개선 전략"""
    st.markdown("## 종합 개선 전략")
    
    evaluation = st.session_state.evaluation_result
    
    # 로드맵 생성
    roadmap = create_improvement_roadmap(evaluation)
    
    # 단계별 전략
    st.markdown("### ESG 개선 로드맵")
    
    for phase in roadmap['phases']:
        with st.expander(f"**Phase {phase['phase']}**: {phase['name']} ({phase['timeline']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**목표**: {phase['target']}")
                st.write("**주요 활동**:")
                for activity in phase['activities']:
                    st.write(f"• {activity}")
            
            with col2:
                st.write(f"**투자**: {phase['investment']}억원")
                st.write(f"**기대 성과**: {phase['expected_outcome']}")
    
    # 시나리오 분석
    display_scenario_analysis(evaluation)

def display_welcome_screen():
    """환영 화면 - 모던 디자인"""
    st.markdown("""
    <div class="fade-in" style="text-align: center; padding: 3rem 1rem;">
        <h1 style="font-size: 3rem; color: #0046FF; margin-bottom: 1rem;">
            Welcome to ShinhanESG
        </h1>
        <p style="font-size: 1.3rem; color: #666; margin-bottom: 3rem;">
            AI 기반 대기업 ESG 통합관리 플랫폼
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <h4 style="margin-bottom: 0.5rem;">ESG 평가</h4>
            <p style="color: #666; font-size: 0.9rem;">
                신한은행 7등급 체계<br>정밀 평가
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <h4 style="margin-bottom: 0.5rem;">AI 예측</h4>
            <p style="color: #666; font-size: 0.9rem;">
                머신러닝 기반<br>미래 성과 예측
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <h4 style="margin-bottom: 0.5rem;">금융 솔루션</h4>
            <p style="color: #666; font-size: 0.9rem;">
                맞춤형 ESG<br>금융상품 매칭
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <h4 style="margin-bottom: 0.5rem;">공급망 분석</h4>
            <p style="color: #666; font-size: 0.9rem;">
                Scope 3 배출량<br>리스크 평가
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem;">
        <p style="font-size: 1.1rem; color: #333;">
            좌측 사이드바에서 기업을 선택하고 평가를 시작하세요
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_modern_footer():
    """모던 푸터"""
    st.markdown("""
    <div style="margin-top: 4rem; padding: 2rem 0; border-top: 1px solid #e9ecef;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <strong style="color: #0046FF;">ShinhanESG Enterprise</strong>
                <span style="color: #666; margin-left: 1rem;">© 2025 Shinhan Bank</span>
            </div>
            <div style="display: flex; gap: 2rem; color: #666; font-size: 0.9rem;">
                <span>esg@shinhan.com</span>
                <span>02-6360-3000</span>
                <span>shinhan.com/esg</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_presentation_mode():
    """프레젠테이션 모드"""
    if 'evaluation_result' not in st.session_state:
        st.session_state.presentation_mode = False
        st.rerun()
        return
    
    # 슬라이드 생성
    if 'presentation_slides' not in st.session_state:
        st.session_state.presentation_slides = presentation_mode.create_presentation(
            st.session_state.evaluation_result,
            st.session_state.get('ai_predictions'),
            st.session_state.get('matched_products'),
            st.session_state.get('supply_chain_analysis')
        )
    
    slides = st.session_state.presentation_slides
    current_slide = st.session_state.get('current_slide', 0)
    
    # 프레젠테이션 모드 전용 CSS
    st.markdown("""
    <style>
        /* 프레젠테이션 모드에서 상단 패딩 제거 */
        .main > div {
            padding-top: 0;
        }
        
        /* 프레젠테이션 버튼 스타일 */
        .stButton > button {
            background: linear-gradient(135deg, #0046FF, #0072CE);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 70, 255, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 70, 255, 0.4);
            background: linear-gradient(135deg, #0072CE, #0046FF);
        }
        
        /* 종료 버튼 특별 스타일 */
        div[data-testid="column"]:last-child .stButton > button {
            background: #FF4757;
            box-shadow: 0 4px 12px rgba(255, 71, 87, 0.3);
        }
        
        div[data-testid="column"]:last-child .stButton > button:hover {
            background: #E83E4C;
            box-shadow: 0 6px 20px rgba(255, 71, 87, 0.4);
        }
        
        /* 슬라이드 선택 드롭다운 스타일 */
        .stSelectbox > div > div {
            background: white;
            border: 2px solid #0046FF;
            border-radius: 12px;
            padding: 0.5rem;
        }
        
        /* 체크박스 스타일 */
        .stCheckbox > label {
            font-weight: 500;
            color: #333;
        }
        
        /* Progress bar 스타일 */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #0046FF, #0072CE);
        }
        
        /* 슬라이드 내용이 잘리지 않도록 */
        .element-container {
            margin-top: 0 !important;
        }
        
        /* 첫 번째 요소의 마진 제거 */
        .element-container:first-child {
            margin-top: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 프레젠테이션 컨테이너
    container = st.container()
    
    # 상단 컨트롤
    col1, col2, col3, col4, col5 = st.columns([1, 2, 4, 1, 1])
    
    with col1:
        if st.button("◀ 이전", key="prev_btn", disabled=(current_slide == 0)):
            st.session_state.current_slide = current_slide - 1
            st.rerun()
    
    with col2:
        st.markdown(f"### 슬라이드 {current_slide + 1} / {len(slides)}")
    
    with col3:
        # Progress bar
        progress = (current_slide + 1) / len(slides)
        st.progress(progress)
    
    with col4:
        if st.button("다음 ▶", key="next_btn", disabled=(current_slide >= len(slides) - 1)):
            st.session_state.current_slide = current_slide + 1
            st.rerun()
    
    with col5:
        if st.button("✕ 종료", key="exit_btn"):
            st.session_state.presentation_mode = False
            st.session_state.current_slide = 0
            st.rerun()
    
    st.markdown("---")
    
    # 슬라이드 내용 (상단 여백 추가)
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    with container:
        presentation_mode.render_slide(slides[current_slide])
    
    # 하단 컨트롤
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        # 자동 재생
        if st.checkbox("자동 재생", key="auto_play"):
            time.sleep(5)  # 5초 후 다음 슬라이드
            if current_slide < len(slides) - 1:
                st.session_state.current_slide = current_slide + 1
                st.rerun()
    
    with col2:
        # 슬라이드 선택
        selected_slide = st.selectbox(
            "슬라이드 이동",
            range(len(slides)),
            format_func=lambda x: f"{x+1}. {slides[x].get('title', 'Slide')}",
            index=current_slide,
            label_visibility="collapsed"
        )
        if selected_slide != current_slide:
            st.session_state.current_slide = selected_slide
            st.rerun()
    
    with col3:
        # 전체화면 팁
        st.info("F11: 전체화면")

# 헬퍼 함수들

def execute_evaluation(enterprise_data, selected_enterprise, 
                       enable_ai, enable_financial, enable_supply_chain, 
                       prediction_period):
    """통합 평가 실행"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 1. 기본 평가
    status_text.text("ESG 평가 진행 중...")
    progress_bar.progress(20)
    evaluation = engine.evaluate_enterprise(enterprise_data)
    st.session_state.evaluation_result = evaluation
    st.session_state.selected_enterprise = selected_enterprise
    st.session_state.enterprise_data = enterprise_data
    
    # 2. AI 예측
    if enable_ai:
        status_text.text("AI 예측 분석 중...")
        progress_bar.progress(40)
        st.session_state.ai_enabled = True
        st.session_state.prediction_period = prediction_period
        perform_ai_prediction(evaluation)
    
    # 3. 금융상품 매칭
    if enable_financial:
        status_text.text("금융상품 매칭 중...")
        progress_bar.progress(60)
        st.session_state.financial_enabled = True
        perform_financial_matching(enterprise_data, evaluation)
    
    # 4. 공급망 분석
    if enable_supply_chain:
        status_text.text("공급망 분석 중...")
        progress_bar.progress(80)
        st.session_state.supply_chain_enabled = True
        perform_supply_chain_analysis(enterprise_data)
    
    # 완료
    progress_bar.progress(100)
    status_text.text("평가 완료!")
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()
    
    st.success("모든 평가가 성공적으로 완료되었습니다!")
    st.balloons()
    
    # 페이지 새로고침으로 헤더 업데이트
    st.rerun()

def perform_ai_prediction(evaluation: Dict):
    """AI 예측 수행"""
    current_scores = evaluation['scores']
    company_name = st.session_state.get('selected_enterprise', None)
    historical_data = ai_predictor.generate_historical_data(current_scores, periods=24, company_name=company_name)
    ai_predictor.train_prediction_model(historical_data)
    
    period_map = {"3개월": 3, "6개월": 6, "1년": 12, "3년": 36}
    periods = period_map.get(st.session_state.prediction_period, 12)
    
    predictions = ai_predictor.predict_future_scores(historical_data, periods=periods, company_name=company_name)
    target_grade = "A" if evaluation['grade'].startswith("B") else "A+"
    improvement_analysis = ai_predictor.analyze_improvement_drivers(current_scores, target_grade)
    
    st.session_state.ai_predictions = {
        'historical': historical_data,
        'predictions': predictions,
        'improvement_analysis': improvement_analysis,
        'confidence': ai_predictor.get_prediction_confidence(predictions)
    }

def perform_financial_matching(company_data: Dict, evaluation: Dict):
    """금융상품 매칭 수행"""
    matched_products = product_matcher.match_products(company_data, evaluation)
    st.session_state.matched_products = matched_products
    
    financing_needs = {'total_amount': 1000}
    package = product_matcher.create_financing_package(
        company_data, evaluation, financing_needs
    )
    st.session_state.financing_package = package

def perform_supply_chain_analysis(company_data: Dict):
    """공급망 분석 수행"""
    scope3_emissions = supply_chain_analyzer.calculate_scope3_emissions(company_data)
    risk_assessment = supply_chain_analyzer.assess_supplier_risks(company_data)
    resilience = supply_chain_analyzer.analyze_supply_chain_resilience(
        {'total_suppliers': 100, 'regions': ['Korea', 'China', 'Japan', 'USA']}
    )
    
    st.session_state.supply_chain_analysis = {
        'scope3_emissions': scope3_emissions,
        'risk_assessment': risk_assessment,
        'resilience': resilience
    }

def display_environmental_details(details: Dict):
    """환경 상세 표시"""
    for key, value in details.items():
        if isinstance(value, dict) and 'score' in value:
            st.metric(key.replace('_', ' ').title(), f"{value['score']:.1f}점")

def display_social_details(details: Dict):
    """사회 상세 표시"""
    for key, value in details.items():
        if isinstance(value, dict) and 'score' in value:
            st.metric(key.replace('_', ' ').title(), f"{value['score']:.1f}점")

def display_governance_details(details: Dict):
    """거버넌스 상세 표시"""
    for key, value in details.items():
        if isinstance(value, dict) and 'score' in value:
            st.metric(key.replace('_', ' ').title(), f"{value['score']:.1f}점")

def display_compliance_status(compliance: Dict):
    """규제 준수 상태 표시"""
    df = pd.DataFrame([
        {"규제": "K-Taxonomy", "상태": compliance['K-Taxonomy']['status'],
         "준수": "준수" if compliance['K-Taxonomy']['compliant'] else "미준수"},
        {"규제": "TCFD", "상태": compliance['TCFD']['status'],
         "준수": "준수" if compliance['TCFD']['compliant'] else "미준수"},
        {"규제": "GRI", "상태": compliance['GRI']['status'],
         "준수": "준수" if compliance['GRI']['compliant'] else "미준수"}
    ])
    st.dataframe(df, hide_index=True, use_container_width=True)

def display_prediction_chart(predictions_data: Dict):
    """예측 차트 표시"""
    historical = predictions_data['historical']
    predictions = predictions_data['predictions']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historical['date'], y=historical['total'],
        mode='lines+markers', name='과거 실적',
        line=dict(color='blue', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=predictions['date'], y=predictions['total'],
        mode='lines+markers', name='AI 예측',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="ESG 점수 예측",
        xaxis_title="날짜", yaxis_title="ESG 점수",
        height=400, hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

def display_ai_improvement_strategy(predictions_data: Dict):
    """AI 개선 전략 표시"""
    improvement = predictions_data['improvement_analysis']
    
    if improvement['status'] == 'success':
        st.markdown("### AI 추천 개선 전략")
        
        for idx, rec in enumerate(improvement['recommendations'][:3], 1):
            st.markdown(f"""
            <div class="recommendation-card">
                <h4>{idx}. {rec['factor'].replace('_', ' ').title()}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                    <div>
                        <strong>예상 개선</strong><br>
                        +{rec['impact']:.1f}점
                    </div>
                    <div>
                        <strong>투자 비용</strong><br>
                        {rec['cost']}억원
                    </div>
                    <div>
                        <strong>소요 기간</strong><br>
                        {rec['time']}개월
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_product_list(matched: Dict):
    """금융상품 목록 표시"""
    st.markdown("### 추천 대출 상품")
    
    for idx, loan in enumerate(matched['recommended_loans'], 1):
        with st.expander(f"{idx}. {loan['product']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("금리 우대", f"{loan['rate_discount']}%p")
                st.metric("최대 한도", f"{loan['max_amount']:,}억원")
            with col2:
                st.metric("연간 절감", f"{loan['annual_savings']:.1f}억원")
                st.write("**주요 특징**:")
                for feature in loan['features'][:2]:
                    st.write(f"• {feature}")

def display_scope3_analysis(scope3: Dict):
    """Scope 3 분석 표시"""
    st.markdown("### Scope 3 배출량")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Scope 3 총량", f"{scope3['scope3_total']:,.0f} tCO2e")
    with col2:
        st.metric("전체 대비 비중", f"{scope3['total_footprint']['scope3_percentage']:.1f}%")
    with col3:
        st.metric("데이터 품질", scope3['data_quality']['overall_quality'])

def display_supplier_risks(risk: Dict):
    """공급업체 리스크 표시"""
    st.markdown("### 공급업체 리스크")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 공급업체", f"{risk['total_suppliers']}개")
    with col2:
        st.metric("평균 리스크", f"{risk['average_risk_score']:.1f}")
    with col3:
        st.metric("고위험 업체", f"{risk['risk_distribution']['high']}개")

def display_supply_resilience(resilience: Dict):
    """공급망 회복탄력성 표시"""
    st.markdown("### 공급망 회복탄력성")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("회복력 점수", f"{resilience['resilience_score']:.1f}")
    with col2:
        st.metric("회복력 등급", resilience['resilience_grade'])
    with col3:
        st.metric("위기 대응력", resilience['resilience_level'])

def create_improvement_roadmap(evaluation: Dict) -> Dict:
    """개선 로드맵 생성"""
    current_score = evaluation['scores']['total']
    
    return {
        'phases': [
            {
                'phase': 1,
                'name': 'Quick Wins',
                'timeline': '0-3개월',
                'target': f'점수 {current_score + 5:.0f}점 달성',
                'activities': [
                    'ESG 위원회 설립',
                    '정책 수립',
                    '데이터 체계 구축'
                ],
                'investment': 50,
                'expected_outcome': '기반 구축'
            },
            {
                'phase': 2,
                'name': 'Foundation',
                'timeline': '3-12개월',
                'target': f'점수 {current_score + 10:.0f}점 달성',
                'activities': [
                    '탄소 측정 시스템',
                    '공급망 평가',
                    'ESG 교육'
                ],
                'investment': 200,
                'expected_outcome': 'B+ 등급'
            },
            {
                'phase': 3,
                'name': 'Excellence',
                'timeline': '12-24개월',
                'target': 'A- 등급',
                'activities': [
                    '재생에너지 50%',
                    'ESG 인증',
                    'Net Zero 선언'
                ],
                'investment': 500,
                'expected_outcome': 'ESG 리더'
            }
        ]
    }

def display_scenario_analysis(evaluation: Dict):
    """시나리오 분석 표시"""
    if 'ai_predictions' not in st.session_state:
        return
    
    st.markdown("### 시나리오 분석")
    
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
    
    st.dataframe(scenarios, use_container_width=True)

if __name__ == "__main__":
    main()