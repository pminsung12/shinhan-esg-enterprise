"""
프레젠테이션 모드 및 PDF 리포트 생성 모듈
경영진 브리핑 및 공식 문서 생성
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import Dict, List, Optional
import base64
from io import BytesIO
import json

class PresentationMode:
    """프레젠테이션 모드 관리"""
    
    def __init__(self):
        """초기화"""
        self.slides = []
        self.current_slide = 0
        
    def create_presentation(self, evaluation_data: Dict, 
                          ai_predictions: Optional[Dict] = None,
                          financial_products: Optional[Dict] = None,
                          supply_chain: Optional[Dict] = None) -> List[Dict]:
        """프레젠테이션 슬라이드 생성
        
        Args:
            evaluation_data: ESG 평가 결과
            ai_predictions: AI 예측 결과
            financial_products: 금융상품 매칭 결과
            supply_chain: 공급망 분석 결과
        
        Returns:
            슬라이드 리스트
        """
        slides = []
        
        # 슬라이드 1: 타이틀
        slides.append({
            'type': 'title',
            'title': 'ESG 경영 성과 보고',
            'subtitle': f"{evaluation_data.get('company', 'Enterprise')} | {datetime.now().strftime('%Y년 %m월')}",
            'presenter': '신한은행 ESG 금융본부',
            'layout': 'center'
        })
        
        # 슬라이드 2: Executive Summary
        slides.append({
            'type': 'executive_summary',
            'title': 'Executive Summary',
            'content': {
                'grade': evaluation_data['grade'],
                'score': evaluation_data['scores']['total'],
                'key_achievements': [
                    f"ESG 종합 등급 {evaluation_data['grade']} 달성",
                    f"금리 {evaluation_data['financial_benefits']['discount_rate']}%p 우대 확보",
                    f"연간 {evaluation_data['financial_benefits']['annual_savings']:.0f}억원 금융비용 절감"
                ],
                'critical_issues': evaluation_data.get('improvement_areas', [])[:3]
            }
        })
        
        # 슬라이드 3: ESG 성과 Overview
        slides.append({
            'type': 'performance_overview',
            'title': 'ESG 성과 Overview',
            'scores': {
                'E': evaluation_data['scores']['E'],
                'S': evaluation_data['scores']['S'],
                'G': evaluation_data['scores']['G'],
                'Total': evaluation_data['scores']['total']
            },
            'compliance': evaluation_data['compliance'],
            'benchmark': '업계 평균 대비 +15%'
        })
        
        # 슬라이드 4: 재무적 영향
        slides.append({
            'type': 'financial_impact',
            'title': '재무적 영향 분석',
            'metrics': {
                'current_benefits': {
                    'rate_discount': evaluation_data['financial_benefits']['discount_rate'],
                    'annual_savings': evaluation_data['financial_benefits']['annual_savings'],
                    'loan_amount': evaluation_data['financial_benefits']['loan_amount']
                },
                'projected_5y': {
                    'cumulative_savings': evaluation_data['financial_benefits']['annual_savings'] * 5,
                    'additional_financing': 2000,
                    'total_value': evaluation_data['financial_benefits']['annual_savings'] * 5 + 100
                }
            }
        })
        
        # 슬라이드 5: AI 예측 (조건부)
        if ai_predictions:
            slides.append({
                'type': 'ai_forecast',
                'title': 'AI 기반 미래 전망',
                'prediction_period': '1년',
                'predicted_score': ai_predictions['predictions'].iloc[-1]['total'] if 'predictions' in ai_predictions else 85,
                'confidence': ai_predictions.get('confidence', {}).get('confidence_score', 85),
                'improvement_potential': ai_predictions.get('improvement_analysis', {}).get('gap', 10),
                'key_drivers': [
                    '탄소중립 로드맵 실행',
                    '공급망 ESG 관리 강화',
                    'ESG 거버넌스 체계 고도화'
                ]
            })
        
        # 슬라이드 6: 금융 솔루션 (조건부)
        if financial_products:
            slides.append({
                'type': 'financial_solutions',
                'title': '맞춤형 금융 솔루션',
                'recommended_products': financial_products.get('recommended_loans', [])[:3],
                'total_facility': 5000,
                'package_benefits': {
                    'immediate': '즉시 실행 가능한 3,000억원 신규 여신',
                    'rate': '평균 1.5%p 금리 인하',
                    'services': 'ESG 컨설팅 및 인증 지원 무료'
                }
            })
        
        # 슬라이드 7: 공급망 분석 (조건부)
        if supply_chain:
            slides.append({
                'type': 'supply_chain',
                'title': '공급망 ESG 현황',
                'metrics': {
                    'scope3_emissions': supply_chain.get('scope3_emissions', {}).get('scope3_total', 10000),
                    'supplier_risk': supply_chain.get('risk_assessment', {}).get('average_risk_score', 75),
                    'high_risk_suppliers': supply_chain.get('risk_assessment', {}).get('risk_distribution', {}).get('high', 10)
                },
                'action_items': [
                    '고위험 공급업체 10개사 집중 관리',
                    'Scope 3 배출량 20% 감축 목표',
                    '공급업체 ESG 교육 프로그램 실시'
                ]
            })
        
        # 슬라이드 8: 개선 로드맵
        slides.append({
            'type': 'roadmap',
            'title': 'ESG 개선 로드맵',
            'phases': [
                {
                    'name': 'Phase 1: Quick Wins',
                    'timeline': '~3개월',
                    'actions': ['ESG 위원회 설립', '정책 수립', '기초 데이터 구축'],
                    'investment': '50억원'
                },
                {
                    'name': 'Phase 2: Foundation',
                    'timeline': '3~12개월',
                    'actions': ['탄소 측정 시스템', '공급망 평가', 'ESG 교육'],
                    'investment': '200억원'
                },
                {
                    'name': 'Phase 3: Excellence',
                    'timeline': '12~24개월',
                    'actions': ['재생에너지 50%', 'ESG 인증', 'Net Zero 선언'],
                    'investment': '500억원'
                }
            ]
        })
        
        # 슬라이드 9: Next Steps
        slides.append({
            'type': 'next_steps',
            'title': 'Next Steps',
            'immediate_actions': [
                '이사회 ESG 전략 승인 (3월)',
                'ESG 위원회 구성 및 출범 (4월)',
                '신한은행 ESG 금융 패키지 계약 (4월)'
            ],
            'q2_milestones': [
                'ESG 정책 및 규정 제정',
                '탄소 배출량 측정 시작',
                '1차 공급업체 평가 실시'
            ],
            'year_end_targets': [
                'ESG 등급 A- 달성',
                'Scope 1,2 배출량 10% 감축',
                '주요 ESG 인증 취득'
            ]
        })
        
        # 슬라이드 10: 맺음말
        slides.append({
            'type': 'closing',
            'title': '지속가능한 미래를 위한 동행',
            'message': '신한은행은 귀사의 ESG 경영 여정에 최고의 파트너가 되겠습니다.',
            'contact': {
                'team': 'ESG 금융본부',
                'email': 'esg@shinhan.com',
                'phone': '02-6360-3000',
                'website': 'www.shinhan.com/esg'
            }
        })
        
        return slides
    
    def render_slide(self, slide: Dict):
        """슬라이드 렌더링
        
        Args:
            slide: 슬라이드 데이터
        """
        slide_type = slide.get('type', 'default')
        
        if slide_type == 'title':
            self._render_title_slide(slide)
        elif slide_type == 'executive_summary':
            self._render_executive_summary(slide)
        elif slide_type == 'performance_overview':
            self._render_performance_overview(slide)
        elif slide_type == 'financial_impact':
            self._render_financial_impact(slide)
        elif slide_type == 'ai_forecast':
            self._render_ai_forecast(slide)
        elif slide_type == 'financial_solutions':
            self._render_financial_solutions(slide)
        elif slide_type == 'supply_chain':
            self._render_supply_chain(slide)
        elif slide_type == 'roadmap':
            self._render_roadmap(slide)
        elif slide_type == 'next_steps':
            self._render_next_steps(slide)
        elif slide_type == 'closing':
            self._render_closing_slide(slide)
        else:
            self._render_default_slide(slide)
    
    def _render_title_slide(self, slide: Dict):
        """타이틀 슬라이드"""
        st.markdown(f"""
        <div style="text-align: center; padding: 100px 20px;">
            <h1 style="font-size: 48px; color: #0046FF; margin-bottom: 20px;">
                {slide['title']}
            </h1>
            <h2 style="font-size: 32px; color: #666; margin-bottom: 40px;">
                {slide['subtitle']}
            </h2>
            <p style="font-size: 20px; color: #999;">
                {slide['presenter']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_executive_summary(self, slide: Dict):
        """Executive Summary 슬라이드"""
        st.markdown(f"## {slide['title']}")
        
        content = slide['content']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            ### ESG 성과
            - **등급**: {content['grade']}
            - **점수**: {content['score']:.1f}
            """)
            
            st.markdown("### 주요 성과")
            for achievement in content['key_achievements']:
                st.write(f"✅ {achievement}")
        
        with col2:
            st.markdown("### 개선 필요 영역")
            for issue in content['critical_issues']:
                st.write(f"⚠️ {issue}")
    
    def _render_performance_overview(self, slide: Dict):
        """성과 Overview 슬라이드"""
        st.markdown(f"## {slide['title']}")
        
        scores = slide['scores']
        
        # 점수 차트
        fig = go.Figure(data=[
            go.Bar(
                x=['환경(E)', '사회(S)', '거버넌스(G)', '종합'],
                y=[scores['E'], scores['S'], scores['G'], scores['Total']],
                marker_color=['#00D67A', '#0046FF', '#FFB800', '#FF4757'],
                text=[f"{v:.1f}" for v in scores.values()],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            height=400,
            yaxis_range=[0, 110],
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 규제 준수
        st.markdown("### 규제 준수 현황")
        compliance = slide['compliance']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("K-Taxonomy", compliance['K-Taxonomy']['status'])
        with col2:
            st.metric("TCFD", compliance['TCFD']['status'])
        with col3:
            st.metric("GRI", compliance['GRI']['status'])
        with col4:
            st.metric("준수도", f"{compliance['overall']:.0f}%")
    
    def _render_financial_impact(self, slide: Dict):
        """재무 영향 슬라이드"""
        st.markdown(f"## {slide['title']}")
        
        metrics = slide['metrics']
        current = metrics['current_benefits']
        projected = metrics['projected_5y']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 현재 혜택")
            st.metric("금리 우대", f"{current['rate_discount']}%p")
            st.metric("연간 절감", f"{current['annual_savings']:.0f}억원")
            st.metric("대출 한도", f"{current['loan_amount']:,}억원")
        
        with col2:
            st.markdown("### 5년 전망")
            st.metric("누적 절감", f"{projected['cumulative_savings']:.0f}억원")
            st.metric("추가 조달 가능", f"{projected['additional_financing']:,}억원")
            st.metric("총 가치 창출", f"{projected['total_value']:.0f}억원")
    
    def _render_ai_forecast(self, slide: Dict):
        """AI 예측 슬라이드"""
        st.markdown(f"## {slide['title']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("예측 기간", slide['prediction_period'])
            st.metric("예상 점수", f"{slide['predicted_score']:.1f}")
            st.metric("신뢰도", f"{slide['confidence']:.0f}%")
            st.metric("개선 잠재력", f"+{slide['improvement_potential']:.1f}점")
        
        with col2:
            st.markdown("### 주요 개선 동인")
            for driver in slide['key_drivers']:
                st.write(f"• {driver}")
    
    def _render_financial_solutions(self, slide: Dict):
        """금융 솔루션 슬라이드"""
        st.markdown(f"## {slide['title']}")
        
        st.markdown("### 추천 상품")
        for product in slide['recommended_products']:
            st.info(f"• {product.get('product', 'ESG 대출')} - 금리 {product.get('rate_discount', 1.0)}%p 우대")
        
        st.markdown("### 패키지 혜택")
        benefits = slide['package_benefits']
        st.success(f"""
        - {benefits['immediate']}
        - {benefits['rate']}
        - {benefits['services']}
        """)
    
    def _render_supply_chain(self, slide: Dict):
        """공급망 슬라이드"""
        st.markdown(f"## {slide['title']}")
        
        metrics = slide['metrics']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Scope 3 배출량", f"{metrics['scope3_emissions']:,} tCO2e")
        with col2:
            st.metric("공급업체 리스크", f"{metrics['supplier_risk']:.1f}점")
        with col3:
            st.metric("고위험 업체", f"{metrics['high_risk_suppliers']}개")
        
        st.markdown("### 주요 Action Items")
        for item in slide['action_items']:
            st.write(f"• {item}")
    
    def _render_roadmap(self, slide: Dict):
        """로드맵 슬라이드"""
        st.markdown(f"## {slide['title']}")
        
        for phase in slide['phases']:
            with st.expander(phase['name']):
                st.write(f"**기간**: {phase['timeline']}")
                st.write(f"**투자**: {phase['investment']}")
                st.write("**주요 활동**:")
                for action in phase['actions']:
                    st.write(f"• {action}")
    
    def _render_next_steps(self, slide: Dict):
        """Next Steps 슬라이드"""
        st.markdown(f"## {slide['title']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 즉시 실행")
            for action in slide['immediate_actions']:
                st.write(f"• {action}")
        
        with col2:
            st.markdown("### 2분기 목표")
            for milestone in slide['q2_milestones']:
                st.write(f"• {milestone}")
        
        with col3:
            st.markdown("### 연말 목표")
            for target in slide['year_end_targets']:
                st.write(f"• {target}")
    
    def _render_closing_slide(self, slide: Dict):
        """맺음말 슬라이드"""
        st.markdown(f"""
        <div style="text-align: center; padding: 80px 20px;">
            <h2 style="font-size: 36px; color: #0046FF; margin-bottom: 30px;">
                {slide['title']}
            </h2>
            <p style="font-size: 24px; color: #666; margin-bottom: 50px;">
                {slide['message']}
            </p>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px;">
                <p style="margin: 10px 0;"><strong>{slide['contact']['team']}</strong></p>
                <p style="margin: 10px 0;">📧 {slide['contact']['email']}</p>
                <p style="margin: 10px 0;">📞 {slide['contact']['phone']}</p>
                <p style="margin: 10px 0;">🌐 {slide['contact']['website']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_default_slide(self, slide: Dict):
        """기본 슬라이드"""
        st.markdown(f"## {slide.get('title', 'Slide')}")
        st.write(slide.get('content', 'No content'))


class ReportGenerator:
    """PDF 리포트 생성기"""
    
    def __init__(self):
        """초기화"""
        self.report_sections = []
    
    def generate_html_report(self, evaluation_data: Dict,
                            company_name: str,
                            ai_predictions: Optional[Dict] = None,
                            financial_products: Optional[Dict] = None,
                            supply_chain: Optional[Dict] = None) -> str:
        """HTML 형식 리포트 생성
        
        Args:
            evaluation_data: ESG 평가 결과
            company_name: 기업명
            ai_predictions: AI 예측 결과
            financial_products: 금융상품 매칭 결과
            supply_chain: 공급망 분석 결과
        
        Returns:
            HTML 문자열
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>ESG 평가 리포트 - {company_name}</title>
            <style>
                body {{
                    font-family: 'Noto Sans KR', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 210mm;
                    margin: 0 auto;
                    padding: 20mm;
                    background: white;
                }}
                .header {{
                    background: linear-gradient(90deg, #0046FF 0%, #00D67A 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 36px;
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    font-size: 18px;
                    opacity: 0.9;
                }}
                .section {{
                    margin-bottom: 40px;
                    page-break-inside: avoid;
                }}
                .section h2 {{
                    color: #0046FF;
                    border-bottom: 2px solid #0046FF;
                    padding-bottom: 10px;
                    font-size: 24px;
                }}
                .section h3 {{
                    color: #333;
                    font-size: 18px;
                    margin-top: 20px;
                }}
                .metrics {{
                    display: flex;
                    justify-content: space-between;
                    margin: 20px 0;
                }}
                .metric {{
                    text-align: center;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 10px;
                    flex: 1;
                    margin: 0 10px;
                }}
                .metric .value {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #0046FF;
                }}
                .metric .label {{
                    font-size: 14px;
                    color: #666;
                    margin-top: 5px;
                }}
                .grade {{
                    display: inline-block;
                    padding: 10px 20px;
                    border-radius: 20px;
                    font-size: 24px;
                    font-weight: bold;
                    color: white;
                }}
                .grade-A-plus {{ background: #00D67A; }}
                .grade-A {{ background: #00C896; }}
                .grade-A-minus {{ background: #00B386; }}
                .grade-B-plus {{ background: #0072CE; }}
                .grade-B {{ background: #0046FF; }}
                .grade-B-minus {{ background: #FFB800; }}
                .grade-C {{ background: #FF4757; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background: #f8f9fa;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 2px solid #ddd;
                    text-align: center;
                    color: #666;
                }}
                .page-break {{
                    page-break-after: always;
                }}
                @media print {{
                    body {{
                        padding: 10mm;
                    }}
                    .page-break {{
                        page-break-after: always;
                    }}
                }}
            </style>
        </head>
        <body>
        """
        
        # 헤더
        html += f"""
        <div class="header">
            <h1>ESG 종합 평가 리포트</h1>
            <p>{company_name} | {datetime.now().strftime('%Y년 %m월 %d일')}</p>
        </div>
        """
        
        # Executive Summary
        html += f"""
        <div class="section">
            <h2>Executive Summary</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="value grade grade-{evaluation_data['grade'].replace('+', '-plus').replace('-', '-minus')}">
                        {evaluation_data['grade']}
                    </div>
                    <div class="label">ESG 등급</div>
                </div>
                <div class="metric">
                    <div class="value">{evaluation_data['scores']['total']:.1f}</div>
                    <div class="label">종합 점수</div>
                </div>
                <div class="metric">
                    <div class="value">{evaluation_data['financial_benefits']['discount_rate']}%p</div>
                    <div class="label">금리 우대</div>
                </div>
                <div class="metric">
                    <div class="value">{evaluation_data['financial_benefits']['annual_savings']:.0f}억</div>
                    <div class="label">연간 절감</div>
                </div>
            </div>
        </div>
        """
        
        # ESG 상세 점수
        html += f"""
        <div class="section">
            <h2>1. ESG 평가 결과</h2>
            <table>
                <tr>
                    <th>구분</th>
                    <th>점수</th>
                    <th>등급</th>
                    <th>평가</th>
                </tr>
                <tr>
                    <td>환경 (E)</td>
                    <td>{evaluation_data['scores']['E']:.1f}</td>
                    <td>{self._score_to_grade(evaluation_data['scores']['E'])}</td>
                    <td>{'우수' if evaluation_data['scores']['E'] >= 80 else '보통' if evaluation_data['scores']['E'] >= 60 else '개선필요'}</td>
                </tr>
                <tr>
                    <td>사회 (S)</td>
                    <td>{evaluation_data['scores']['S']:.1f}</td>
                    <td>{self._score_to_grade(evaluation_data['scores']['S'])}</td>
                    <td>{'우수' if evaluation_data['scores']['S'] >= 80 else '보통' if evaluation_data['scores']['S'] >= 60 else '개선필요'}</td>
                </tr>
                <tr>
                    <td>거버넌스 (G)</td>
                    <td>{evaluation_data['scores']['G']:.1f}</td>
                    <td>{self._score_to_grade(evaluation_data['scores']['G'])}</td>
                    <td>{'우수' if evaluation_data['scores']['G'] >= 80 else '보통' if evaluation_data['scores']['G'] >= 60 else '개선필요'}</td>
                </tr>
                <tr style="font-weight: bold;">
                    <td>종합</td>
                    <td>{evaluation_data['scores']['total']:.1f}</td>
                    <td>{evaluation_data['grade']}</td>
                    <td>{'우수' if evaluation_data['scores']['total'] >= 80 else '보통' if evaluation_data['scores']['total'] >= 60 else '개선필요'}</td>
                </tr>
            </table>
        </div>
        """
        
        # 규제 준수 현황
        html += f"""
        <div class="section">
            <h2>2. 규제 준수 현황</h2>
            <table>
                <tr>
                    <th>규제</th>
                    <th>준수 여부</th>
                    <th>상태</th>
                </tr>
                <tr>
                    <td>K-Taxonomy</td>
                    <td>{'✅' if evaluation_data['compliance']['K-Taxonomy']['compliant'] else '❌'}</td>
                    <td>{evaluation_data['compliance']['K-Taxonomy']['status']}</td>
                </tr>
                <tr>
                    <td>TCFD</td>
                    <td>{'✅' if evaluation_data['compliance']['TCFD']['compliant'] else '❌'}</td>
                    <td>{evaluation_data['compliance']['TCFD']['status']}</td>
                </tr>
                <tr>
                    <td>GRI</td>
                    <td>{'✅' if evaluation_data['compliance']['GRI']['compliant'] else '❌'}</td>
                    <td>{evaluation_data['compliance']['GRI']['status']}</td>
                </tr>
            </table>
            <p><strong>종합 준수도: {evaluation_data['compliance']['overall']:.0f}%</strong></p>
        </div>
        """
        
        # 금융 혜택
        html += f"""
        <div class="page-break"></div>
        <div class="section">
            <h2>3. 금융 혜택 분석</h2>
            <h3>현재 혜택</h3>
            <ul>
                <li>기준 금리: {evaluation_data['financial_benefits']['base_rate']}%</li>
                <li>ESG 우대 할인: -{evaluation_data['financial_benefits']['discount_rate']}%p</li>
                <li>최종 적용 금리: <strong>{evaluation_data['financial_benefits']['final_rate']}%</strong></li>
                <li>대출 금액: {evaluation_data['financial_benefits']['loan_amount']:,}억원</li>
                <li>연간 이자 절감액: <strong>{evaluation_data['financial_benefits']['annual_savings']:.0f}억원</strong></li>
            </ul>
            
            <h3>5년 전망</h3>
            <ul>
                <li>누적 절감액: {evaluation_data['financial_benefits']['annual_savings'] * 5:.0f}억원</li>
                <li>추가 조달 가능 금액: 2,000억원</li>
                <li>총 경제적 가치: {evaluation_data['financial_benefits']['annual_savings'] * 5 + 100:.0f}억원</li>
            </ul>
        </div>
        """
        
        # AI 예측 (조건부)
        if ai_predictions:
            html += f"""
            <div class="section">
                <h2>4. AI 기반 미래 전망</h2>
                <ul>
                    <li>예측 신뢰도: {ai_predictions.get('confidence', {}).get('confidence_score', 85):.0f}%</li>
                    <li>1년 후 예상 점수: {ai_predictions.get('predictions', pd.DataFrame()).iloc[-1]['total'] if 'predictions' in ai_predictions else 85:.1f}점</li>
                    <li>개선 잠재력: +{ai_predictions.get('improvement_analysis', {}).get('gap', 10):.1f}점</li>
                    <li>필요 투자: {ai_predictions.get('improvement_analysis', {}).get('total_cost', 500)}억원</li>
                    <li>예상 ROI: {ai_predictions.get('improvement_analysis', {}).get('roi', 150):.0f}%</li>
                </ul>
            </div>
            """
        
        # 개선 권고사항
        html += f"""
        <div class="section">
            <h2>5. 개선 권고사항</h2>
            <ol>
        """
        
        for area in evaluation_data.get('improvement_areas', []):
            html += f"<li>{area}</li>"
        
        html += """
            </ol>
        </div>
        """
        
        # 푸터
        html += f"""
        <div class="footer">
            <p>본 리포트는 신한은행 ESG 평가 시스템에 의해 자동 생성되었습니다.</p>
            <p>문의: ESG금융본부 | 02-6360-3000 | esg@shinhan.com</p>
            <p>© 2024 Shinhan Bank. All rights reserved.</p>
        </div>
        </body>
        </html>
        """
        
        return html
    
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
    
    def create_pdf_download_link(self, html_content: str, filename: str = "ESG_Report.pdf") -> str:
        """PDF 다운로드 링크 생성
        
        Note: 실제 PDF 변환은 weasyprint 또는 pdfkit 라이브러리가 필요하지만,
        여기서는 HTML 다운로드로 대체
        
        Args:
            html_content: HTML 내용
            filename: 파일명
        
        Returns:
            다운로드 링크 HTML
        """
        # HTML을 base64로 인코딩
        b64 = base64.b64encode(html_content.encode()).decode()
        
        # 다운로드 링크 생성
        href = f'<a href="data:text/html;base64,{b64}" download="{filename.replace(".pdf", ".html")}">📥 리포트 다운로드</a>'
        
        return href
    
    def generate_excel_report(self, evaluation_data: Dict, 
                            company_name: str) -> BytesIO:
        """Excel 형식 리포트 생성
        
        Args:
            evaluation_data: ESG 평가 결과
            company_name: 기업명
        
        Returns:
            Excel 파일 BytesIO 객체
        """
        output = BytesIO()
        
        # Excel Writer 생성
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 요약 시트
            summary_df = pd.DataFrame({
                '항목': ['기업명', '평가일', 'ESG 등급', '종합 점수', '금리 우대', '연간 절감액'],
                '값': [
                    company_name,
                    datetime.now().strftime('%Y-%m-%d'),
                    evaluation_data['grade'],
                    f"{evaluation_data['scores']['total']:.1f}",
                    f"{evaluation_data['financial_benefits']['discount_rate']}%p",
                    f"{evaluation_data['financial_benefits']['annual_savings']:.0f}억원"
                ]
            })
            summary_df.to_excel(writer, sheet_name='요약', index=False)
            
            # ESG 점수 시트
            scores_df = pd.DataFrame({
                '영역': ['환경(E)', '사회(S)', '거버넌스(G)', '종합'],
                '점수': [
                    evaluation_data['scores']['E'],
                    evaluation_data['scores']['S'],
                    evaluation_data['scores']['G'],
                    evaluation_data['scores']['total']
                ],
                '등급': [
                    self._score_to_grade(evaluation_data['scores']['E']),
                    self._score_to_grade(evaluation_data['scores']['S']),
                    self._score_to_grade(evaluation_data['scores']['G']),
                    evaluation_data['grade']
                ]
            })
            scores_df.to_excel(writer, sheet_name='ESG 점수', index=False)
            
            # 규제 준수 시트
            compliance_df = pd.DataFrame({
                '규제': ['K-Taxonomy', 'TCFD', 'GRI'],
                '준수여부': [
                    evaluation_data['compliance']['K-Taxonomy']['status'],
                    evaluation_data['compliance']['TCFD']['status'],
                    evaluation_data['compliance']['GRI']['status']
                ]
            })
            compliance_df.to_excel(writer, sheet_name='규제준수', index=False)
        
        output.seek(0)
        return output