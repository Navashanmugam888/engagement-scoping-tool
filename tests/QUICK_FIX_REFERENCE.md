# QUICK REFERENCE: EFFORT CALCULATION FIXES NEEDED

## Current State: Python = 1541.0 hours vs Excel = 884.5 hours (+74.2% ERROR)

## 7 Categories with Critical Mismatches

| # | Category | Excel | Python | Error | Fix |
|---|----------|-------|--------|-------|-----|
| 1 | Build and Configure FCC | 104 | 139.5 | +35.5 | Remove subtask detail summing |
| 2 | Historical Data | 72 | 592.0 | +520.0 | HistData Validation is separate |
| 3 | Calculations | 27 | 46.0 | +19.0 | BR/MF are separate tasks |
| 4 | Integrations | 92 | 124.0 | +32.0 | Don't add detail calculations |
| 5 | Secured Dimensions | 4 | 24.0 | +20.0 | Task row, not category |
| 6 | Testing/Training | 164 | 244.0 | +80.0 | Verify base/tier logic |
| 7 | Management Reports | 52 | 0.0 | -52.0 | IMPLEMENT formula |

## The Core Problem

Python is mixing TWO DIFFERENT CALCULATION PATTERNS:

### Pattern A (Category Headers)
Excel: `Base + TierAdj` (ignores detail calculations)
Python: `Base + TierAdj + (sum of ALL task details)` ← **WRONG**

### Pattern B (Task Rows)  
Excel: Detail-based formula only (e.g., `E*4`, `ROUND(E*0.5)*8+...`)
Python: Some implemented, some not

## Top 3 Priorities

### 1. Fix `calculate_category_final_estimate()` 
**Remove the line:** `task_estimate_sum = sum(task_estimates.values())`

Categories should return ONLY: `base_hours + tier_adjustment`

### 2. Separate Task Rows from Categories
Stop treating rows 81 (Secured Dimensions), 98 (Management Reports), etc. as category headers.

They're individual task rows with their own detail formulas.

### 3. Implement Missing Formulas
- Row 98 (Management Reports): `=ROUND(E*0.5,0)*8 + ROUND(E*0.25,0)*12 + ROUND(E*0.25,0)*16`
- Verify other complex formulas are correct

## Expected Result After Fixes

Total hours should be: **884.5** (currently 1541.0)

This is a **42% reduction** in estimated effort - shows how severe the overestimation is.

## Files to Modify

1. `backend/core/effort_calculator.py` - Main fix
2. `backend/data/effort_template.py` - Structure update
3. Tests expecting old values need updates

---

**Generated:** December 2, 2025  
**Status:** Ready for implementation
