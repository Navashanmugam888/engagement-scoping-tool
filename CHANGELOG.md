# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-12-02

### Features
- Initial release of Engagement Scoping Tool for FCC implementations
- Complete effort estimation engine with 16 category tier-based scaling
- Scope definition processor with metric weightage calculation
- Formula evaluator supporting Excel-like syntax
- Support for 71 FCC implementation metrics
- Tier-based classification (Tier 1-5 based on engagement weightage 0-999)
- Exact parity with Excel Effort Estimation workbook calculations

### Fixed
- **Historical Data Category Calculation**: Fixed 120-hour gap in Historical Data category
  - Root cause: Data validation tasks (rows 86-88) incorrectly using own details instead of shared Historical Data Validation details
  - Solution: Updated to use `historical_data_validation.details` for all three data validation task formulas:
    - Data Validation for Account Alt Hierarchies: `20 × hist_data_details`
    - Data Validation for Entity Alt Hierarchies: `20 × hist_data_details`
    - Historical Journal Conversion: `20 × hist_data_details`
  - Result: Historical Data total now correctly calculates as 552 hours (72 base + tier + 360+40+40+40 tasks)

### Implementation Details

#### Data Validation Task Dependencies
Excel formulas for data validation tasks use hardcoded cell references:
- Row 86: `=C86*E86` where `E86=IF(D86="YES",'Scope Definition'!D54,0)`
- Row 87: `=C87*E87` where `E87='Scope Definition'!D13`
- Row 88: `=C88*E88` where `E88=IF(D88="YES",'Scope Definition'!D54,0)`

All reference the Historical Data Validation details value (Scope Definition!D54), not their own metrics.

#### Critical Components
- **In-Scope Flag**: Gate (0/1) that determines effort contribution
- **Tier Adjustments**: 4 adjustment tiers for 16 categories
  - (0, 8, 12, 16): 11 categories
  - (0, 8, 16, 24): 4 categories
  - (0, 4, 6, 8): 1 category
  - (0, 0, 0, 0): 1 category
- **Excel ROUND Implementation**: Custom function for round-half-up behavior
- **Task Formulas**: 34 tasks with specialized formulas, 58 tasks with zero contribution

### Testing
- Comprehensive test validates all 16 categories against Excel values
- Test case: 1892.5 hours (236.6 days, 7.89 months) - exact match to Excel
- All metrics tested with actual weightage calculations

### Documentation
- Added comprehensive README with usage examples
- Documented tier definitions and calculation methodology
- Added docstrings explaining critical logic dependencies
- Created CHANGELOG for version tracking

### Known Dependencies
- **EffortCalculator** depends on exact formula implementations - do not modify without Excel verification
- **Historical Data Validation details** shared with 3 dependent tasks - changes to this metric affect 4 categories
- **In-scope flag** is critical control - must be set before effort calculation
- **Excel ROUND** behavior required for formula accuracy - use `excel_round()` function

