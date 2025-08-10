"""
신한은행 ESG 금융상품 자동 매칭 시스템
ESG 등급별 맞춤형 금융상품 추천 및 혜택 계산
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json

class FinancialProductMatcher:
    """ESG 금융상품 자동 매칭 엔진"""
    
    def __init__(self):
        """초기화"""
        # 신한은행 ESG 대출 상품 포트폴리오
        self.loan_products = {
            "ESG_우수_상생지원대출": {
                "name": "신한 ESG 우수 상생지원대출",
                "type": "기업대출",
                "target": ["대기업", "중견기업", "중소기업", "협력사"],
                "min_grade": "B",
                "rate_discount": {
                    "A+": 0.3, "A": 0.3, "A-": 0.25,
                    "B+": 0.2, "B": 0.2, "B-": 0.15
                },
                "max_amount": 5000,  # 억원
                "features": [
                    "ESG 경영 우수기업 및 협력사 대상",
                    "협력사 동반 성장 지원",
                    "간소화된 심사 프로세스"
                ],
                "required_docs": ["ESG 평가 보고서", "재무제표", "사업계획서"],
                "benefits": {
                    "금리우대": "0.2~0.3%p",
                    "한도우대": "기본한도 대비 120%",
                    "수수료감면": "약정수수료 50% 감면"
                }
            },
            "녹색정책금융_이차보전": {
                "name": "녹색정책금융 활성화 이차보전 대출",
                "type": "녹색금융",
                "target": ["제조업", "에너지", "건설업"],
                "min_grade": "B-",
                "rate_discount": {
                    "A+": 2.0, "A": 1.8, "A-": 1.5,
                    "B+": 1.2, "B": 1.0, "B-": 0.8
                },
                "max_amount": 3000,
                "features": [
                    "정부 이차보전 지원",
                    "재생에너지 사업 우대",
                    "녹색인증 기업 추가 혜택"
                ],
                "required_docs": ["녹색인증서", "환경영향평가", "탄소감축계획"],
                "benefits": {
                    "금리우대": "최대 2.0%p",
                    "이차보전": "정부지원 0.5~1.0%p",
                    "상환유예": "최대 3년 거치"
                }
            },
            "건물에너지_감축대출": {
                "name": "건물에너지 감축 상생 금융지원 협약보증 대출",
                "type": "에너지효율",
                "target": ["중소기업", "소상공인"],
                "min_grade": "C",
                "rate_discount": {
                    "A+": 1.0, "A": 1.0, "A-": 0.9,
                    "B+": 0.8, "B": 0.7, "B-": 0.6,
                    "C": 0.5
                },
                "max_amount": 30,  # 업체당
                "features": [
                    "보증료 0.5% 지원",
                    "에너지 감축률 기반 추가 혜택",
                    "한국부동산원 협약"
                ],
                "required_docs": ["에너지진단서", "감축계획서", "건물등기부"],
                "benefits": {
                    "금리우대": "최대 1.0%p",
                    "보증료지원": "0.5%",
                    "우대기간": "감축률 5% 초과시 3년"
                }
            },
            "지속가능연계대출_SLL": {
                "name": "지속가능연계대출 (SLL)",
                "type": "SLL",
                "target": ["대기업", "중견기업"],
                "min_grade": "B+",
                "rate_discount": {
                    "A+": 0.5, "A": 0.4, "A-": 0.35,
                    "B+": 0.3
                },
                "max_amount": 10000,
                "features": [
                    "ESG 목표 달성시 금리 인하",
                    "맞춤형 KPI 설정",
                    "국제 기준 준수 (LMA 원칙)"
                ],
                "required_docs": ["ESG 목표 계획서", "제3자 검증 보고서"],
                "benefits": {
                    "금리우대": "KPI 달성시 추가 인하",
                    "평가비용": "은행 부담",
                    "글로벌인증": "국제 SLL 인증"
                }
            },
            "탄소중립_특별대출": {
                "name": "탄소중립 2050 특별대출",
                "type": "탄소중립",
                "target": ["전업종"],
                "min_grade": "B-",
                "rate_discount": {
                    "A+": 1.5, "A": 1.3, "A-": 1.1,
                    "B+": 0.9, "B": 0.7, "B-": 0.5
                },
                "max_amount": 2000,
                "features": [
                    "탄소중립 로드맵 수립 기업",
                    "RE100 가입 기업 우대",
                    "탄소배출권 연계"
                ],
                "required_docs": ["탄소중립 계획서", "배출량 검증서"],
                "benefits": {
                    "금리우대": "최대 1.5%p",
                    "컨설팅": "무료 탄소중립 컨설팅",
                    "배출권": "배출권 거래 지원"
                }
            }
        }
        
        # ESG 연계 예적금 상품
        self.deposit_products = {
            "아름다운_용기_예금": {
                "name": "아름다운 용기 예·적금",
                "type": "예금",
                "base_rate": 1.65,
                "bonus_rate": 0.15,
                "max_rate": 1.8,
                "conditions": [
                    "다회용기 사용 인증",
                    "1회용컵 보증금제 참여",
                    "친환경 활동 서약"
                ],
                "term": "1년",
                "features": ["ESG 실천 포인트 적립", "우대금리 제공"]
            },
            "ESG_정기예금": {
                "name": "ESG 우수기업 정기예금",
                "type": "기업예금",
                "base_rate": 2.0,
                "bonus_rate": 0.5,
                "max_rate": 2.5,
                "conditions": ["ESG 등급 B 이상"],
                "term": "6개월~3년",
                "features": ["장기 우대금리", "자동 재예치"]
            }
        }
        
        # 그린본드 상품
        self.bond_products = {
            "신한_그린본드": {
                "name": "신한 그린본드",
                "type": "채권",
                "currency": ["KRW", "USD"],
                "min_investment": 1000,  # 억원
                "rate_range": "3.0~4.5%",
                "term": "3~7년",
                "use_of_proceeds": [
                    "재생에너지 프로젝트",
                    "에너지 효율 개선",
                    "친환경 건물",
                    "지속가능한 물 관리",
                    "청정 운송"
                ],
                "certification": "Climate Bonds Standard",
                "reporting": "연간 임팩트 보고서 제공"
            },
            "소셜본드": {
                "name": "신한 소셜본드",
                "type": "채권",
                "currency": ["KRW"],
                "min_investment": 500,
                "rate_range": "3.2~4.2%",
                "term": "3~5년",
                "use_of_proceeds": [
                    "사회적 기업 지원",
                    "취약계층 고용",
                    "교육 인프라",
                    "의료 서비스"
                ],
                "certification": "Social Bond Principles",
                "reporting": "분기별 사회적 성과 보고"
            }
        }
        
        # 특별 프로그램
        self.special_programs = {
            "ESG_컨설팅": {
                "name": "ESG 경영 컨설팅 프로그램",
                "fee": "무료 (우수고객)",
                "services": [
                    "ESG 현황 진단",
                    "개선 로드맵 수립",
                    "인증 취득 지원",
                    "정기 모니터링"
                ]
            },
            "탄소회계": {
                "name": "탄소회계 시스템 구축 지원",
                "fee": "50% 할인",
                "services": [
                    "Scope 1,2,3 측정",
                    "탄소회계 시스템 구축",
                    "TCFD 보고서 작성"
                ]
            }
        }
    
    def match_products(self, company_data: Dict, esg_evaluation: Dict) -> Dict:
        """기업에 맞는 금융상품 매칭
        
        Args:
            company_data: 기업 정보
            esg_evaluation: ESG 평가 결과
        
        Returns:
            매칭된 금융상품 및 혜택
        """
        grade = esg_evaluation['grade']
        scores = esg_evaluation['scores']
        industry = company_data['basic_info']['industry']
        asset_size = company_data['basic_info']['asset_size']
        
        # 추천 상품 리스트
        recommended_loans = []
        recommended_deposits = []
        recommended_bonds = []
        special_offers = []
        
        # 대출 상품 매칭
        for product_id, product in self.loan_products.items():
            if self._is_eligible(grade, product['min_grade']):
                # 업종 적합성 확인
                if self._check_industry_fit(industry, product['target']):
                    # 금리 혜택 계산
                    rate_discount = product['rate_discount'].get(grade, 0)
                    
                    # 예상 절감액 계산 (1000억 대출 기준)
                    loan_amount = min(1000, product['max_amount'])
                    annual_savings = loan_amount * rate_discount / 100
                    
                    recommended_loans.append({
                        'product': product['name'],
                        'type': product['type'],
                        'rate_discount': rate_discount,
                        'max_amount': product['max_amount'],
                        'annual_savings': annual_savings,
                        'features': product['features'],
                        'benefits': product['benefits'],
                        'priority': self._calculate_priority(scores, product['type'])
                    })
        
        # 우선순위 정렬
        recommended_loans.sort(key=lambda x: x['priority'], reverse=True)
        
        # 예적금 상품 매칭
        if grade >= "B":
            for product_id, product in self.deposit_products.items():
                if "기업" in product['type']:
                    recommended_deposits.append({
                        'product': product['name'],
                        'max_rate': product['max_rate'],
                        'term': product['term'],
                        'features': product['features']
                    })
        
        # 그린본드 추천 (대기업)
        if asset_size >= 1000 and grade >= "B+":
            for bond_id, bond in self.bond_products.items():
                recommended_bonds.append({
                    'product': bond['name'],
                    'type': bond['type'],
                    'rate_range': bond['rate_range'],
                    'term': bond['term'],
                    'use_of_proceeds': bond['use_of_proceeds']
                })
        
        # 특별 프로그램
        if grade >= "B":
            for program_id, program in self.special_programs.items():
                special_offers.append({
                    'program': program['name'],
                    'fee': program['fee'],
                    'services': program['services']
                })
        
        # 종합 패키지 구성
        total_benefits = self._calculate_total_benefits(
            recommended_loans,
            grade,
            loan_amount=1000
        )
        
        return {
            'matched_date': datetime.now().isoformat(),
            'company_grade': grade,
            'recommended_loans': recommended_loans[:3],  # 상위 3개
            'recommended_deposits': recommended_deposits,
            'recommended_bonds': recommended_bonds,
            'special_offers': special_offers,
            'total_benefits': total_benefits,
            'package_summary': self._create_package_summary(
                grade, scores, recommended_loans
            )
        }
    
    def _is_eligible(self, current_grade: str, min_grade: str) -> bool:
        """등급 자격 확인"""
        grade_order = ["A+", "A", "A-", "B+", "B", "B-", "C"]
        
        if current_grade in grade_order and min_grade in grade_order:
            return grade_order.index(current_grade) <= grade_order.index(min_grade)
        return False
    
    def _check_industry_fit(self, industry: str, target_list: List[str]) -> bool:
        """업종 적합성 확인"""
        if "전업종" in target_list:
            return True
        
        # 업종 매핑
        industry_map = {
            "제조업": ["제조업", "대기업", "중견기업"],
            "금융업": ["대기업", "금융업"],
            "IT/서비스": ["대기업", "중견기업", "IT"],
            "에너지": ["에너지", "제조업"],
            "건설업": ["건설업", "대기업"]
        }
        
        if industry in industry_map:
            return any(t in target_list for t in industry_map[industry])
        
        return "중소기업" in target_list or "대기업" in target_list
    
    def _calculate_priority(self, scores: Dict, product_type: str) -> float:
        """상품 우선순위 계산"""
        priority = 0
        
        # ESG 점수 기반
        priority += scores['total'] / 100 * 50
        
        # 상품 타입별 가중치
        type_weights = {
            "SLL": 30,
            "녹색금융": 25,
            "탄소중립": 25,
            "기업대출": 20,
            "에너지효율": 15
        }
        priority += type_weights.get(product_type, 10)
        
        # 환경 점수가 높으면 녹색금융 우선
        if product_type in ["녹색금융", "탄소중립"] and scores['E'] > 80:
            priority += 20
        
        return priority
    
    def _calculate_total_benefits(self, loans: List[Dict], grade: str, 
                                 loan_amount: float) -> Dict:
        """총 혜택 계산"""
        if not loans:
            return {
                'total_rate_discount': 0,
                'total_annual_savings': 0,
                'package_value': 0
            }
        
        # 최고 금리 우대
        max_discount = max(loan['rate_discount'] for loan in loans)
        
        # 연간 절감액
        annual_savings = loan_amount * max_discount / 100
        
        # 5년간 누적 절감
        cumulative_5y = annual_savings * 5
        
        # 추가 혜택 (컨설팅, 수수료 등)
        additional_benefits = 50  # 억원
        
        return {
            'total_rate_discount': max_discount,
            'total_annual_savings': annual_savings,
            'cumulative_savings_5y': cumulative_5y,
            'additional_benefits': additional_benefits,
            'package_value': cumulative_5y + additional_benefits
        }
    
    def _create_package_summary(self, grade: str, scores: Dict, 
                               loans: List[Dict]) -> Dict:
        """패키지 요약 생성"""
        # 등급별 맞춤 메시지
        grade_messages = {
            "A+": "최고 등급 혜택을 누리실 수 있습니다. VIP 전용 상품을 추천드립니다.",
            "A": "우수한 ESG 성과를 인정받아 프리미엄 혜택을 제공합니다.",
            "A-": "안정적인 ESG 경영으로 우대 금리를 적용받으실 수 있습니다.",
            "B+": "ESG 개선 노력을 지원하는 맞춤형 상품을 제공합니다.",
            "B": "ESG 도약을 위한 스텝업 패키지를 추천드립니다.",
            "B-": "ESG 시작 단계를 위한 기본 패키지를 제공합니다.",
            "C": "ESG 개선을 위한 특별 지원 프로그램을 안내드립니다."
        }
        
        # 강점 영역 파악
        strengths = []
        if scores['E'] >= 80:
            strengths.append("환경 리더십")
        if scores['S'] >= 80:
            strengths.append("사회적 책임")
        if scores['G'] >= 80:
            strengths.append("투명한 거버넌스")
        
        # 추천 focus
        focus_area = "균형적 성장"
        if scores['E'] < 70:
            focus_area = "녹색전환 가속화"
        elif scores['S'] < 70:
            focus_area = "사회가치 창출"
        elif scores['G'] < 70:
            focus_area = "거버넌스 고도화"
        
        return {
            'grade_message': grade_messages.get(grade, "맞춤형 혜택을 제공합니다."),
            'strengths': strengths,
            'focus_area': focus_area,
            'recommended_products': len(loans),
            'key_benefit': f"최대 {loans[0]['rate_discount']}%p 금리 우대" if loans else "맞춤 상담 필요"
        }
    
    def calculate_loan_terms(self, loan_amount: float, grade: str, 
                           product_type: str = "ESG_우수_상생지원대출") -> Dict:
        """대출 조건 상세 계산
        
        Args:
            loan_amount: 대출 금액 (억원)
            grade: ESG 등급
            product_type: 상품 유형
        
        Returns:
            대출 조건 상세
        """
        base_rate = 3.5  # 기준금리
        
        # 상품별 우대금리
        product = self.loan_products.get(product_type, {})
        discount = product.get('rate_discount', {}).get(grade, 0)
        
        final_rate = base_rate - discount
        
        # 상환 계산 (5년 만기)
        term_years = 5
        monthly_rate = final_rate / 12 / 100
        n_payments = term_years * 12
        
        # 원리금균등상환
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**n_payments) / \
                            ((1 + monthly_rate)**n_payments - 1)
        else:
            monthly_payment = loan_amount / n_payments
        
        total_payment = monthly_payment * n_payments
        total_interest = total_payment - loan_amount
        
        return {
            'loan_amount': loan_amount,
            'base_rate': base_rate,
            'discount_rate': discount,
            'final_rate': final_rate,
            'term_years': term_years,
            'monthly_payment': round(monthly_payment, 2),
            'total_payment': round(total_payment, 2),
            'total_interest': round(total_interest, 2),
            'savings_vs_base': round((base_rate / 100 * loan_amount * term_years) - total_interest, 2)
        }
    
    def simulate_product_upgrade(self, current_grade: str, 
                                target_grade: str) -> Dict:
        """등급 상승시 상품 업그레이드 시뮬레이션
        
        Args:
            current_grade: 현재 등급
            target_grade: 목표 등급
        
        Returns:
            업그레이드 혜택
        """
        current_benefits = []
        target_benefits = []
        
        # 현재 등급 혜택
        for product_id, product in self.loan_products.items():
            if self._is_eligible(current_grade, product['min_grade']):
                current_rate = product['rate_discount'].get(current_grade, 0)
                current_benefits.append({
                    'product': product['name'],
                    'rate_discount': current_rate
                })
        
        # 목표 등급 혜택
        for product_id, product in self.loan_products.items():
            if self._is_eligible(target_grade, product['min_grade']):
                target_rate = product['rate_discount'].get(target_grade, 0)
                target_benefits.append({
                    'product': product['name'],
                    'rate_discount': target_rate
                })
        
        # 추가 이용 가능 상품
        new_products = []
        for product_id, product in self.loan_products.items():
            if (self._is_eligible(target_grade, product['min_grade']) and 
                not self._is_eligible(current_grade, product['min_grade'])):
                new_products.append(product['name'])
        
        # 금리 개선폭 계산
        max_current = max([b['rate_discount'] for b in current_benefits], default=0)
        max_target = max([b['rate_discount'] for b in target_benefits], default=0)
        rate_improvement = max_target - max_current
        
        # 1000억 대출 기준 추가 절감액
        additional_savings = 1000 * rate_improvement / 100
        
        return {
            'current_grade': current_grade,
            'target_grade': target_grade,
            'current_products': len(current_benefits),
            'target_products': len(target_benefits),
            'new_products': new_products,
            'rate_improvement': rate_improvement,
            'additional_annual_savings': additional_savings,
            'upgrade_benefits': {
                'expanded_limits': "한도 20% 상향",
                'priority_processing': "Fast Track 심사",
                'fee_waivers': "각종 수수료 면제",
                'exclusive_services': "전담 RM 배정"
            }
        }
    
    def get_product_recommendations(self, esg_scores: Dict, 
                                   improvement_areas: List[str]) -> List[Dict]:
        """개선 영역별 금융상품 추천
        
        Args:
            esg_scores: ESG 점수
            improvement_areas: 개선 필요 영역
        
        Returns:
            추천 상품 리스트
        """
        recommendations = []
        
        # 환경 개선 필요시
        if "환경" in str(improvement_areas) or esg_scores['E'] < 70:
            recommendations.append({
                'area': '환경(E)',
                'recommended_product': '녹색정책금융 활성화 이차보전 대출',
                'reason': '친환경 전환 자금 지원',
                'benefits': [
                    '최대 2.0%p 금리 우대',
                    '정부 이차보전 추가 지원',
                    '녹색 프로젝트 컨설팅'
                ],
                'impact': 'E 점수 10~15점 상승 기대'
            })
            
            recommendations.append({
                'area': '환경(E)',
                'recommended_product': '건물에너지 감축 대출',
                'reason': '에너지 효율 개선',
                'benefits': [
                    '보증료 0.5% 지원',
                    '감축 성과 연동 우대',
                    '에너지 진단 서비스'
                ],
                'impact': '에너지 비용 20% 절감'
            })
        
        # 사회 개선 필요시
        if "사회" in str(improvement_areas) or esg_scores['S'] < 70:
            recommendations.append({
                'area': '사회(S)',
                'recommended_product': '신한 소셜본드',
                'reason': '사회적 가치 창출',
                'benefits': [
                    '사회공헌 자금 조달',
                    '이미지 개선 효과',
                    'ESG 인증 지원'
                ],
                'impact': 'S 점수 8~12점 상승 기대'
            })
        
        # 거버넌스 개선 필요시
        if "거버넌스" in str(improvement_areas) or esg_scores['G'] < 70:
            recommendations.append({
                'area': '거버넌스(G)',
                'recommended_product': '지속가능연계대출(SLL)',
                'reason': 'ESG 경영체계 구축',
                'benefits': [
                    'KPI 달성 연동 금리',
                    '국제 인증 취득',
                    'ESG 컨설팅 제공'
                ],
                'impact': 'G 점수 5~10점 상승 기대'
            })
        
        # 종합 개선
        if len(recommendations) == 0 or esg_scores['total'] < 75:
            recommendations.append({
                'area': '종합',
                'recommended_product': 'ESG 우수 상생지원대출',
                'reason': 'ESG 전반적 개선',
                'benefits': [
                    '협력사 동반 성장',
                    '유연한 자금 운용',
                    'ESG 통합 관리'
                ],
                'impact': '전체 등급 상승 지원'
            })
        
        return recommendations
    
    def create_financing_package(self, company_data: Dict, 
                                esg_evaluation: Dict,
                                financing_needs: Dict) -> Dict:
        """종합 금융 패키지 구성
        
        Args:
            company_data: 기업 정보
            esg_evaluation: ESG 평가 결과
            financing_needs: 자금 소요
        
        Returns:
            맞춤형 금융 패키지
        """
        grade = esg_evaluation['grade']
        total_needs = financing_needs.get('total_amount', 1000)
        
        # 자금 용도별 배분
        allocation = {
            'working_capital': total_needs * 0.3,
            'facility_investment': total_needs * 0.3,
            'esg_improvement': total_needs * 0.2,
            'rd_innovation': total_needs * 0.2
        }
        
        # 상품 믹스 구성
        product_mix = []
        
        # 운전자금
        if allocation['working_capital'] > 0:
            product_mix.append({
                'purpose': '운전자금',
                'amount': allocation['working_capital'],
                'product': 'ESG 우수 상생지원대출',
                'rate_discount': self.loan_products['ESG_우수_상생지원대출']['rate_discount'].get(grade, 0)
            })
        
        # 시설자금
        if allocation['facility_investment'] > 0:
            product_mix.append({
                'purpose': '시설투자',
                'amount': allocation['facility_investment'],
                'product': '녹색정책금융 이차보전',
                'rate_discount': self.loan_products['녹색정책금융_이차보전']['rate_discount'].get(grade, 0)
            })
        
        # ESG 개선자금
        if allocation['esg_improvement'] > 0:
            product_mix.append({
                'purpose': 'ESG 개선',
                'amount': allocation['esg_improvement'],
                'product': '지속가능연계대출',
                'rate_discount': 0.5 if grade >= "B+" else 0.3
            })
        
        # 혁신자금
        if allocation['rd_innovation'] > 0:
            product_mix.append({
                'purpose': 'R&D/혁신',
                'amount': allocation['rd_innovation'],
                'product': '탄소중립 특별대출',
                'rate_discount': self.loan_products['탄소중립_특별대출']['rate_discount'].get(grade, 0)
            })
        
        # 평균 금리 우대 계산
        weighted_discount = sum(p['amount'] * p['rate_discount'] for p in product_mix) / total_needs
        
        # 부가 서비스
        additional_services = []
        if grade >= "B+":
            additional_services.extend([
                "무료 ESG 컨설팅 (연 4회)",
                "탄소회계 시스템 구축 지원",
                "ESG 보고서 작성 지원",
                "전담 RM 배정"
            ])
        
        if grade >= "A-":
            additional_services.extend([
                "해외 ESG 인증 취득 지원",
                "그린본드 발행 주관",
                "ESG 투자자 매칭"
            ])
        
        # 패키지 가치 계산
        annual_value = total_needs * weighted_discount / 100  # 금리 절감
        service_value = 5 if grade >= "B+" else 2  # 서비스 가치 (억원)
        total_package_value = (annual_value * 5) + service_value  # 5년 기준
        
        return {
            'package_name': f"신한 ESG {grade} 등급 프리미엄 패키지",
            'total_facility': total_needs,
            'product_mix': product_mix,
            'average_discount': round(weighted_discount, 2),
            'annual_savings': round(annual_value, 1),
            'package_value_5y': round(total_package_value, 1),
            'additional_services': additional_services,
            'exclusive_benefits': {
                'fast_track': grade >= "B+",
                'fee_waiver': grade >= "A-",
                'global_network': grade >= "A",
                'vip_events': grade >= "A+"
            },
            'next_review': (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
            'upgrade_potential': self._get_upgrade_message(grade)
        }
    
    def _get_upgrade_message(self, current_grade: str) -> str:
        """등급 업그레이드 메시지"""
        upgrade_map = {
            "C": "B- 등급 달성시 금리 0.3%p 추가 인하",
            "B-": "B 등급 달성시 신규 상품 이용 가능",
            "B": "B+ 등급 달성시 프리미엄 서비스 제공",
            "B+": "A- 등급 달성시 VIP 혜택 시작",
            "A-": "A 등급 달성시 글로벌 네트워크 이용",
            "A": "A+ 등급 달성시 최고 수준 혜택",
            "A+": "최고 등급 유지로 독점 혜택 지속"
        }
        return upgrade_map.get(current_grade, "지속적인 ESG 개선 지원")