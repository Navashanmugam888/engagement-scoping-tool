#!/usr/bin/env python
"""
DETAILED ANALYSIS OF EFFORT CALCULATION DISCREPANCIES
=====================================================

This script identifies why Python calculations differ from Excel.
"""

print("""
================================================================================
EFFORT CALCULATION DISCREPANCIES - ROOT CAUSE ANALYSIS
================================================================================

Based on examining the Excel "Effort Estimation" sheet formulas:

KEY FINDING: Excel has TWO TYPES of category calculations
===============================================================================

TYPE 1: CATEGORY HEADERS (Using named ranges & tier adjustments)
  Row 5: Project Initiation and Planning
  Row 18: Requirement Gathering
  Row 28: Design
  Row 35: Build and Configure FCC
  Row 53: Setup Application Features
  Row 74: Calculations
  Row 84: Historical Data
  Row 90: Integrations
  Row 90: Reporting (implied)
  Row 106: Automations
  Row 112: Testing/Training
  Row 123: Documentations
  Row 128: Change Management
  
  Formula Pattern:
    =IF(EngagementWeightage<=100, BASE_VALUE,
        IF(EngagementWeightage<=120, BASE_VALUE+8,
           IF(EngagementWeightage<=160, BASE_VALUE+12, BASE_VALUE+16)))
  
  The BASE_VALUE comes from Excel NAMED RANGES that reference Category sums
  Example: "Build_and_Configure" = SUM(C36:C51) = 88
  
  These categories DO NOT sum subtask details - they just add a tier adjustment
  to the base category hours.

TYPE 2: INDIVIDUAL TASK ROWS (Using detail-based formulas)
  Examples:
    Row 38: Account Alternate Hierarchies
    Row 41: Reporting Currency
    Row 45: Entity Alternate Hierarchies
    Row 49: Custom Dimensions
    Row 81: Secured Dimensions
    Row 98: Management Reports
    Row 116: Parallel Testing
  
  Formula Pattern:
    =C*E (simple multiplication)
      OR
    =ROUND(E*0.5,0)*8 + ROUND(E*0.25,0)*12 + ROUND(E*0.25,0)*16
  
  These tasks have their own row and calculate based on details (Column E)

CRITICAL ISSUE IN PYTHON CODE:
================================================================================

The Python EffortCalculator.calculate_category_final_estimate() function is:

1. WRONG: Adding subtask estimates to category base
   Current logic: category_base + task_estimate_sum
   
   This causes MASSIVE overestimation because:
   - Build and Configure FCC base = 88, gets +16 tier adjustment = 104
   - But then Python ADDS all the Account Alt Hierarchies, Currency, Entity
     Alt Hierarchies, etc. detail calculations ON TOP
   
2. WRONG: Treating Secured Dimensions, Number of Users as category sums
   - Row 81: "Secured Dimensions" is a SINGLE TASK, not a category header
   - It should calculate as E81*4 where E81 comes from details
   - But Python code treats it like a category header and adds ALL its
     subtasks (which don't exist)

3. WRONG: "Secured Dimensions" row 81 shows:
   - C81 = 2 (base hours)
   - E81 = formula looking up detail from Scope Definition
   - F81 = E81*4 (simple multiplication by details)
   
   But Python category_final_estimate adds tier adjustments (0-16) to this,
   treating it as a category header when it's actually a single task.

EXAMPLES OF MISMATCHES:
================================================================================

1. Build and Configure FCC:
   Excel: Base=88 + TierAdj(16 at W=141) = 104 hours
   Python: Base=88 + TierAdj + (C38*E38 + C40*E40 + C41*E41 + ... all subtasks)
           = 88 + 16 + 51.5 = 139.5
   ERROR: Python adds subtask details on top of category base

2. Historical Data:
   Excel: Base=60 + TierAdj(12 at W=141) = 72 hours
   Python: Base=60 + TierAdj + SUM of all tasks (like HistData Validation)
           = 60 + 12 + (15 + (4+1)*10)*8 = 60 + 12 + 520 = 592
   ERROR: Historical Data Validation formula result (520) should NOT be added
          to Historical Data category - they're separate!

3. Calculations:
   Excel: Base=15 + TierAdj(12) = 27 hours
   Python: Base=15 + TierAdj + business_rules_calc + member_formula_calc + ...
           = 15 + 12 + 8 + 11 + ... = 46
   ERROR: Those are separate category tasks, not subcategories

4. Management Reports:
   Excel: Row 98 with formula =ROUND(E98*0.5,0)*8 + ROUND(E98*0.25,0)*12 + ROUND(E98*0.25,0)*16
          = Complex scaling formula using details only, NO base + tier
          Result: 52 hours
   Python: 0 hours (not even recognized as having calculations)
   ERROR: Management Reports formula not implemented in Python

5. Secured Dimensions:
   Excel: Row 81 with formula =E81*4
          E81 = details value from Scope Definition = 1
          F81 = 1*4 = 4 hours
   Python: Treating as category header with tier adjustment + task estimates
           = 2 + 16 + 6 = 24
   ERROR: Should be 4 hours max, not 24

REQUIRED FIXES:
================================================================================

1. REFACTOR category identification:
   - Create a EXPLICIT list of which rows are CATEGORY HEADERS vs TASK ROWS
   - Category headers: 5, 18, 28, 35, 53, 74, 84, 90, 106, 112, 123, 128
   - Task rows with details: 38, 41, 45, 49, 70, 75, 76, 81, 82, 86-88, 92,
     95, 98, 100, 101, 104, 116, etc.

2. DO NOT mix calculations:
   - Category headers should NOT sum their subtask details
   - They should only apply: BASE_VALUE + TIER_ADJUSTMENT
   - Subtask calculations should be SEPARATE

3. Implement missing formulas:
   - Management Reports: =ROUND(E98*0.5,0)*8 + ROUND(E98*0.25,0)*12 + ROUND(E98*0.25,0)*16
   - Add Business Rules detail calculation
   - Add Member Formula detail calculation

4. Fix individual task mapping:
   - Secured Dimensions (Row 81): =E81*4 (not category, just task)
   - Number of Users (Row 82): =E82*0.2
   - Historical Data Validation is a separate row, not part of Historical Data category

5. Create EFFORT_ESTIMATION_TEMPLATE that mirrors Excel structure:
   - Don't nest task details under categories
   - Keep them as separate flat list
   - Only add task details to their parent category if explicitly nested in Excel
""")

# Create diagnostic output
import json

discrepancies = {
    'Build and Configure FCC': {
        'issue': 'Python adds subtask details to category base',
        'excel_logic': 'Base (88) + Tier Adjustment (16 at W=141) = 104',
        'python_logic': 'Base + TierAdj + sum(all detail formulas) = 139.5',
        'fix': 'Remove subtask detail summation from category_final_estimate'
    },
    'Historical Data': {
        'issue': 'Python includes HistData Validation (520) in category calc',
        'excel_logic': 'Base (60) + Tier Adjustment (12 at W=141) = 72',
        'python_logic': 'Base + TierAdj + Historical_Data_Validation_calc = 592',
        'fix': 'HistData Validation is separate, not part of HistData category'
    },
    'Calculations': {
        'issue': 'Python includes Business Rules and Member Formula',
        'excel_logic': 'Base (15) + Tier Adjustment (12 at W=141) = 27',
        'python_logic': 'Base + TierAdj + BR_calc + MF_calc = 46',
        'fix': 'These are separate tasks, not part of Calculations category'
    },
    'Management Reports': {
        'issue': 'Python missing complex detail formula',
        'excel_logic': 'Row 98: =ROUND(E*0.5,0)*8 + ROUND(E*0.25,0)*12 + ROUND(E*0.25,0)*16 = 52',
        'python_logic': 'Not implemented = 0',
        'fix': 'Add Management Reports detail calculation formula'
    },
    'Secured Dimensions': {
        'issue': 'Python treating as category instead of single task',
        'excel_logic': 'Row 81: =E*4 where E=1 = 4 hours',
        'python_logic': 'Base (2) + TierAdj (16) + task_details = 24',
        'fix': 'Row 81 is a task row, not a category header'
    }
}

with open('DISCREPANCY_ANALYSIS.json', 'w') as f:
    json.dump(discrepancies, f, indent=2)

print('\n\nDetailed analysis saved to DISCREPANCY_ANALYSIS.json')
