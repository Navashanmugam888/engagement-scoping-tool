"""
Formula Evaluation Engine
Evaluates Excel-like formulas with FeatureName[Column] syntax
"""

import re
from typing import Dict, Any, List


class FormulaEvaluator:
    """Evaluates Excel formulas with FeatureName[Column] syntax"""
    
    def __init__(self, metrics_data: List[Dict[str, Any]]):
        """
        Initialize with metrics data
        
        Args:
            metrics_data: List of metric dictionaries with 'name', 'in_scope', 'details'
        """
        self.metrics_lookup = {m['name']: m for m in metrics_data}
    
    def evaluate(self, formula: str) -> float:
        """
        Evaluate a formula and return the result
        
        Args:
            formula: Formula string like "=IF(Account[InScope]="YES",2,0)"
        
        Returns:
            Calculated numeric value
        """
        if not formula:
            return 0
        
        # Remove leading '='
        if formula.startswith('='):
            formula = formula[1:]
        
        # Replace all FeatureName[Column] references with actual values
        formula_with_values = self._replace_references(formula)
        
        # Evaluate the formula
        try:
            result = self._safe_eval(formula_with_values)
            return float(result) if result != "" else 0
        except Exception as e:
            print(f"Error evaluating formula: {e}")
            print(f"  Original: {formula[:100]}")
            print(f"  Replaced: {formula_with_values[:100]}")
            return 0
    
    def _replace_references(self, formula: str) -> str:
        """Replace all FeatureName[Column] with actual values"""
        pattern = r'([A-Za-z][\w\s\-\.]*?)\[(InScope|Details)\]'
        
        def replacer(match):
            feature_name = match.group(1).strip()
            column_name = match.group(2)
            
            metric = self.metrics_lookup.get(feature_name)
            
            if metric:
                if column_name == 'InScope':
                    value = metric.get('in_scope', 'NO')
                    return f'"{value}"'
                elif column_name == 'Details':
                    value = metric.get('details', 0)
                    return str(value if value is not None else 0)
            
            return '"NO"' if column_name == 'InScope' else '0'
        
        return re.sub(pattern, replacer, formula)
    
    def _safe_eval(self, expression: str) -> Any:
        """Safely evaluate the expression"""
        # Convert Excel = to Python ==
        expression = re.sub(r'([^<>!])=([^=])', r'\1==\2', expression)
        
        # Create safe namespace with Excel function equivalents
        namespace = {
            'IF': self._if,
            'AND': self._and,
            'OR': self._or,
            'SUM': sum,
            'IFS': self._ifs,
            'TRUE': True,
            '__builtins__': {}
        }
        
        return eval(expression, namespace, {})
    
    def _if(self, condition, true_val, false_val):
        """Excel IF function"""
        return true_val if condition else false_val
    
    def _and(self, *args):
        """Excel AND function"""
        return all(args)
    
    def _or(self, *args):
        """Excel OR function"""
        return any(args)
    
    def _ifs(self, *args):
        """Excel IFS function - evaluates condition/value pairs"""
        for i in range(0, len(args), 2):
            if i + 1 < len(args):
                condition = args[i]
                value = args[i + 1]
                if condition:
                    return value
        return 0
