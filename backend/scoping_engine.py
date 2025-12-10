"""
FCC Scoping Tool - Main Backend Engine
Orchestrates the complete scoping and effort estimation workflow
"""

import json
from pathlib import Path
from datetime import datetime

from backend.core.scope_processor import ScopeDefinitionProcessor
from backend.core.effort_calculator import EffortCalculator
from backend.core.fte_calculator import FTEEffortsCalculator
from backend.core.sow_report_generator import SOWReportGenerator
from backend.config import OUTPUT_DIR


class ScopingEngine:
    """
    Main engine that orchestrates the complete scoping workflow:
    1. Process scope definition inputs
    2. Calculate engagement weightage
    3. Determine implementation tier
    4. Calculate effort estimation
    5. Generate reports
    """
    
    def __init__(self):
        self.scope_processor = ScopeDefinitionProcessor()
        self.fte_calculator = FTEEffortsCalculator()
        self.scope_result = None
        self.effort_result = None
        self.fte_result = None
        self.scope_inputs_dict = None
    
    def process_scope(self, user_input: dict) -> dict:
        """
        Process scope definition
        
        Args:
            user_input: {
                'scope_inputs': [
                    {'name': 'Account', 'in_scope': 'YES', 'details': 2000},
                    ...
                ],
                'selected_roles': ['PM USA', 'PM India', ...]
            }
        
        Returns:
            Scope processing result with weightage and tier
        """
        print("\n" + "="*80)
        print("STEP 1: PROCESSING SCOPE DEFINITION")
        print("="*80)
        
        # Store scope_inputs_dict for report generation
        scope_inputs_list = user_input.get('scope_inputs', [])
        self.scope_inputs_dict = {item['name']: item for item in scope_inputs_list}
        
        self.scope_result = self.scope_processor.process_user_input(user_input)
        
        print(f"\n✓ Scope processing complete")
        print(f"  Total Weightage: {self.scope_result['total_weightage']}")
        print(f"  Implementation Tier: {self.scope_result['tier']} - {self.scope_result['tier_name']}")
        print(f"  Metrics In Scope: {self.scope_result['summary']['in_scope_count']}/{self.scope_result['summary']['total_metrics']}")
        print(f"  Selected Roles: {len(self.scope_result['selected_roles'])}")
        
        return self.scope_result
    
    def calculate_effort(self) -> dict:
        """
        Calculate effort estimation based on scope result
        
        Returns:
            Effort estimation with hours, days, months
        """
        if not self.scope_result:
            raise ValueError("Must process scope first before calculating effort")
        
        print("\n" + "="*80)
        print("STEP 2: CALCULATING EFFORT ESTIMATION")
        print("="*80)
        
        calculator = EffortCalculator(self.scope_result)
        effort_estimation = calculator.calculate_effort()
        summary = calculator.generate_summary(effort_estimation)
        
        self.effort_result = {
            'summary': summary,
            'categories': effort_estimation
        }
        
        print(f"\n✓ Effort calculation complete")
        print(f"  Total Time: {summary['total_time_hours']} hours")
        print(f"  Final Estimate: {summary['final_estimate_hours']} hours")
        print(f"  Duration: {summary['total_days']} days ({summary['total_months']} months)")
        
        return self.effort_result
    
    def calculate_fte_allocation(self) -> dict:
        """
        Calculate FTE allocation by role
        
        Returns:
            FTE allocation with hours for each selected role
        """
        if not self.scope_result or not self.effort_result:
            raise ValueError("Must process scope and calculate effort first")
        
        print("\n" + "="*80)
        print("STEP 3: CALCULATE FTE ALLOCATION BY ROLE (SUMPRODUCT)")
        print("="*80)
        
        selected_roles = self.scope_result['selected_roles']
        effort_estimation = self.effort_result['categories']
        
        role_fte = self.fte_calculator.calculate_role_fte_from_effort(effort_estimation, selected_roles)
        
        # Convert to dict with hours, days, months
        fte_result = {}
        total_fte_hours = 0
        
        for role in selected_roles:
            hours = role_fte.get(role, 0)
            fte_result[role] = {
                'hours': hours,
                'days': hours / 8,
                'months': (hours / 8) / 30
            }
            total_fte_hours += hours
        
        self.fte_result = {
            'by_role': fte_result,
            'total_hours': total_fte_hours,
            'total_days': total_fte_hours / 8,
            'total_months': (total_fte_hours / 8) / 30
        }
        
        print(f"\n✓ FTE allocation complete")
        print(f"  Selected Roles: {len(selected_roles)}")
        print(f"  Total Role Hours: {total_fte_hours:.2f} hours")
        print(f"  Average per Role: {total_fte_hours / len(selected_roles):.2f} hours")
        
        return self.fte_result
    
    def generate_report(self, output_filename: str = None) -> dict:
        """
        Generate complete scoping report (JSON + Word document)
        
        Args:
            output_filename: Optional custom filename
        
        Returns:
            Complete report data with file paths
        """
        if not self.scope_result or not self.effort_result:
            raise ValueError("Must process scope and calculate effort before generating report")
        
        print("\n" + "="*80)
        print("GENERATING REPORT")
        print("="*80)
        
        # Generate JSON report
        report = {
            'generated_at': datetime.now().isoformat(),
            'scope_definition': {
                'total_weightage': self.scope_result['total_weightage'],
                'tier': self.scope_result['tier'],
                'tier_name': self.scope_result['tier_name'],
                'tier_range': self.scope_result['tier_range'],
                'selected_roles': self.scope_result['selected_roles'],
                'summary': self.scope_result['summary'],
                'metrics': self.scope_result['metrics']
            },
            'effort_estimation': {
                'summary': self.effort_result['summary'],
                'categories': self.effort_result['categories']
            }
        }
        
        # Add FTE allocation if available
        if self.fte_result:
            report['fte_allocation'] = self.fte_result
        
        # Save JSON report
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'scoping_report_{timestamp}'
        else:
            # Remove extension if provided
            output_filename = output_filename.replace('.json', '').replace('.docx', '')
        
        json_path = OUTPUT_DIR / f'{output_filename}.json'
        
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[OK] JSON Report saved to: {json_path}")
        
        # Generate Word document report
        sow_generator = SOWReportGenerator()
        
        # Prepare FTE allocation for Word doc
        fte_for_word = {}
        if self.fte_result:
            for role in self.scope_result['selected_roles']:
                if role in self.fte_result['by_role']:
                    fte_for_word[role] = self.fte_result['by_role'][role]
        
        # Don't add extra timestamp - output_filename already has one
        docx_filename = f'{output_filename.replace(".json", "")}.docx'
        
        docx_path = sow_generator.generate_word_document(
            self.scope_result,
            self.effort_result['categories'],
            self.effort_result['summary'],
            fte_for_word,
            self.scope_inputs_dict,
            OUTPUT_DIR / docx_filename
        )
        
        print(f"[OK] Word Report saved to: {docx_path}")
        
        report['files'] = {
            'json_report': str(json_path),
            'word_report': str(docx_path)
        }
        
        return report
    
    def run_complete_workflow(self, user_input: dict, output_filename: str = None) -> dict:
        """
        Run complete workflow: scope → effort → report
        
        Args:
            user_input: Scope definition inputs
            output_filename: Optional custom output filename
        
        Returns:
            Complete report
        """
        print("\n" + "="*80)
        print("FCC ENGAGEMENT SCOPING TOOL - COMPLETE WORKFLOW")
        print("="*80)
        
        # Step 1: Process scope
        self.process_scope(user_input)
        
        # Step 2: Calculate effort
        self.calculate_effort()
        
        # Step 3: Calculate FTE allocation
        self.calculate_fte_allocation()
        
        # Step 4: Generate report
        report = self.generate_report(output_filename)
        
        # Print summary
        self._print_summary()
        
        return report
    
    def _print_summary(self):
        """Print executive summary"""
        print("\n" + "="*80)
        print("EXECUTIVE SUMMARY")
        print("="*80)
        
        scope = self.scope_result
        effort = self.effort_result['summary']
        
        print(f"\n📊 SCOPE DEFINITION")
        print(f"   Engagement Weightage: {scope['total_weightage']}")
        print(f"   Implementation Tier: {scope['tier']} - {scope['tier_name']}")
        print(f"   Weightage Range: {scope['tier_range'][0]}-{scope['tier_range'][1]}")
        print(f"   Features In Scope: {scope['summary']['in_scope_count']}/{scope['summary']['total_metrics']}")
        
        print(f"\n⏱️  EFFORT ESTIMATION")
        print(f"   Total Time (Tier-Adjusted): {effort['total_time_hours']} hours")
        print(f"   Final Estimate: {effort['final_estimate_hours']} hours")
        print(f"   Duration: {effort['total_days']} days")
        print(f"   Duration: {effort['total_months']} months")
        
        print(f"\n👥 TEAM")
        print(f"   Selected Roles: {len(scope['selected_roles'])}")
        for role in scope['selected_roles']:
            print(f"     • {role}")
        
        # Print FTE allocation if available
        if self.fte_result:
            print(f"\n📊 FTE ALLOCATION BY ROLE")
            print(f"   {'Role':<40} {'Hours':>12}")
            print(f"   {'-'*54}")
            for role in scope['selected_roles']:
                if role in self.fte_result['by_role']:
                    hours = self.fte_result['by_role'][role]['hours']
                    print(f"   {role:<40} {hours:>12.2f}")
            print(f"   {'-'*54}")
            print(f"   {'TOTAL':<40} {self.fte_result['total_hours']:>12.2f}")
        
        print("\n" + "="*80)
