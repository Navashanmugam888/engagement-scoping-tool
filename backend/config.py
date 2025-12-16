"""
Configuration and Constants
Centralized configuration for the scoping tool
"""

from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'backend' / 'data'
OUTPUT_DIR = BASE_DIR / 'output'
EXCEL_FILE = BASE_DIR / 'Engagement Scoping Tool - FCC.xlsx'

# Tier definitions based on engagement weightage (SINGLE SOURCE OF TRUTH)
TIER_THRESHOLDS = [
    {"tier": "Tier 1 - Jumpstart", "minWeightage": 0, "maxWeightage": 61},
    {"tier": "Tier 2 - Foundation Plus", "minWeightage": 61, "maxWeightage": 100},
    {"tier": "Tier 3 - Enhanced Scope", "minWeightage": 101, "maxWeightage": 150},
    {"tier": "Tier 4 - Advanced Enablement", "minWeightage": 151, "maxWeightage": 200},
    {"tier": "Tier 5 - Full Spectrum", "minWeightage": 201, "maxWeightage": 999},
]

















# TIERS dict for backward compatibility (derived from TIER_THRESHOLDS)
TIERS = {
    i+1: {"name": tier["tier"], "range": (tier["minWeightage"], tier["maxWeightage"])}
    for i, tier in enumerate(TIER_THRESHOLDS)
}

# Available roles for implementation (SINGLE SOURCE OF TRUTH)
AVAILABLE_ROLES = [
    "PM USA",
    "PM India",
    "Architect USA",
    "Sr. Delivery Lead India",
    "Delivery Lead India",
    "App Lead USA",
    "App Lead India",
    "App Developer USA",
    "App Developer India",
    "Integration Lead USA",
    "Integration Developer India",
    "Reporting Lead India",
    "Security Lead India",
]

















# Calculation constants
HOURS_PER_DAY = 8
DAYS_PER_MONTH = 30

# Excel sheet names
SHEET_SCOPE_DEFINITION = 'Scope Definition'
SHEET_EFFORT_ESTIMATION = 'Effort Estimation'
SHEET_SCOPE_OF_SERVICE = 'Scope of Service'

# Named ranges (from Excel)
NAMED_RANGES = {
    'EngagementWeightage': 'Scope Definition!E103',
    'FeatureCleanRange': 'Scope Definition!G6:G102',
    'InScopeFlagRange': 'Scope Definition!H6:H102'
}
