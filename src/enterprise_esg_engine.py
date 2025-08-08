"""
대기업 ESG 평가 엔진
신한은행 7등급 체계 적용
"""
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class EnterpriseESGEngine:
    """대기업 ESG 평가 엔진"""
    
    def __init__(self):
        """초기화"""
        # 신한은행 7등급 체계
        self.grade_system = {
            "A+": {"min": 90, "color": "#00D67A", "rate_discount": 2.7},
            "A": {"min": 85, "color": "#00C896", "rate_discount": 2.2},
            "A-": {"min": 80, "color": "#00B386", "rate_discount": 1.8},
            "B+": {"min": 75, "color": "#0072CE", "rate_discount": 1.5},
            "B": {"min": 70, "color": "#0046FF", "rate_discount": 1.2},
            "B-": {"min": 65, "color": "#FFB800", "rate_discount": 0.8},
            "C": {"min": 0, "color": "#FF4757", "rate_discount": 0.4}
        }
        
        # 업종별 가중치
        self.industry_weights = {
            "제조업": {"E": 0.45, "S": 0.30, "G": 0.25},
            "금융업": {"E": 0.25, "S": 0.35, "G": 0.40},
            "IT/서비스": {"E": 0.30, "S": 0.40, "G": 0.30}
        }
        
        # 평가 기준 로드
        self.load_benchmarks()
    
    def load_benchmarks(self):
        """업종별 벤치마크 로드"""
        try:
            with open('data/sample_enterprises.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.benchmarks = data.get('industry_benchmarks', {})
        except FileNotFoundError:
            print("Warning: 벤치마크 데이터를 찾을 수 없습니다. 기본값을 사용합니다.")
            self.benchmarks = {}
    
    def evaluate_enterprise(self, company_data: Dict) -> Dict:
        """기업 ESG 종합 평가"""
        try:
            # 기본 정보 추출
            industry = company_data['basic_info']['industry']
            weights = self.industry_weights.get(industry, {"E": 0.33, "S": 0.33, "G": 0.34})
            
            # 각 영역 평가
            e_score, e_details = self._evaluate_environmental(company_data, industry)
            s_score, s_details = self._evaluate_social(company_data, industry)
            g_score, g_details = self._evaluate_governance(company_data, industry)
            
            # 종합 점수 계산
            total_score = (
                e_score * weights["E"] +
                s_score * weights["S"] +
                g_score * weights["G"]
            )
            
            # 등급 결정
            grade = self._determine_grade(total_score)
            
            # 규제 준수도
            compliance_score = self._evaluate_compliance(company_data)
            
            # 결과 반환
            return {
                "evaluation_date": datetime.now().isoformat(),
                "company": company_data['basic_info']['name'],
                "industry": industry,
                "scores": {
                    "E": round(e_score, 1),
                    "S": round(s_score, 1),
                    "G": round(g_score, 1),
                    "total": round(total_score, 1)
                },
                "details": {
                    "E": e_details,
                    "S": s_details,
                    "G": g_details
                },
                "grade": grade,
                "financial_benefits": self._calculate_financial_benefits(grade, company_data),
                "compliance": compliance_score,
                "improvement_areas": self._identify_improvement_areas(e_score, s_score, g_score)
            }
            
        except Exception as e:
            print(f"평가 중 오류 발생: {str(e)}")
            return self._get_default_evaluation()
    
    def _evaluate_environmental(self, data: Dict, industry: str) -> Tuple[float, Dict]:
        """환경(E) 평가"""
        env_data = data.get('environmental', {})
        details = {}
        score = 0
        
        # 1. 탄소 배출 평가 (30점)
        carbon_total = (
            env_data.get('carbon_scope1', 0) +
            env_data.get('carbon_scope2', 0) +
            env_data.get('carbon_scope3', 0)
        )
        
        benchmark_carbon = self.benchmarks.get(industry, {}).get('avg_carbon_intensity', 10000)
        carbon_ratio = carbon_total / benchmark_carbon if benchmark_carbon > 0 else 1
        
        if carbon_ratio < 0.7:
            carbon_score = 30
        elif carbon_ratio < 1.0:
            carbon_score = 20
        elif carbon_ratio < 1.3:
            carbon_score = 10
        else:
            carbon_score = 0
        
        score += carbon_score
        details['carbon_emission'] = {
            'total': carbon_total,
            'vs_benchmark': f"{(1-carbon_ratio)*100:.1f}%" if carbon_ratio < 1 else f"+{(carbon_ratio-1)*100:.1f}%",
            'score': carbon_score
        }
        
        # 2. 재생에너지 사용 (25점)
        renewable_ratio = env_data.get('renewable_energy_ratio', 0)
        renewable_score = min(25, renewable_ratio * 50)
        score += renewable_score
        details['renewable_energy'] = {
            'ratio': renewable_ratio,
            'score': renewable_score
        }
        
        # 3. 자원 효율성 (25점)
        recycling_rate = env_data.get('waste_recycling_rate', 0)
        recycling_score = min(25, recycling_rate * 25)
        score += recycling_score
        details['resource_efficiency'] = {
            'recycling_rate': recycling_rate,
            'score': recycling_score
        }
        
        # 4. 환경 인증 (20점)
        certifications = env_data.get('env_certifications', [])
        cert_score = min(20, len(certifications) * 10)
        score += cert_score
        details['certifications'] = {
            'list': certifications,
            'score': cert_score
        }
        
        return score, details
    
    def _evaluate_social(self, data: Dict, industry: str) -> Tuple[float, Dict]:
        """사회(S) 평가"""
        social_data = data.get('social', {})
        details = {}
        score = 0
        
        # 1. 다양성 및 포용성 (25점)
        diversity_ratio = social_data.get('diversity_ratio', 0)
        diversity_score = min(25, diversity_ratio * 50)
        score += diversity_score
        details['diversity'] = {
            'ratio': diversity_ratio,
            'score': diversity_score
        }
        
        # 2. 안전 및 보건 (25점)
        accident_rate = social_data.get('accident_rate', 0.5)
        if accident_rate < 0.1:
            safety_score = 25
        elif accident_rate < 0.3:
            safety_score = 15
        else:
            safety_score = 5
        score += safety_score
        details['safety'] = {
            'accident_rate': accident_rate,
            'score': safety_score
        }
        
        # 3. 고객 만족 (25점)
        customer_satisfaction = social_data.get('customer_satisfaction', 0)
        satisfaction_score = min(25, (customer_satisfaction / 100) * 25)
        score += satisfaction_score
        details['customer'] = {
            'satisfaction': customer_satisfaction,
            'score': satisfaction_score
        }
        
        # 4. 사회 공헌 (25점)
        donation_ratio = social_data.get('donation_ratio', 0)
        contribution_score = min(25, donation_ratio * 1000)
        score += contribution_score
        details['contribution'] = {
            'donation_ratio': donation_ratio,
            'score': contribution_score
        }
        
        return score, details
    
    def _evaluate_governance(self, data: Dict, industry: str) -> Tuple[float, Dict]:
        """거버넌스(G) 평가"""
        gov_data = data.get('governance', {})
        details = {}
        score = 0
        
        # 1. 이사회 독립성 (30점)
        independent_ratio = gov_data.get('independent_director_ratio', 0)
        independence_score = min(30, independent_ratio * 50)
        score += independence_score
        details['board_independence'] = {
            'ratio': independent_ratio,
            'score': independence_score
        }
        
        # 2. ESG 거버넌스 (30점)
        has_esg_committee = gov_data.get('has_esg_committee', False)
        esg_gov_score = 30 if has_esg_committee else 0
        score += esg_gov_score
        details['esg_governance'] = {
            'has_committee': has_esg_committee,
            'score': esg_gov_score
        }
        
        # 3. 윤리 및 준법 (20점)
        ethics_violations = gov_data.get('ethics_violations', 0)
        if ethics_violations == 0:
            ethics_score = 20
        elif ethics_violations < 3:
            ethics_score = 10
        else:
            ethics_score = 0
        score += ethics_score
        details['ethics'] = {
            'violations': ethics_violations,
            'score': ethics_score
        }
        
        # 4. 정보 공개 (20점)
        disclosure_score = gov_data.get('disclosure_score', 0)
        transparency_score = min(20, (disclosure_score / 100) * 20)
        score += transparency_score
        details['transparency'] = {
            'disclosure_score': disclosure_score,
            'score': transparency_score
        }
        
        return score, details
    
    def _evaluate_compliance(self, data: Dict) -> Dict:
        """규제 준수도 평가"""
        compliance = data.get('compliance', {})
        
        k_taxonomy = compliance.get('k_taxonomy_compliant', False)
        tcfd = compliance.get('tcfd_compliant', False)
        gri = compliance.get('gri_compliant', False)
        
        total_compliance = sum([k_taxonomy, tcfd, gri]) / 3 * 100
        
        return {
            'K-Taxonomy': {'compliant': k_taxonomy, 'status': '준수' if k_taxonomy else '미준수'},
            'TCFD': {'compliant': tcfd, 'status': '준수' if tcfd else '미준수'},
            'GRI': {'compliant': gri, 'status': '준수' if gri else '미준수'},
            'overall': round(total_compliance, 1)
        }
    
    def _determine_grade(self, score: float) -> str:
        """점수에 따른 등급 결정"""
        for grade, criteria in self.grade_system.items():
            if score >= criteria['min']:
                return grade
        return 'C'
    
    def _calculate_financial_benefits(self, grade: str, company_data: Dict) -> Dict:
        """등급별 금융 혜택 계산"""
        grade_info = self.grade_system[grade]
        
        # 대출 금액
        loan_amount = company_data.get('financial', {}).get('target_loan_amount', 1000)
        
        # 금리 우대 혜택 계산
        base_rate = 3.5  # 기준 금리
        discount_rate = grade_info['rate_discount']
        final_rate = base_rate - discount_rate
        annual_savings = loan_amount * discount_rate / 100
        
        return {
            'grade': grade,
            'base_rate': base_rate,
            'discount_rate': discount_rate,
            'final_rate': final_rate,
            'annual_savings': annual_savings,
            'loan_amount': loan_amount
        }
    
    def _identify_improvement_areas(self, e_score: float, s_score: float, g_score: float) -> List[str]:
        """개선 필요 영역 식별"""
        areas = []
        
        if e_score < 70:
            areas.append("환경(E): 재생에너지 전환 및 탄소 감축 필요")
        if s_score < 70:
            areas.append("사회(S): 다양성 증진 및 안전 관리 강화 필요")
        if g_score < 70:
            areas.append("거버넌스(G): ESG 위원회 설립 및 투명성 제고 필요")
        
        return areas if areas else ["전 영역에서 우수한 성과를 보이고 있습니다."]
    
    def _get_default_evaluation(self) -> Dict:
        """기본 평가 결과 (오류 시)"""
        return {
            "evaluation_date": datetime.now().isoformat(),
            "company": "Unknown",
            "industry": "Unknown",
            "scores": {"E": 0, "S": 0, "G": 0, "total": 0},
            "details": {"E": {}, "S": {}, "G": {}},
            "grade": "C",
            "financial_benefits": {},
            "compliance": {"overall": 0},
            "improvement_areas": ["데이터 오류로 평가를 완료할 수 없습니다."]
        }