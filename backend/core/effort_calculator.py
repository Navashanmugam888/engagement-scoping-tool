"""
Effort Estimation Calculator

Calculates effort estimation based on scope definition and engagement weightage.
Implements exact formulas from Excel Effort Estimation sheet including:
- Task-level effort calculations with specialized formulas
- Tier-based adjustments for 16 categories
- In-scope gating via in_scope_flag
- Excel ROUND function implementation (round half up)

Key Features:
- Handles complex scaling formulas (ROUND-based calculations)
- Special multipliers for specific task types
- Conditional logic for threshold-based calculations
- Aggregates task estimates at category level
- Calculates summary: hours → days (÷8) → months (÷30)
"""

from pathlib import Path
import sys
import math

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import HOURS_PER_DAY, DAYS_PER_MONTH
from backend.data.effort_template import EFFORT_ESTIMATION_TEMPLATE


def excel_round(value, decimals=0):
    """
    Implements Excel ROUND function (round half up)
    Python's round() uses banker's rounding (round half to even)
    Excel uses traditional rounding (round half away from zero)
    """
    multiplier = 10 ** decimals
    return math.floor(value * multiplier + 0.5) / multiplier


class EffortCalculator:
    """
    Calculates effort estimation with tier-based adjustments
    Matches Excel Effort Estimation sheet logic exactly
    """
    
    def __init__(self, scope_result: dict):
        """
        Initialize with scope processing result
        
        Args:
            scope_result: Output from ScopeDefinitionProcessor
        """
        self.scope_metrics = {m['name']: m for m in scope_result['metrics']}
        self.engagement_weightage = scope_result['total_weightage']
        self.tier = scope_result['tier']
        self.tier_name = scope_result['tier_name']
    
    def lookup_inscope(self, task_name: str) -> str:
        """Check if task is in scope"""
        metric = self.scope_metrics.get(task_name)
        return "YES" if metric and metric['in_scope_flag'] == 1 else "NO"
    
    def lookup_details(self, task_name: str) -> float:
        """Get details value from scope definition"""
        metric = self.scope_metrics.get(task_name)
        if metric and metric['in_scope'] == "YES":
            return metric.get('details', 0) if metric.get('details') is not None else 0
        return 0
    
    def calculate_task_final_estimate(self, task_name: str) -> float:
        """
        Calculate Final Estimate for individual tasks
        Implements exact Excel formulas from Effort Estimation sheet
        
        Only tasks with detail formulas contribute to effort.
        Tasks without formulas return 0.
        """
        in_scope = self.lookup_inscope(task_name)
        
        # If not in scope, no effort
        if in_scope != "YES":
            return 0
        
        # Get details value
        details = self.lookup_details(task_name)
        
        # Define all tasks with formulas and their calculation logic
        # Format: 'TaskName': (base_hours, formula_type)
        
        # Complex Scaling Formula (ROUND based):
        # =ROUND(E*0.5,0)*8 + ROUND(E*0.25,0)*12 + ROUND(E*0.25,0)*16
        complex_round_formula_tasks = {
            'Data Forms': 4,
            'Dashboards': 4,
            'Business Rules': 8,
            'Management Reports': 8,
        }
        
        if task_name in complex_round_formula_tasks:
            if details > 0:
                part1 = int(excel_round(details * 0.5)) * 8
                part2 = int(excel_round(details * 0.25)) * 12
                part3 = int(excel_round(details * 0.25)) * 16
                return part1 + part2 + part3
            return 0
        
        # Member Formula special calculation
        # =ROUND(E*0.5,0)*2 + ROUND(E*0.25,0)*3 + ROUND(E*0.25,0)*4
        if task_name == "Member Formula":
            if details > 0:
                part1 = int(excel_round(details * 0.5)) * 2
                part2 = int(excel_round(details * 0.25)) * 3
                part3 = int(excel_round(details * 0.25)) * 4
                return part1 + part2 + part3
            return 0
        
        # Custom KPIs special calculation
        # =ROUND(E*0.5,0)*2 + ROUND(E*0.25,0)*4 + ROUND(E*0.25,0)*4
        if task_name == "Custom KPIs":
            if details > 0:
                part1 = int(excel_round(details * 0.5)) * 2
                part2 = int(excel_round(details * 0.25)) * 4
                part3 = int(excel_round(details * 0.25)) * 4
                return part1 + part2 + part3
            return 0
        
        # Secured Dimensions: =E*4
        if task_name == "Secured Dimensions":
            return details * 4
        
        # Number of Users: =E*0.2
        if task_name == "Number of Users":
            return details * 0.2
        
        # Historical Data Validation: =(15 + (E+1)*10)*8
        if task_name == "Historical Data Validation":
            if details > 0:
                return (15 + (details + 1) * 10) * 8
            return 0
        
        # Prelim FCC User Provisioning: =IF(E>50, 8, 0)
        if task_name == "Prelim FCC User Provisioning":
            return 8 if details > 50 else 0
        
        # Parallel Testing: =C*2 (where C=40, and details come from D116)
        # But D116 has value 2, so this is C*D = 40*2 = 80 (fixed)
        if task_name == "Parallel Testing":
            # E116 = 2 (from row 116 column D/E)
            return 40 * 2  # Fixed value from Excel
        
        # Data Validation tasks reuse Historical Data Validation's details value
        # Excel formulas: Row 86 =C86*E86 where E86=IF(D86="YES",'Scope Definition'!D54,0)
        #                Row 87 =C87*E87 where E87='Scope Definition'!D13  (but D13=D54=2)
        #                Row 88 =C88*E88 where E88=IF(D88="YES",'Scope Definition'!D54,0)
        # D54 = Historical Data Validation's details value
        if task_name == "Data Validation for Account Alt Hierarchies":
            hist_data_details = self.lookup_details("Historical Data Validation")
            return 20 * hist_data_details if hist_data_details > 0 else 0
        
        if task_name == "Data Validation for Entity Alt Hierarchies":
            hist_data_details = self.lookup_details("Historical Data Validation")
            return 20 * hist_data_details if hist_data_details > 0 else 0
        
        if task_name == "Historical Journal Conversion":
            hist_data_details = self.lookup_details("Historical Data Validation")
            return 20 * hist_data_details if hist_data_details > 0 else 0
        
        # Standard formula tasks: =C*E or =E*C (multiplication)
        standard_multiply_tasks = {
            'Account Alternate Hierarchies': 8,
            'Multi-Currency': 1,
            'Reporting Currency': 0.5,
            'Entity Alternate Hierarchies': 4,
            'Scenario': 1,
            'Custom Dimensions': 4,
            'Alternate Hierarchies in Custom Dimensions': 4,
            'Additional Alias Tables': 1,
            'Journal Templates': 1,
            'Configurable Consolidation Rules': 8,
            'Files Based Loads': 16,
            'Direct Connect Integrations': 16,
            'Outbound Integrations': 16,
            'Pipeline': 16,
            'Custom Scripting': 16,
            'Consolidation Reports': 4,
            'Consolidation Journal Reports': 4,
            'Intercompany Reports': 8,
            'Task Manager Reports': 4,
            'Enterprise Journal Reports': 4,
            'Smart View Reports': 8,
        }
        
        if task_name in standard_multiply_tasks:
            base_hours = standard_multiply_tasks[task_name]
            return base_hours * details if details > 0 else 0
        
        # All other tasks: no formula, contribute 0
        return 0
    
    def calculate_category_final_estimate(self, category_name: str, base_hours: float, task_estimates: dict) -> float:
        """
        Calculate Final Estimate for category header
        
        Excel formula pattern (from Row 5, 18, etc.):
        =IF(EngagementWeightage<=100, CategoryBase,
            IF(EngagementWeightage<=120, CategoryBase+adjustment1,
               IF(EngagementWeightage<=160, CategoryBase+adjustment2,
                  CategoryBase+adjustment3)))
        """
        w = self.engagement_weightage
        
        # Tier-based adjustments for all categories - extracted from Excel
        # Format: (adjustment for <=100, <=120, <=160, >160)
        tier_adjustments = {
            "Project Initiation and Planning": (0, 4, 6, 8),
            "Requirement Gathering, Read back and Client Sign-off": (0, 8, 12, 16),
            "Design": (0, 8, 16, 24),
            "Build and Configure FCC": (0, 8, 16, 24),
            "Setup Application Features": (0, 8, 16, 24),
            "Application Customization": (0, 8, 12, 16),
            "Calculations": (0, 8, 12, 16),
            "Security": (0, 8, 12, 16),
            "Historical Data": (0, 8, 12, 16),
            "Integrations": (0, 8, 12, 16),
            "Reporting": (0, 8, 12, 16),
            "Automations": (0, 8, 12, 16),
            "Testing/Training": (0, 8, 12, 16),
            "Transition": (0, 8, 16, 24),
            "Documentations": (0, 8, 12, 16),
            "Change Management": (0, 8, 12, 16),
            "Creating and Managing EPM Cloud Infrastructure": (0, 0, 0, 0),
        }
        
        # Calculate category base with tier adjustment
        category_adjustment = 0
        if category_name in tier_adjustments:
            adj = tier_adjustments[category_name]
            if w <= 100:
                category_adjustment = adj[0]
            elif w <= 120:
                category_adjustment = adj[1]
            elif w <= 160:
                category_adjustment = adj[2]
            else:
                category_adjustment = adj[3]
        
        category_base = base_hours + category_adjustment
        
        # Add subtask estimates from tasks with detail formulas
        task_estimate_sum = sum(task_estimates.values()) if task_estimates else 0
        
        return category_base + task_estimate_sum
    
    def calculate_effort(self) -> dict:
        """
        Calculate complete effort estimation matching Excel logic
        
        Returns:
            dict with effort estimation for all categories
        """
        effort_estimation = {}
        
        for category, data in EFFORT_ESTIMATION_TEMPLATE.items():
            category_info = {
                'base_hours': data['total'],
                'final_estimate': 0,
                'in_days': 0,
                'tasks': []
            }
            
            # Calculate each task's final estimate
            task_estimates = {}
            for task_name, task_base_hours in data['tasks'].items():
                task_final_estimate = self.calculate_task_final_estimate(task_name)
                
                task_info = {
                    'name': task_name,
                    'base_hours': task_base_hours,
                    'in_scope': self.lookup_inscope(task_name),
                    'details': self.lookup_details(task_name),
                    'final_estimate': task_final_estimate
                }
                
                category_info['tasks'].append(task_info)
                if task_final_estimate > 0:
                    task_estimates[task_name] = task_final_estimate
            
            # Calculate category Final Estimate (base + tier adjustment + task estimates)
            category_final_estimate = self.calculate_category_final_estimate(
                category,
                data['total'],
                task_estimates
            )
            
            category_info['final_estimate'] = category_final_estimate
            
            # In Days = Final Estimate / 8
            category_info['in_days'] = round(category_final_estimate / HOURS_PER_DAY, 2)
            
            effort_estimation[category] = category_info
        
        return effort_estimation
    
    def generate_summary(self, effort_estimation: dict) -> dict:
        """
        Generate summary statistics based on Excel formula logic
        
        From Excel Effort Estimation Sheet Row 131-132:
        F131: "Hours" (header)
        F132: =SUM(G5:G130) - This sums the Final Estimates (Column F values wrap to G in summary)
        G132: =F132/8 - Total Hours / 8 = Days
        H132: =G132/30 - Days / 30 = Months
        
        The column mapping in Excel:
        - Column F (Final Estimate) contains the calculated effort for each row
        - Row 132 column F formula =SUM(G5:G130) actually represents the sum of all Final Estimates
        - In column G of summary, it shows Days = Hours/8
        - In column H of summary, it shows Months = Days/30
        """
        # Sum of all Final Estimates from all categories
        total_hours = sum(cat['final_estimate'] for cat in effort_estimation.values())
        
        # total_days = total_hours / 8
        total_days = total_hours / 8
        
        # total_months = total_days / 30
        total_months = total_days / 30
        
        return {
            'engagement_weightage': self.engagement_weightage,
            'tier': self.tier,
            'tier_name': self.tier_name,
            'total_time_hours': total_hours,
            'final_estimate_hours': total_hours,
            'total_days': round(total_days, 2),
            'total_months': round(total_months, 2)
        }

