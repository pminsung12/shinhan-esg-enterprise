"""
공급망 ESG 분석 시스템
Scope 3 배출량 계산 및 공급업체 리스크 평가
"""
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json
import random

class SupplyChainAnalyzer:
    """공급망 ESG 분석 엔진"""
    
    def __init__(self):
        """초기화"""
        # Scope 3 카테고리 정의 (GHG Protocol 기준)
        self.scope3_categories = {
            "purchased_goods": {
                "name": "구매한 제품 및 서비스",
                "avg_emission_factor": 0.5,  # tCO2e/백만원
                "description": "원재료, 부품, 포장재 등"
            },
            "capital_goods": {
                "name": "자본재",
                "avg_emission_factor": 0.3,
                "description": "건물, 장비, 기계 등"
            },
            "fuel_energy": {
                "name": "연료 및 에너지",
                "avg_emission_factor": 0.8,
                "description": "Scope 1,2 제외 연료/에너지"
            },
            "transportation_upstream": {
                "name": "운송 및 유통(상류)",
                "avg_emission_factor": 0.2,
                "description": "구매 제품의 운송"
            },
            "waste": {
                "name": "폐기물 처리",
                "avg_emission_factor": 0.1,
                "description": "운영 중 발생 폐기물"
            },
            "business_travel": {
                "name": "출장",
                "avg_emission_factor": 0.15,
                "description": "직원 출장 관련"
            },
            "employee_commuting": {
                "name": "직원 통근",
                "avg_emission_factor": 0.05,
                "description": "직원 출퇴근"
            },
            "leased_assets": {
                "name": "리스 자산",
                "avg_emission_factor": 0.2,
                "description": "임대 시설/장비"
            },
            "transportation_downstream": {
                "name": "운송 및 유통(하류)",
                "avg_emission_factor": 0.25,
                "description": "판매 제품의 운송"
            },
            "product_use": {
                "name": "판매 제품 사용",
                "avg_emission_factor": 1.0,
                "description": "고객의 제품 사용"
            },
            "product_eol": {
                "name": "판매 제품 폐기",
                "avg_emission_factor": 0.15,
                "description": "제품 수명 종료 처리"
            },
            "investments": {
                "name": "투자",
                "avg_emission_factor": 0.4,
                "description": "투자 포트폴리오"
            }
        }
        
        # 공급업체 리스크 평가 기준
        self.risk_criteria = {
            "environmental": {
                "carbon_intensity": {"weight": 0.3, "threshold": 100},
                "waste_management": {"weight": 0.2, "threshold": 70},
                "certification": {"weight": 0.2, "threshold": 50},
                "violations": {"weight": 0.3, "threshold": 0}
            },
            "social": {
                "labor_practices": {"weight": 0.3, "threshold": 80},
                "safety_record": {"weight": 0.3, "threshold": 90},
                "community_impact": {"weight": 0.2, "threshold": 70},
                "human_rights": {"weight": 0.2, "threshold": 100}
            },
            "governance": {
                "transparency": {"weight": 0.3, "threshold": 80},
                "compliance": {"weight": 0.3, "threshold": 90},
                "ethics": {"weight": 0.2, "threshold": 85},
                "management": {"weight": 0.2, "threshold": 75}
            }
        }
        
        # 산업별 공급망 특성
        self.industry_profiles = {
            "제조업": {
                "tier1_suppliers": 50,
                "tier2_suppliers": 200,
                "critical_categories": ["purchased_goods", "transportation_upstream", "capital_goods"],
                "avg_dependency": 0.6
            },
            "IT/서비스": {
                "tier1_suppliers": 30,
                "tier2_suppliers": 100,
                "critical_categories": ["purchased_goods", "business_travel", "employee_commuting"],
                "avg_dependency": 0.4
            },
            "금융업": {
                "tier1_suppliers": 20,
                "tier2_suppliers": 50,
                "critical_categories": ["investments", "business_travel", "leased_assets"],
                "avg_dependency": 0.3
            }
        }
    
    def calculate_scope3_emissions(self, company_data: dict, 
                                  supply_chain_data: Optional[dict] = None) -> dict:
        """Scope 3 배출량 계산
        
        Args:
            company_data: 기업 정보
            supply_chain_data: 공급망 데이터 (선택)
        
        Returns:
            Scope 3 배출량 분석 결과
        """
        industry = company_data['basic_info']['industry']
        revenue = company_data['basic_info'].get('revenue', 10000)  # 억원
        
        # 공급망 데이터가 없으면 시뮬레이션
        if not supply_chain_data:
            supply_chain_data = self._simulate_supply_chain(industry, revenue)
        
        # 카테고리별 배출량 계산
        emissions_by_category = {}
        total_emissions = 0
        
        for category_id, category in self.scope3_categories.items():
            # 활동량 추정
            activity_amount = supply_chain_data.get(category_id, {}).get('amount', revenue * 0.1)
            
            # 배출계수 적용
            emission_factor = category['avg_emission_factor']
            
            # 산업별 조정
            if industry == "제조업" and category_id in ["purchased_goods", "transportation_upstream"]:
                emission_factor *= 1.5
            elif industry == "금융업" and category_id == "investments":
                emission_factor *= 2.0
            
            # 배출량 계산
            emissions = activity_amount * emission_factor
            
            emissions_by_category[category_id] = {
                'name': category['name'],
                'emissions': round(emissions, 2),
                'percentage': 0,  # 나중에 계산
                'activity_amount': activity_amount,
                'emission_factor': emission_factor
            }
            
            total_emissions += emissions
        
        # 비율 계산
        for category in emissions_by_category.values():
            category['percentage'] = round(category['emissions'] / total_emissions * 100, 1) if total_emissions > 0 else 0
        
        # 주요 배출원 식별
        sorted_categories = sorted(emissions_by_category.items(), 
                                 key=lambda x: x[1]['emissions'], 
                                 reverse=True)
        
        hotspots = [
            {
                'category': cat[1]['name'],
                'emissions': cat[1]['emissions'],
                'percentage': cat[1]['percentage'],
                'reduction_potential': self._estimate_reduction_potential(cat[0])
            }
            for cat in sorted_categories[:5]
        ]
        
        # Scope 1,2,3 통합
        scope1 = company_data.get('environmental', {}).get('carbon_scope1', 1000)
        scope2 = company_data.get('environmental', {}).get('carbon_scope2', 500)
        
        total_footprint = scope1 + scope2 + total_emissions
        
        return {
            'calculation_date': datetime.now().isoformat(),
            'scope3_total': round(total_emissions, 2),
            'scope3_categories': emissions_by_category,
            'hotspots': hotspots,
            'total_footprint': {
                'scope1': scope1,
                'scope2': scope2,
                'scope3': round(total_emissions, 2),
                'total': round(total_footprint, 2),
                'scope3_percentage': round(total_emissions / total_footprint * 100, 1)
            },
            'data_quality': self._assess_data_quality(supply_chain_data),
            'recommendations': self._generate_scope3_recommendations(hotspots)
        }
    
    def assess_supplier_risks(self, company_data: dict, 
                            supplier_list: Optional[List[dict]] = None) -> dict:
        """공급업체 ESG 리스크 평가
        
        Args:
            company_data: 기업 정보
            supplier_list: 공급업체 리스트 (선택)
        
        Returns:
            공급망 리스크 평가 결과
        """
        industry = company_data['basic_info']['industry']
        profile = self.industry_profiles.get(industry, self.industry_profiles["제조업"])
        
        # 공급업체 리스트가 없으면 시뮬레이션
        if not supplier_list:
            supplier_list = self._simulate_suppliers(profile)
        
        # 공급업체별 리스크 평가
        assessed_suppliers = []
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        for supplier in supplier_list:
            risk_scores = self._calculate_supplier_risk(supplier)
            
            # 종합 리스크 레벨 결정
            total_risk = risk_scores['total_score']
            if total_risk < 40:
                risk_level = "High"
                high_risk_count += 1
            elif total_risk < 70:
                risk_level = "Medium"
                medium_risk_count += 1
            else:
                risk_level = "Low"
                low_risk_count += 1
            
            assessed_suppliers.append({
                'supplier_name': supplier['name'],
                'tier': supplier['tier'],
                'location': supplier.get('location', 'Korea'),
                'spend': supplier.get('spend', 100),  # 억원
                'risk_level': risk_level,
                'risk_scores': risk_scores,
                'critical': supplier.get('critical', False),
                'improvement_areas': self._identify_supplier_improvements(risk_scores)
            })
        
        # 리스크별 정렬
        assessed_suppliers.sort(key=lambda x: x['risk_scores']['total_score'])
        
        # 공급망 전체 리스크 점수
        avg_risk_score = np.mean([s['risk_scores']['total_score'] for s in assessed_suppliers])
        
        # 집중도 리스크 분석
        concentration_risk = self._analyze_concentration_risk(assessed_suppliers)
        
        # 지역별 리스크 분석
        geographic_risk = self._analyze_geographic_risk(assessed_suppliers)
        
        return {
            'assessment_date': datetime.now().isoformat(),
            'total_suppliers': len(assessed_suppliers),
            'risk_distribution': {
                'high': high_risk_count,
                'medium': medium_risk_count,
                'low': low_risk_count
            },
            'average_risk_score': round(avg_risk_score, 1),
            'high_risk_suppliers': [s for s in assessed_suppliers if s['risk_level'] == "High"][:10],
            'critical_suppliers': [s for s in assessed_suppliers if s['critical']][:5],
            'concentration_risk': concentration_risk,
            'geographic_risk': geographic_risk,
            'supply_chain_grade': self._determine_supply_chain_grade(avg_risk_score),
            'action_plan': self._create_action_plan(assessed_suppliers)
        }
    
    def _simulate_supply_chain(self, industry: str, revenue: float) -> dict:
        """공급망 데이터 시뮬레이션"""
        supply_chain = {}
        
        for category_id in self.scope3_categories.keys():
            # 산업별 가중치
            if industry == "제조업":
                weights = {"purchased_goods": 0.4, "transportation_upstream": 0.2}
            elif industry == "금융업":
                weights = {"investments": 0.6, "business_travel": 0.1}
            else:
                weights = {"purchased_goods": 0.3, "business_travel": 0.2}
            
            weight = weights.get(category_id, 0.05)
            amount = revenue * weight * np.random.uniform(0.8, 1.2)
            
            supply_chain[category_id] = {
                'amount': amount,
                'data_source': 'estimated',
                'quality': 'medium'
            }
        
        return supply_chain
    
    def _simulate_suppliers(self, profile: dict) -> List[dict]:
        """공급업체 리스트 시뮬레이션"""
        suppliers = []
        
        # Tier 1 공급업체
        for i in range(profile['tier1_suppliers']):
            suppliers.append({
                'name': f"Supplier_T1_{i+1}",
                'tier': 1,
                'location': np.random.choice(['Korea', 'China', 'Japan', 'USA', 'EU']),
                'spend': np.random.uniform(50, 500),
                'critical': np.random.random() < 0.2,
                'esg_scores': {
                    'E': np.random.uniform(40, 90),
                    'S': np.random.uniform(40, 90),
                    'G': np.random.uniform(40, 90)
                }
            })
        
        # Tier 2 공급업체 (샘플)
        for i in range(min(50, profile['tier2_suppliers'])):
            suppliers.append({
                'name': f"Supplier_T2_{i+1}",
                'tier': 2,
                'location': np.random.choice(['Korea', 'China', 'Vietnam', 'India']),
                'spend': np.random.uniform(10, 100),
                'critical': np.random.random() < 0.05,
                'esg_scores': {
                    'E': np.random.uniform(30, 80),
                    'S': np.random.uniform(30, 80),
                    'G': np.random.uniform(30, 80)
                }
            })
        
        return suppliers
    
    def _calculate_supplier_risk(self, supplier: dict) -> dict:
        """개별 공급업체 리스크 계산"""
        esg_scores = supplier.get('esg_scores', {})
        
        # ESG 각 영역별 리스크 (100 - 점수)
        e_risk = 100 - esg_scores.get('E', 50)
        s_risk = 100 - esg_scores.get('S', 50)
        g_risk = 100 - esg_scores.get('G', 50)
        
        # Tier별 가중치
        tier_weight = 1.0 if supplier['tier'] == 1 else 0.7
        
        # 지역별 리스크 조정
        location_risk = {
            'Korea': 1.0,
            'Japan': 1.0,
            'USA': 1.1,
            'EU': 1.0,
            'China': 1.3,
            'Vietnam': 1.4,
            'India': 1.5
        }
        location_factor = location_risk.get(supplier.get('location', 'Korea'), 1.2)
        
        # 종합 리스크 점수 (낮을수록 고위험)
        total_score = ((100 - e_risk * 0.35) + 
                      (100 - s_risk * 0.35) + 
                      (100 - g_risk * 0.3)) * tier_weight / location_factor
        
        return {
            'environmental_risk': round(e_risk, 1),
            'social_risk': round(s_risk, 1),
            'governance_risk': round(g_risk, 1),
            'total_score': round(total_score, 1),
            'tier_factor': tier_weight,
            'location_factor': location_factor
        }
    
    def _identify_supplier_improvements(self, risk_scores: dict) -> List[str]:
        """공급업체 개선 필요 영역 식별"""
        improvements = []
        
        if risk_scores['environmental_risk'] > 60:
            improvements.append("환경 관리 시스템 구축 필요")
        if risk_scores['social_risk'] > 60:
            improvements.append("노동/안전 관리 강화 필요")
        if risk_scores['governance_risk'] > 60:
            improvements.append("준법/윤리 체계 개선 필요")
        
        return improvements
    
    def _analyze_concentration_risk(self, suppliers: List[dict]) -> dict:
        """공급망 집중도 리스크 분석"""
        total_spend = sum(s['spend'] for s in suppliers)
        
        # 상위 공급업체 집중도
        sorted_suppliers = sorted(suppliers, key=lambda x: x['spend'], reverse=True)
        top5_spend = sum(s['spend'] for s in sorted_suppliers[:5])
        top10_spend = sum(s['spend'] for s in sorted_suppliers[:10])
        
        concentration_score = 100
        if top5_spend / total_spend > 0.5:
            concentration_score -= 30
        if top10_spend / total_spend > 0.7:
            concentration_score -= 20
        
        return {
            'top5_concentration': round(top5_spend / total_spend * 100, 1),
            'top10_concentration': round(top10_spend / total_spend * 100, 1),
            'concentration_score': concentration_score,
            'risk_level': 'High' if concentration_score < 70 else 'Medium' if concentration_score < 85 else 'Low'
        }
    
    def _analyze_geographic_risk(self, suppliers: List[dict]) -> dict:
        """지역별 리스크 분석"""
        location_counts = {}
        location_spend = {}
        
        for supplier in suppliers:
            location = supplier.get('location', 'Unknown')
            location_counts[location] = location_counts.get(location, 0) + 1
            location_spend[location] = location_spend.get(location, 0) + supplier['spend']
        
        total_spend = sum(location_spend.values())
        
        # 지역별 비중
        geographic_distribution = {
            loc: {
                'count': count,
                'spend_percentage': round(location_spend[loc] / total_spend * 100, 1)
            }
            for loc, count in location_counts.items()
        }
        
        # 다각화 점수
        diversity_score = 100
        max_concentration = max(v['spend_percentage'] for v in geographic_distribution.values())
        if max_concentration > 50:
            diversity_score -= 30
        if len(location_counts) < 3:
            diversity_score -= 20
        
        return {
            'distribution': geographic_distribution,
            'diversity_score': diversity_score,
            'primary_region': max(location_spend, key=location_spend.get),
            'risk_level': 'High' if diversity_score < 70 else 'Medium' if diversity_score < 85 else 'Low'
        }
    
    def _determine_supply_chain_grade(self, avg_score: float) -> str:
        """공급망 등급 결정"""
        if avg_score >= 85:
            return "A"
        elif avg_score >= 75:
            return "B+"
        elif avg_score >= 65:
            return "B"
        elif avg_score >= 55:
            return "B-"
        elif avg_score >= 45:
            return "C"
        else:
            return "D"
    
    def _create_action_plan(self, suppliers: List[dict]) -> List[dict]:
        """공급망 개선 실행 계획"""
        action_items = []
        
        # 고위험 공급업체 대응
        high_risk = [s for s in suppliers if s['risk_level'] == "High"]
        if high_risk:
            action_items.append({
                'priority': 'High',
                'action': '고위험 공급업체 집중 관리',
                'targets': [s['supplier_name'] for s in high_risk[:5]],
                'timeline': '3개월 내',
                'expected_impact': 'Supply chain risk 20% 감소'
            })
        
        # 중요 공급업체 ESG 개선
        critical = [s for s in suppliers if s['critical']]
        if critical:
            action_items.append({
                'priority': 'High',
                'action': '핵심 공급업체 ESG 역량 강화',
                'targets': [s['supplier_name'] for s in critical[:3]],
                'timeline': '6개월 내',
                'expected_impact': 'Critical supplier ESG score 10점 상승'
            })
        
        # 공급망 다각화
        action_items.append({
            'priority': 'Medium',
            'action': '공급망 다각화 전략 수립',
            'targets': ['신규 공급업체 발굴', '지역 다각화'],
            'timeline': '12개월 내',
            'expected_impact': '집중도 리스크 30% 감소'
        })
        
        return action_items
    
    def _estimate_reduction_potential(self, category: str) -> dict:
        """배출량 감축 잠재력 추정"""
        reduction_strategies = {
            "purchased_goods": {
                'potential': 30,
                'strategies': ['저탄소 원재료 전환', '공급업체 협력']
            },
            "transportation_upstream": {
                'potential': 25,
                'strategies': ['물류 최적화', '친환경 운송수단']
            },
            "product_use": {
                'potential': 40,
                'strategies': ['제품 효율 개선', '사용자 교육']
            },
            "investments": {
                'potential': 35,
                'strategies': ['ESG 투자 확대', '탈탄소 포트폴리오']
            }
        }
        
        return reduction_strategies.get(category, {
            'potential': 20,
            'strategies': ['일반 개선 활동']
        })
    
    def _assess_data_quality(self, data: dict) -> dict:
        """데이터 품질 평가"""
        quality_scores = {
            'primary_data': 30,  # 실제 측정 데이터 비율
            'estimated_data': 50,  # 추정 데이터 비율
            'proxy_data': 20  # 대리 데이터 비율
        }
        
        overall_quality = "Medium"
        if quality_scores['primary_data'] > 60:
            overall_quality = "High"
        elif quality_scores['primary_data'] < 20:
            overall_quality = "Low"
        
        return {
            'overall_quality': overall_quality,
            'data_composition': quality_scores,
            'improvement_needed': overall_quality != "High"
        }
    
    def _generate_scope3_recommendations(self, hotspots: List[dict]) -> List[dict]:
        """Scope 3 감축 권고사항 생성"""
        recommendations = []
        
        for hotspot in hotspots[:3]:
            if hotspot['category'] == "구매한 제품 및 서비스":
                recommendations.append({
                    'category': hotspot['category'],
                    'action': '공급업체 협력 프로그램',
                    'description': '주요 공급업체와 탄소감축 파트너십 구축',
                    'potential_reduction': f"{hotspot['reduction_potential']['potential']}%",
                    'implementation': '6-12개월'
                })
            elif hotspot['category'] == "운송 및 유통(상류)":
                recommendations.append({
                    'category': hotspot['category'],
                    'action': '물류 최적화',
                    'description': '운송 경로 최적화 및 친환경 운송수단 전환',
                    'potential_reduction': f"{hotspot['reduction_potential']['potential']}%",
                    'implementation': '3-6개월'
                })
            elif hotspot['category'] == "판매 제품 사용":
                recommendations.append({
                    'category': hotspot['category'],
                    'action': '제품 효율 개선',
                    'description': '에너지 효율 제품 개발 및 사용자 교육',
                    'potential_reduction': f"{hotspot['reduction_potential']['potential']}%",
                    'implementation': '12-24개월'
                })
            else:
                recommendations.append({
                    'category': hotspot['category'],
                    'action': '배출량 감축 프로그램',
                    'description': '카테고리별 맞춤 감축 전략 수립',
                    'potential_reduction': '20%',
                    'implementation': '6-12개월'
                })
        
        return recommendations
    
    def create_supplier_engagement_program(self, company_data: dict, 
                                          target_suppliers: List[dict]) -> dict:
        """공급업체 협력 프로그램 설계
        
        Args:
            company_data: 기업 정보
            target_suppliers: 대상 공급업체 리스트
        
        Returns:
            협력 프로그램 상세
        """
        program_tiers = {
            'platinum': {
                'criteria': 'ESG Score > 80',
                'benefits': [
                    '장기 계약 보장',
                    '조기 대금 지급',
                    'ESG 인증 비용 지원',
                    '기술 개발 협력'
                ],
                'requirements': [
                    'CDP 공시 참여',
                    '탄소중립 로드맵 수립',
                    '연간 ESG 보고서 제출'
                ]
            },
            'gold': {
                'criteria': 'ESG Score 60-80',
                'benefits': [
                    '우선 공급업체 지위',
                    'ESG 교육 프로그램 제공',
                    '개선 컨설팅 지원'
                ],
                'requirements': [
                    'ESG 자가진단 실시',
                    '개선 계획 수립',
                    '분기별 진도 보고'
                ]
            },
            'silver': {
                'criteria': 'ESG Score < 60',
                'benefits': [
                    'ESG 역량 구축 지원',
                    '기초 교육 제공',
                    '멘토링 프로그램'
                ],
                'requirements': [
                    'ESG 개선 의지 표명',
                    '기초 평가 참여',
                    '개선 목표 설정'
                ]
            }
        }
        
        # 공급업체 분류
        classified_suppliers = {
            'platinum': [],
            'gold': [],
            'silver': []
        }
        
        for supplier in target_suppliers:
            avg_score = np.mean([
                supplier.get('esg_scores', {}).get('E', 50),
                supplier.get('esg_scores', {}).get('S', 50),
                supplier.get('esg_scores', {}).get('G', 50)
            ])
            
            if avg_score > 80:
                classified_suppliers['platinum'].append(supplier['name'])
            elif avg_score > 60:
                classified_suppliers['gold'].append(supplier['name'])
            else:
                classified_suppliers['silver'].append(supplier['name'])
        
        # 프로그램 KPI
        program_kpis = [
            {
                'metric': '참여 공급업체 수',
                'target': len(target_suppliers),
                'timeline': '1년'
            },
            {
                'metric': '평균 ESG 점수 향상',
                'target': '10점',
                'timeline': '2년'
            },
            {
                'metric': 'Scope 3 배출량 감축',
                'target': '15%',
                'timeline': '3년'
            },
            {
                'metric': 'ESG 인증 취득률',
                'target': '50%',
                'timeline': '2년'
            }
        ]
        
        # 예산 및 ROI
        program_budget = len(target_suppliers) * 0.5  # 억원
        expected_benefits = {
            'risk_reduction': '공급망 리스크 30% 감소',
            'cost_savings': f'연간 {program_budget * 0.3:.1f}억원 절감',
            'reputation': 'ESG 평가 등급 상승',
            'compliance': '규제 대응력 강화'
        }
        
        return {
            'program_name': 'Supply Chain ESG Excellence Program',
            'launch_date': datetime.now().strftime("%Y-%m-%d"),
            'duration': '3년',
            'tiers': program_tiers,
            'supplier_classification': classified_suppliers,
            'total_suppliers': len(target_suppliers),
            'program_kpis': program_kpis,
            'budget': f'{program_budget:.1f}억원',
            'expected_roi': '150%',
            'expected_benefits': expected_benefits,
            'implementation_phases': [
                {
                    'phase': 1,
                    'name': '프로그램 설계 및 파일럿',
                    'duration': '3개월',
                    'activities': ['공급업체 평가', '프로그램 설계', '파일럿 운영']
                },
                {
                    'phase': 2,
                    'name': '전면 시행',
                    'duration': '9개월',
                    'activities': ['전체 공급업체 참여', '교육 프로그램 운영', '개선 지원']
                },
                {
                    'phase': 3,
                    'name': '고도화 및 확산',
                    'duration': '24개월',
                    'activities': ['성과 모니터링', '우수사례 확산', '2차 공급업체 확대']
                }
            ]
        }
    
    def analyze_supply_chain_resilience(self, supply_chain_data: dict) -> dict:
        """공급망 회복탄력성 분석
        
        Args:
            supply_chain_data: 공급망 데이터
        
        Returns:
            회복탄력성 평가 결과
        """
        resilience_factors = {
            'diversification': {
                'score': 0,
                'weight': 0.25,
                'status': ''
            },
            'flexibility': {
                'score': 0,
                'weight': 0.20,
                'status': ''
            },
            'visibility': {
                'score': 0,
                'weight': 0.20,
                'status': ''
            },
            'collaboration': {
                'score': 0,
                'weight': 0.20,
                'status': ''
            },
            'risk_management': {
                'score': 0,
                'weight': 0.15,
                'status': ''
            }
        }
        
        # 다각화 평가
        supplier_count = supply_chain_data.get('total_suppliers', 50)
        geographic_diversity = len(supply_chain_data.get('regions', ['Korea', 'China', 'Japan']))
        
        if supplier_count > 100 and geographic_diversity > 5:
            resilience_factors['diversification']['score'] = 90
            resilience_factors['diversification']['status'] = 'Excellent'
        elif supplier_count > 50 and geographic_diversity > 3:
            resilience_factors['diversification']['score'] = 70
            resilience_factors['diversification']['status'] = 'Good'
        else:
            resilience_factors['diversification']['score'] = 50
            resilience_factors['diversification']['status'] = 'Needs Improvement'
        
        # 유연성 평가
        dual_sourcing_ratio = supply_chain_data.get('dual_sourcing_ratio', 0.3)
        resilience_factors['flexibility']['score'] = min(100, dual_sourcing_ratio * 200)
        resilience_factors['flexibility']['status'] = 'Good' if dual_sourcing_ratio > 0.4 else 'Moderate'
        
        # 가시성 평가
        digital_integration = supply_chain_data.get('digital_integration', 0.5)
        resilience_factors['visibility']['score'] = digital_integration * 100
        resilience_factors['visibility']['status'] = 'High' if digital_integration > 0.7 else 'Medium'
        
        # 협업 평가
        partnership_score = supply_chain_data.get('partnership_score', 60)
        resilience_factors['collaboration']['score'] = partnership_score
        resilience_factors['collaboration']['status'] = 'Strong' if partnership_score > 75 else 'Developing'
        
        # 리스크 관리 평가
        risk_protocols = supply_chain_data.get('risk_protocols', 3)
        resilience_factors['risk_management']['score'] = min(100, risk_protocols * 20)
        resilience_factors['risk_management']['status'] = 'Robust' if risk_protocols > 4 else 'Basic'
        
        # 종합 점수 계산
        total_score = sum(
            factor['score'] * factor['weight'] 
            for factor in resilience_factors.values()
        )
        
        # 회복탄력성 등급
        if total_score >= 80:
            resilience_grade = 'A'
            resilience_level = 'High'
        elif total_score >= 60:
            resilience_grade = 'B'
            resilience_level = 'Moderate'
        else:
            resilience_grade = 'C'
            resilience_level = 'Low'
        
        # 개선 권고사항
        improvements = []
        for factor_name, factor_data in resilience_factors.items():
            if factor_data['score'] < 70:
                improvements.append({
                    'area': factor_name.replace('_', ' ').title(),
                    'current_score': factor_data['score'],
                    'target_score': 80,
                    'priority': 'High' if factor_data['weight'] > 0.2 else 'Medium'
                })
        
        return {
            'assessment_date': datetime.now().isoformat(),
            'resilience_score': round(total_score, 1),
            'resilience_grade': resilience_grade,
            'resilience_level': resilience_level,
            'factor_scores': resilience_factors,
            'strengths': [k for k, v in resilience_factors.items() if v['score'] >= 80],
            'weaknesses': [k for k, v in resilience_factors.items() if v['score'] < 60],
            'improvement_areas': improvements,
            'crisis_readiness': {
                'pandemic': 'Prepared' if total_score > 70 else 'Vulnerable',
                'climate_events': 'Resilient' if resilience_factors['diversification']['score'] > 70 else 'At Risk',
                'geopolitical': 'Adaptive' if resilience_factors['flexibility']['score'] > 70 else 'Exposed'
            }
        }