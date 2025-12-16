"""
Report Generator - Creates SOW Report with Scope, Timings, and KDD Items

This generates a professional report document based on scoping results.
"""

import json
from datetime import datetime, timedelta
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from backend.data.excel_templates import KDD_DEFINITIONS, KDD_CONDITIONAL_MAPPINGS


class SOWReportGenerator:
    """Generate Statement of Work report with Scope, Timings, and KDD Items"""
    
    def __init__(self):
        """Initialize report generator"""
        # Tier definitions
        self.tier_ranges = {
            'Tier 1 - Jumpstart': {'min': 0, 'max': 60},
            'Tier 2 - Foundation Plus': {'min': 61, 'max': 100},
            'Tier 3 - Enhanced Scope': {'min': 101, 'max': 150},
            'Tier 4 - Advanced Enablement': {'min': 151, 'max': 200},
            'Tier 5 - Full Spectrum': {'min': 201, 'max': 999},
        }
    
    def get_tier_name(self, weightage):
        """Determine tier name based on engagement weightage"""
        for tier_name, range_dict in self.tier_ranges.items():
            if range_dict['min'] <= weightage <= range_dict['max']:
                return tier_name
        return 'Tier 3 - Enhanced Scope'  # Default
    
    def get_scope_details(self):
        """Extract scope details from Scope Definition sheet"""
        details = {}
        
        # Map of metric name to cell reference (Column D = Details)
        # These are the key metrics we need
        key_metrics = {
            'Account': 6,           # Row 6, Column D
            'Account Hierarchies': 7,
            'Entity': 11,
            'Entity Hierarchies': 13,
            'Currencies': 9,
            'Reporting Currencies': 10,
            'Custom Dimensions': 16,
            'Custom Dimension Hierarchies': 17,
            'Data Forms': 40,
            'Business Rules': 44,
            'Member Formulas': 45,
        }
        
        for metric_name, row in key_metrics.items():
            details[metric_name] = self.ws_scope.cell(row, 4).value or 0  # Column D
        
        return details
    
    def get_metric_in_scope(self, metric_name):
        """Check if a metric is in scope (Column C = YES/NO)"""
        # Find the row with this metric
        for row in range(6, 100):
            metric = self.ws_scope.cell(row, 2).value
            if metric and metric.strip() == metric_name.strip():
                in_scope = self.ws_scope.cell(row, 3).value
                return in_scope == 'YES'
        return False
    
    def generate_scope_section(self, scope_data, tier_name):
        """Generate Scope of Service section"""
        scope_text = f"""
================================================================================
1. SCOPE OF SERVICE
================================================================================

Engagement Tier: {tier_name}

Scope of Services

Under this SOW, Donyati will work with Client to provide Services noted below. 
Actual activities, work items, schedule and deliverables would be jointly managed 
by Donyati and Client based on the Client's business priorities. 

The scope of this engagement is focused on the implementation of the following 
application modules:

Oracle EPM Enterprise – Financial Consolidation and Close

Donyati Services consist of the following:

DIMENSIONS
----------
• Account Dimension
  Approximately {scope_data.get('Account', 'TBD')} accounts will be configured 
  based on the current Chart of Accounts.
  
• Account Alternate Hierarchies
  Up to {scope_data.get('Account Hierarchies', 'TBD')} alternate hierarchies 
  will be developed.
  
• Entity Dimension
  Approximately {scope_data.get('Entity', 'TBD')} entities will be configured 
  based on the current structure.
  
• Entity Alternate Hierarchies
  Up to {scope_data.get('Entity Hierarchies', 'TBD')} alternate hierarchies 
  will be developed.
  
• Currency Configuration
  {scope_data.get('Currencies', 'TBD')} currencies will be configured with 
  {scope_data.get('Reporting Currencies', 'TBD')} reporting currency/currencies.
  
• Custom Dimensions
  {scope_data.get('Custom Dimensions', 'TBD')} custom dimensions will be leveraged 
  to support additional reporting requirements. Up to {scope_data.get('Custom Dimension Hierarchies', 'TBD')} 
  alternate hierarchies will be developed.
  
• Standard Dimensions
  Year, Period, View, Consolidation, Intercompany, and Data Source dimensions 
  will be configured to support consolidation and reporting.

APPLICATION FEATURES
--------------------
• Standard elimination capabilities will be provided
• Consolidation journals will be enabled
• Consolidation journal templates will be created as needed
• Approval process will be utilized in the application
• Task manager may be used to support Financial Consolidation and Close

APPLICATION CUSTOMIZATION
--------------------------
• Custom Data Forms
  If required, up to {scope_data.get('Data Forms', 'TBD')} custom data forms 
  will be developed to support Financial Consolidation and Close.

CALCULATIONS
------------
• Custom Business Rules
  If required, up to {scope_data.get('Business Rules', 'TBD')} custom business 
  rules will be developed to support Financial Consolidation and Close.
  
• Member Formulas
  If required, up to {scope_data.get('Member Formulas', 'TBD')} member formulas 
  will be developed to support Financial Consolidation and Close.

SECURITY
--------
• User security will be configured based on Client's requirements
• Data security will be implemented as required
"""
        return scope_text
    
    def generate_timings_section(self, effort_estimation, summary, fte_hours_dict=None):
        """Generate Timings/Effort Estimation section with monthly resource allocation
        
        Args:
            effort_estimation: Category effort breakdown
            summary: Total hours/days/months
            fte_hours_dict: Dict of role -> total_fte_hours (from FTE calculator)
        """
        from datetime import datetime, timedelta
        
        total_months = summary['total_months']
        total_months_rounded = round(total_months)
        
        # Calculate dates
        today = datetime.now()
        start_date = today.strftime("%d-%b-%Y").upper()
        
        # Add months to get end date
        month = today.month + total_months_rounded
        year = today.year
        while month > 12:
            month -= 12
            year += 1
        
        # Get last day of target month
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        end_date_str = end_date.strftime("%d-%b-%Y").upper()
        
        # Build monthly allocation table
        timings_text = f"""
================================================================================
2. TIMINGS (EFFORT ESTIMATION & RESOURCE ALLOCATION)
================================================================================

IMPLEMENTATION SCHEDULE
-----------------------
• Engagement Start Date: {start_date}
• Engagement End Date: {end_date_str}
• Total Duration: {total_months_rounded} months

Note: Go-live support will be provided and additional capabilities will be added 
per a subsequent Statement of Work expected to be started immediately following 
the completion of this Statement of Work.

TOTAL IMPLEMENTATION EFFORT
---------------------------
• Total Hours: {summary['total_time_hours']:.1f} hours
• Total Days: {summary['total_days']:.1f} days (@ 8 hours/day)
• Total Months: {total_months:.2f} months (@ 30 days/month)

This SOW assumes {total_months_rounded} months to complete Financial Consolidation and Close.

EFFORT BY CATEGORY
-------------------
"""
        
        # Add category breakdown
        for category_name in sorted(effort_estimation.keys()):
            cat_data = effort_estimation[category_name]
            hours = cat_data['final_estimate']
            days = cat_data['in_days']
            timings_text += f"• {category_name:<50} {hours:>8.1f} hrs ({days:>6.2f} days)\n"
        
        timings_text += f"""
TOTAL                                                      {summary['total_time_hours']:>8.1f} hrs ({summary['total_days']:>6.2f} days)

MONTHLY RESOURCE ALLOCATION
----------------------------
Completion of Services and Deliverables agreed upon is subject to, among other 
things, appropriate cooperation, obtaining the necessary information, and timely 
response to inquiries. The table below shows the estimated hours per month for 
each resource role. At the conclusion of Requirements and Design, Donyati will 
revise the implementation timeline to incorporate agreed upon requirements and 
design elements. Donyati and Client will review and approve the revised 
implementation timeline before moving into the Development Phase.

"""
        
        # Generate monthly allocation table
        if fte_hours_dict:
            timings_text += "Resource Role / Monthly Hours"
            
            # Create header row with month numbers
            timings_text += "\t" * 2
            for month in range(1, total_months_rounded + 1):
                timings_text += f"\t{month}"
            timings_text += "\n"
            timings_text += "-" * 100 + "\n"
            
            # Add each role's monthly allocation
            for role in sorted(fte_hours_dict.keys()):
                total_fte = fte_hours_dict[role]
                monthly_hours = total_fte / total_months_rounded
                monthly_hours_rounded = round(monthly_hours)
                
                timings_text += f"{role:<40}"
                for month in range(1, total_months_rounded + 1):
                    timings_text += f"\t{monthly_hours_rounded}"
                timings_text += "\n"
        
        timings_text += """
TIMELINE ASSUMPTIONS
---------------------
• 8 hours per working day
• 30 days per month
• Assumes full-time commitment of allocated resources
• Schedule may vary based on resource availability and Client priorities
"""
        return timings_text
    
    def _load_kdd_definitions(self):
        """Load KDD definitions from Definitions sheet"""
        try:
            ws_def = self.wb['Definitions']
            kdd_list = {}
            
            # Rows B138-B149 contain the KDD definitions
            # These are referenced by the conditional formulas
            kdd_rows = list(range(138, 150))  # Rows 138-149
            
            for idx, row in enumerate(kdd_rows, 1):
                kdd_text = ws_def.cell(row, 2).value  # Column B
                if kdd_text:
                    kdd_list[f'KDD{idx:02d}'] = str(kdd_text).strip()
            
            return kdd_list
        except:
            return {}
    
    def get_applicable_kdds(self, scope_inputs_dict):
        """
        Determine which KDDs apply based on scope definition
        
        Formulas from user:
        - KDD01: If E26 > 0 (Custom Dimensions)
        - KDD02: If E31 > 0 (Cash Flow)
        - KDD03: If E23 > 0 (Journals)
        - KDD04: If F59 > 0 (Smart View Reports)
        - KDD05: If F53 > 0 (Consolidation Journal Reports)
        - KDD06: If F75 > 0 (Custom Scripting)
        - KDD07: If E34 > 0 (Approval Process)
        - KDD08: If E36 > 0 (Historic Overrides)
        - KDD09: If E32 > 0 (Audit)
        - KDD10: If E33 > 0 (Task Manager)
        - KDD11: If F49 > 0 (Management Reports)
        - KDD12: If E37 > 0 (Business Rules)
        """
        
        applicable = []
        
        # Map of KDD to metric name and required details value > 0
        kdd_mapping = {
            'KDD01': ('Custom Dimensions', 'details'),
            'KDD02': ('Cash Flow', 'details'),
            'KDD03': ('Consolidation Journals', 'details'),
            'KDD04': ('Smart View Reports', 'details'),
            'KDD05': ('Consolidation Journal Reports', 'details'),
            'KDD06': ('Custom Scripting', 'details'),
            'KDD07': ('Approval Process', 'details'),
            'KDD08': ('Historic Overrides', 'details'),
            'KDD09': ('Audit', 'details'),
            'KDD10': ('Task Manager', 'details'),
            'KDD11': ('Management Reports', 'details'),
            'KDD12': ('Business Rules', 'details'),
        }
        
        # Check which metrics are in scope with details > 0
        for kdd_id, (metric_name, check_type) in kdd_mapping.items():
            # Find in scope_inputs_dict
            for metric in scope_inputs_dict:
                if metric.get('name') == metric_name:
                    in_scope = metric.get('in_scope') == 'YES'
                    details = metric.get('details', 0) or 0
                    
                    if in_scope and details > 0:
                        applicable.append(kdd_id)
                    break
        
        return applicable
    
    def generate_kdd_section(self, scope_inputs_dict=None):
        """Generate Key Design Decisions section from Scope Definition sheet
        
        Structure:
        - KDD01-KDD04: Always included (default for all implementations)
        - KDD05+: Conditional based on Scope Definition cell values
        
        Uses conditional logic:
        - IF(Scope Definition!E26>0, Definitions!B138, "") -> Ownership Management (KDD05)
        - IF(Scope Definition!E31>0, Definitions!B139, "") -> Cash Flow (KDD06)
        - IF(Scope Definition!E23>0, Definitions!B140, "") -> Journal Process (KDD07)
        - IF(Scope Definition!F59>0, Definitions!B141, "") -> Integrations (KDD08)
        - IF(Scope Definition!F53>0, Definitions!B142, "") -> Historical Data (KDD09)
        - IF(Scope Definition!F75>0, Definitions!B143, "") -> Automations (KDD10)
        - IF(Scope Definition!E34>0, Definitions!B144, "") -> Approval Process (KDD11)
        - IF(Scope Definition!E36>0, Definitions!B145, "") -> Task Manager (KDD12)
        - IF(Scope Definition!E32>0, Definitions!B146, "") -> Supplemental Data (KDD13)
        - IF(Scope Definition!E33>0, Definitions!B147, "") -> Enterprise Journals (KDD14)
        - IF(Scope Definition!F49>0, Definitions!B148, "") -> Application Security (KDD15)
        - IF(Scope Definition!E37>0, Definitions!B149, "") -> Audit (KDD16)
        
        Args:
            scope_inputs_dict: List of scope input dicts (optional)
        """
        
        # Load Definitions sheet for KDD text
        try:
            ws_defs = self.wb['Definitions']
        except:
            ws_defs = load_workbook(EXCEL_FILE, data_only=True)['Definitions']
        
        # Conditional KDD mapping: (Scope Definition cell, Definitions sheet row, KDD number, KDD title)
        conditional_kdd_mappings = [
            ('E26', 138, '05', 'Ownership Management'),
            ('E31', 139, '06', 'Cash Flow'),
            ('E23', 140, '07', 'Journal Process'),
            ('F59', 141, '08', 'Integrations'),
            ('F53', 142, '09', 'Historical Data Source and Validations'),
            ('F75', 143, '10', 'Automations'),
            ('E34', 144, '11', 'Approval Process'),
            ('E36', 145, '12', 'Task Manager'),
            ('E32', 146, '13', 'Supplemental Data Collection'),
            ('E33', 147, '14', 'Enterprise Journals'),
            ('F49', 148, '15', 'Application Security'),
            ('E37', 149, '16', 'Audit'),
        ]
        
        kdd_text = """
================================================================================
3. KEY DESIGN DECISIONS (KDD)
================================================================================

The following Key Design Decisions have been identified as critical for the 
successful implementation:

"""
        
        # Always include KDD01-KDD04 (default for all implementations)
        default_kdds = [
            ('01', 'General Application Configuration', 
             'Configuration of general application settings including dimensions, members, '
             'accounts, and application structure per requirements.'),
            ('02', 'Metadata Configuration', 
             'Configuration of metadata elements including custom properties, business rules, '
             'member formulas, and calculation logic.'),
            ('03', 'FCC Consolidations and Other Calculations', 
             'Configuration of consolidation rules, elimination entries, adjustment journals, '
             'and supporting calculations.'),
            ('04', 'Reports and Data Form Configuration', 
             'Development of management reports and data forms to support consolidation and '
             'financial reporting requirements.'),
        ]
        
        # Add default KDDs
        for kdd_num, kdd_title, kdd_desc in default_kdds:
            kdd_text += f"\nKDD{kdd_num}. {kdd_title}\n"
            kdd_text += f"    {kdd_desc}\n"
        
        # Collect and add conditional KDDs
        conditional_kdds = []
        
        for scope_cell, defs_row, kdd_num, kdd_title in conditional_kdd_mappings:
            try:
                # Get value from Scope Definition sheet
                scope_value = self.ws_scope[scope_cell].value
                
                # Check if value > 0
                if scope_value is not None and scope_value > 0:
                    # Get KDD text from Definitions sheet
                    kdd_text_from_defs = ws_defs.cell(defs_row, 2).value  # Column B
                    
                    if kdd_text_from_defs:
                        conditional_kdds.append((kdd_num, kdd_title, str(kdd_text_from_defs).strip()))
            except Exception as e:
                pass  # Skip if cell not found
        
        # Add conditional KDDs
        for kdd_num, kdd_title, kdd_desc in conditional_kdds:
            kdd_text += f"\nKDD{kdd_num}. {kdd_title}\n"
            kdd_text += f"    {kdd_desc}\n"
        
        kdd_text += "\n" + "=" * 80 + "\n"
        return kdd_text
    
    def generate_report(self, scope_result, effort_estimation, summary, fte_hours_dict=None, scope_inputs_dict=None):
        """
        Generate complete SOW report
        
        Args:
            scope_result: Output from ScopeDefinitionProcessor
            effort_estimation: Output from EffortCalculator
            summary: Summary dict with total hours/days/months
            fte_hours_dict: Dict of role -> total_fte_hours (from FTE calculator)
            scope_inputs_dict: List of scope input dicts (for KDD filtering)
            
        Returns:
            dict with report sections
        """
        # Get scope data
        scope_data = self.get_scope_details()
        
        # Determine tier
        weightage = scope_result['total_weightage']
        tier_name = scope_result['tier_name']
        
        # Generate sections
        scope_section = self.generate_scope_section(scope_data, tier_name)
        timings_section = self.generate_timings_section(effort_estimation, summary, fte_hours_dict)
        kdd_section = self.generate_kdd_section(scope_inputs_dict)
        
        # Combine report
        full_report = f"""
{'='*80}
STATEMENT OF WORK (SOW) REPORT
FCC IMPLEMENTATION ENGAGEMENT
{'='*80}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Engagement Weightage: {weightage:.1f}
Implementation Tier: {tier_name}

{scope_section}

{timings_section}

{kdd_section}

{'='*80}
END OF REPORT
{'='*80}
"""
        
        return {
            'full_report': full_report,
            'scope_section': scope_section,
            'timings_section': timings_section,
            'kdd_section': kdd_section,
            'metadata': {
                'weightage': weightage,
                'tier_name': tier_name,
                'total_hours': summary['total_time_hours'],
                'total_days': summary['total_days'],
                'total_months': summary['total_months'],
                'generated': datetime.now().isoformat()
            }
        }


if __name__ == '__main__':
    print("SOW Report Generator - Ready for testing")
    generator = SOWReportGenerator()
    print("✓ Generator initialized successfully")
