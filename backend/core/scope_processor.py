"""
Scope Definition Processor

Processes user input and calculates engagement weightage for FCC implementation scoping.

Key Responsibilities:
1. Load metrics from Excel Scope Definition sheet (71 metrics)
2. Process user inputs: in_scope (YES/NO) and details (numeric value)
3. Set in_scope_flag (1/0) - critical gate for effort calculation
4. Evaluate weightage formulas for each metric using FormulaEvaluator
5. Calculate total engagement weightage (sum of all metric weightages)
6. Determine implementation tier based on weightage range

Critical Detail:
- in_scope_flag = 1 when in_scope == "YES", else 0
- Effort calculator uses in_scope_flag to gate all effort contributions
- When flag=0, no effort is calculated regardless of details value

Formula Evaluation:
- Formulas use FeatureName[InScope] and FeatureName[Details] syntax
- FormulaEvaluator replaces these with actual values before evaluation
- Supports IF, AND, OR, SUM, IFS Excel functions
"""

from pathlib import Path
import pandas as pd
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import AVAILABLE_ROLES, TIERS
from backend.utils.formula_evaluator import FormulaEvaluator
from backend.data.excel_templates import METRICS_TEMPLATE


class ScopeDefinitionProcessor:
    """
    Processes scope definition inputs and calculates engagement weightage
    """
    
    def __init__(self):
        self.metrics = []
        self.formulas = {}
        self.roles = AVAILABLE_ROLES
        
        # Load data
        self._load_metrics()
        self._load_formulas()
        
        print(f"Loaded {len(self.metrics)} metrics from Scope Definition (excluding section headings)")
        print(f"Loaded {len(self.formulas)} formulas")
        print(f"Loaded {len(self.roles)} available roles")
    
    def _load_metrics(self):
        """Load all metrics from template (previously from Excel Scope Definition sheet)"""
        # Use hardcoded metrics template instead of reading from Excel
        for metric_def in METRICS_TEMPLATE:
            self.metrics.append({
                'row': metric_def['row'],
                'name': metric_def['name'],
                'in_scope': None,
                'details': None,
                'weightage': 0,
                'feature_clean': metric_def['name'],
                'in_scope_flag': 0,
                'is_details_required': metric_def['is_details_required'],
                'is_sub_question': metric_def['is_sub_question']
            })
    
    def _load_formulas(self):
        """Load formulas from CSV files"""
        # Load main formulas
        main_csv = Path(__file__).parent.parent / 'data' / 'formulas_expanded.csv'
        if main_csv.exists():
            df = pd.read_csv(main_csv)
            for _, row in df.iterrows():
                self.formulas[row['Metric']] = row['Formula']
        
        # Load supplemental array formulas
        array_csv = Path(__file__).parent.parent / 'data' / 'formulas_array_supplement.csv'
        if array_csv.exists():
            df_array = pd.read_csv(array_csv)
            for _, row in df_array.iterrows():
                self.formulas[row['Metric']] = row['Formula']
            print(f"Loaded {len(df_array)} additional formulas from array supplement")
    
    def process_user_input(self, user_input: dict) -> dict:
        """
        Process user input and calculate weightage
        
        Args:
            user_input: {
                'scope_inputs': [{'name': str, 'in_scope': str, 'details': number}, ...],
                'selected_roles': [str, ...]
            }
        
        Returns:
            dict with metrics, weightage, tier, and summary
        """
        # Map user inputs to metrics
        scope_inputs_dict = {item['name']: item for item in user_input['scope_inputs']}
        
        for metric in self.metrics:
            user_data = scope_inputs_dict.get(metric['name'], {})
            metric['in_scope'] = user_data.get('in_scope', 'NO')
            metric['details'] = user_data.get('details', 0)
            metric['in_scope_flag'] = 1 if metric['in_scope'] == 'YES' else 0
        
        # Evaluate formulas to calculate weightage
        evaluator = FormulaEvaluator(self.metrics)
        
        for metric in self.metrics:
            formula = self.formulas.get(metric['name'], '')
            if formula:
                metric['weightage'] = evaluator.evaluate(formula)
                metric['formula'] = formula
            else:
                metric['formula'] = ''
        
        # Calculate total weightage
        total_weightage = sum(m['weightage'] for m in self.metrics)
        
        # Determine tier
        tier = self._determine_tier(total_weightage)
        tier_info = TIERS[tier]
        
        # Summary
        in_scope_count = sum(1 for m in self.metrics if m['in_scope_flag'] == 1)
        out_scope_count = len(self.metrics) - in_scope_count
        
        return {
            'total_weightage': total_weightage,
            'tier': tier,
            'tier_name': tier_info['name'],
            'tier_range': tier_info['range'],
            'metrics': self.metrics,
            'selected_roles': user_input.get('selected_roles', []),
            'summary': {
                'total_metrics': len(self.metrics),
                'in_scope_count': in_scope_count,
                'out_scope_count': out_scope_count
            }
        }
    
    def _determine_tier(self, weightage: float) -> int:
        """Determine implementation tier based on weightage"""
        for tier, info in TIERS.items():
            min_val, max_val = info['range']
            if min_val <= weightage <= max_val:
                return tier
        return 5  # Default to highest tier
