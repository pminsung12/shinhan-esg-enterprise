"""
ShinhanESG Enterprise - 메인 애플리케이션
대기업 ESG 통합관리 플랫폼
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="ShinhanESG Enterprise",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # 헤더
    st.title("🏢 ShinhanESG Enterprise")
    st.subheader("대기업 ESG 통합관리 플랫폼")
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        st.info("ESG 평가 시스템 v1.0")
        
        # 테스트 선택 옵션
        test_option = st.selectbox(
            "테스트 항목",
            ["환경 확인", "데이터 테스트", "차트 테스트"]
        )
    
    # 메인 컨텐츠
    if test_option == "환경 확인":
        show_environment_check()
    elif test_option == "데이터 테스트":
        show_data_test()
    elif test_option == "차트 테스트":
        show_chart_test()
    
    # 푸터
    st.markdown("---")
    st.caption("신한은행 ICT 인턴 프로젝트 | ShinhanESG Enterprise v1.0")

def show_environment_check():
    """환경 설정 확인"""
    st.header("✅ 환경 설정 확인")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("패키지 버전")
        
        # 주요 패키지 버전 확인
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

def show_data_test():
    """데이터 테스트"""
    st.header("📊 데이터 테스트")
    
    # 샘플 데이터 생성
    sample_data = pd.DataFrame({
        '기업명': ['삼성전자', 'SK하이닉스', 'LG화학', '현대자동차', 'POSCO'],
        'ESG점수': [82.5, 78.3, 75.9, 73.2, 71.8],
        '등급': ['A-', 'B+', 'B+', 'B', 'B'],
        '업종': ['전자', '반도체', '화학', '자동차', '철강']
    })
    
    # 데이터프레임 표시
    st.subheader("샘플 기업 ESG 데이터")
    st.dataframe(
        sample_data.style.highlight_max(subset=['ESG점수']),
        use_container_width=True
    )
    
    # 기본 통계
    st.subheader("기본 통계")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("평균 ESG 점수", f"{sample_data['ESG점수'].mean():.1f}")
    with col2:
        st.metric("최고 점수", f"{sample_data['ESG점수'].max():.1f}")
    with col3:
        st.metric("최저 점수", f"{sample_data['ESG점수'].min():.1f}")

def show_chart_test():
    """차트 테스트"""
    st.header("📈 차트 테스트")
    
    # Plotly 차트 테스트
    fig = go.Figure(data=[
        go.Bar(
            x=['환경(E)', '사회(S)', '거버넌스(G)'],
            y=[75, 82, 88],
            marker_color=['#00D67A', '#0046FF', '#FFB800']
        )
    ])
    
    fig.update_layout(
        title="ESG 영역별 점수",
        xaxis_title="영역",
        yaxis_title="점수",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 성공 메시지
    st.success("✅ 차트가 정상적으로 렌더링되었습니다!")

if __name__ == "__main__":
    main()