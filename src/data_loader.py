"""
데이터 로더 유틸리티
"""
import json
import os
from typing import Dict, List, Optional

class DataLoader:
    """데이터 로드 및 관리"""
    
    def __init__(self, data_path: str = "data"):
        """초기화
        
        Args:
            data_path: 데이터 파일 경로
        """
        self.data_path = data_path
        self.enterprises_data = None
        self.benchmarks = None
        self._load_data()
    
    def _load_data(self):
        """데이터 파일 로드"""
        try:
            # 샘플 기업 데이터 로드
            enterprises_file = os.path.join(self.data_path, 'sample_enterprises.json')
            if os.path.exists(enterprises_file):
                with open(enterprises_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.enterprises_data = data.get('enterprises', {})
                    self.benchmarks = data.get('industry_benchmarks', {})
                    print(f"✅ 데이터 로드 완료: {len(self.enterprises_data)}개 기업")
            else:
                print(f"⚠️ 데이터 파일을 찾을 수 없습니다: {enterprises_file}")
                self._create_default_data()
                
        except Exception as e:
            print(f"❌ 데이터 로드 중 오류: {str(e)}")
            self._create_default_data()
    
    def _create_default_data(self):
        """기본 데이터 생성"""
        self.enterprises_data = {
            "테스트기업": {
                "basic_info": {
                    "name": "테스트기업",
                    "industry": "제조업",
                    "asset_size": 1000000,
                    "employee_count": 10000
                },
                "environmental": {
                    "carbon_scope1": 1000,
                    "carbon_scope2": 500,
                    "carbon_scope3": 5000,
                    "renewable_energy_ratio": 0.3
                },
                "social": {
                    "diversity_ratio": 0.3,
                    "accident_rate": 0.1,
                    "customer_satisfaction": 80
                },
                "governance": {
                    "independent_director_ratio": 0.5,
                    "has_esg_committee": True,
                    "ethics_violations": 0
                },
                "financial": {
                    "target_loan_amount": 1000
                },
                "compliance": {
                    "k_taxonomy_compliant": True,
                    "tcfd_compliant": False,
                    "gri_compliant": True
                }
            }
        }
        
        self.benchmarks = {
            "제조업": {
                "avg_carbon_intensity": 10000,
                "avg_renewable_ratio": 0.3,
                "avg_accident_rate": 0.15,
                "avg_esg_score": 72
            }
        }
    
    def get_enterprise_list(self) -> List[str]:
        """기업 목록 반환"""
        return list(self.enterprises_data.keys())
    
    def get_enterprise_data(self, enterprise_name: str) -> Optional[Dict]:
        """특정 기업 데이터 반환"""
        return self.enterprises_data.get(enterprise_name)
    
    def get_industry_benchmark(self, industry: str) -> Optional[Dict]:
        """업종별 벤치마크 반환"""
        return self.benchmarks.get(industry)
    
    def get_all_industries(self) -> List[str]:
        """모든 업종 목록 반환"""
        industries = set()
        for enterprise in self.enterprises_data.values():
            industry = enterprise.get('basic_info', {}).get('industry')
            if industry:
                industries.add(industry)
        return sorted(list(industries))
    
    def add_historical_data(self, enterprise_name: str) -> Dict:
        """과거 데이터 시뮬레이션 추가"""
        import numpy as np
        
        # 최근 12개월 데이터 시뮬레이션
        current_data = self.get_enterprise_data(enterprise_name)
        if not current_data:
            return {}
        
        # 현재 데이터를 기준으로 과거 데이터 생성
        historical_scores = []
        base_score = 70  # 시작 점수
        
        for i in range(12):
            # 점진적 개선 시뮬레이션
            score = base_score + i * np.random.uniform(0.5, 1.5)
            score = min(100, max(0, score + np.random.normal(0, 2)))
            historical_scores.append(round(score, 1))
        
        return {
            "historical_scores": historical_scores,
            "trend": "improving" if historical_scores[-1] > historical_scores[0] else "declining"
        }