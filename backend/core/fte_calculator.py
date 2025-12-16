"""
FTE Efforts Calculator

Calculates role-based FTE (Full-Time Equivalent) effort allocation.
Uses SUMPRODUCT formula: hours × role allocation percentage for each tier.

Formula pattern from Excel:
=SUMPRODUCT($I$6:$I$22, J6:J22)

Where:
- $I$6:$I$22 = Hours from Effort Estimation for each tier
- J6:J22 = Role allocation percentage (0-1) for each tier
- Result = Total FTE hours for that role across all tiers
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.data.excel_templates import APP_TIERS_ROLES, APP_TIERS_DATA


class FTEEffortsCalculator:
    """Calculate role-based FTE effort allocation"""
    
    def __init__(self):
        """Load tier definitions and role allocation data from template"""
        self.tiers_data = {}  # Dict with row_index -> {hours, roles: {role -> allocation}}
        self.roles = []
        self.tier_hours = {}
        self.category_tier_mapping = {}  # Maps category name to tier row index
        
        self._load_app_tiers_data()
    
    def _load_app_tiers_data(self):
        """Load tier and role allocation data from template (previously from Excel App Tiers Definition sheet)"""
        # Use hardcoded roles from template
        self.roles = APP_TIERS_ROLES.copy()
        
        # Load tier/category data from template
        # Note: Hours are NOT stored in template - they come dynamically from effort_estimation
        for tier_info in APP_TIERS_DATA:
            row_idx = tier_info['row_index']
            self.tiers_data[row_idx] = {
                'category': tier_info['category'],
                'roles': tier_info['roles'].copy()
            }
        
        print(f"Loaded {len(self.roles)} roles: {self.roles}")
        print(f"Loaded {len(self.tiers_data)} tier/category rows (6-22)")
    
    def calculate_role_fte_from_effort(self, effort_estimation: dict, selected_roles: list = None) -> dict:
        """
        Calculate FTE hours for each role using effort estimation output
        
        Uses SUMPRODUCT: Sum of (Category_Hours × Role_Allocation_%)
        For each category, multiply the effort hours by the role's allocation percentage,
        then sum across all 17 rows (rows 6-22 in App Tiers Definition).
        
        Excel Formula Pattern: =SUMPRODUCT($I6:$I22, J6:J22)
        Where:
        - I6:I22 = Hours from effort_estimation (17 rows, one for each category)
        - J6:J22 = Role allocation percentage for that row
        
        Args:
            effort_estimation: dict from EffortCalculator.calculate_effort()
                              with category_name -> {'final_estimate': hours, ...} mapping
            selected_roles: list of selected role names (None = all roles)
        
        Returns:
            dict with role_name -> fte_hours mapping
        """
        role_fte = {}
        roles_to_calculate = selected_roles if selected_roles else self.roles
        
        # For each role, calculate SUMPRODUCT across all 17 rows (rows 6-22)
        for role in roles_to_calculate:
            if role not in self.roles:
                continue
            
            total_fte = 0.0
            
            # Iterate through each row 0-16 (representing rows 6-22 in Excel)
            for row_idx in range(17):  # 17 rows total (rows 6-22)
                if row_idx not in self.tiers_data:
                    continue
                
                tier_data = self.tiers_data[row_idx]
                category_name = tier_data['category']
                
                # Get hours for this category from effort_estimation
                # effort_estimation structure: {'Project Initiation and Planning': {'final_estimate': 18, ...}, ...}
                hours_value = 0.0
                if category_name in effort_estimation:
                    effort_entry = effort_estimation[category_name]
                    if isinstance(effort_entry, dict) and 'final_estimate' in effort_entry:
                        hours_value = effort_entry['final_estimate']
                    elif isinstance(effort_entry, (int, float)):
                        hours_value = effort_entry
                
                # Get role allocation percentage for this row
                role_allocation = tier_data['roles'].get(role, 0.0)
                
                # SUMPRODUCT: hours × allocation, then sum across all rows
                total_fte += hours_value * role_allocation
            
            role_fte[role] = total_fte
        
        return role_fte
    
    def get_role_allocation_matrix(self) -> dict:
        """
        Get the complete role allocation matrix for all tiers/categories
        
        Returns:
            dict with category_name -> {role -> allocation_percentage} mapping
        """
        allocation_matrix = {}
        for row_idx in sorted(self.tiers_data.keys()):
            tier_data = self.tiers_data[row_idx]
            category_name = tier_data['category']
            allocation_matrix[category_name] = tier_data['roles'].copy()
        
        return allocation_matrix
    
    def generate_fte_summary(self, effort_estimation: dict, selected_roles: list = None) -> dict:
        """
        Generate complete FTE summary for all selected roles
        
        Args:
            effort_estimation: Output from EffortCalculator.calculate_effort()
            selected_roles: List of selected role names
        
        Returns:
            dict with:
            - role_fte_hours: dict of role -> fte_hours
            - role_fte_days: dict of role -> fte_days (hours/8)
            - role_fte_summary: list of dicts with role details
        """
        # Map effort estimation by tier
        tier_efforts = {}
        for category, cat_data in effort_estimation.items():
            # Get tier name from effort_estimation summary
            # For now, assume we need to get this from scope_result
            pass
        
        # Calculate role FTE
        role_fte_hours = self.calculate_role_fte(tier_efforts, selected_roles)
        
        # Convert to days
        role_fte_days = {role: hours / 8 for role, hours in role_fte_hours.items()}
        
        # Create summary
        summary = []
        for role in (selected_roles if selected_roles else self.roles):
            if role in role_fte_hours:
                summary.append({
                    'role': role,
                    'fte_hours': role_fte_hours[role],
                    'fte_days': role_fte_days[role],
                    'fte_months': role_fte_days[role] / 30
                })
        
        return {
            'role_fte_hours': role_fte_hours,
            'role_fte_days': role_fte_days,
            'role_fte_summary': summary
        }

