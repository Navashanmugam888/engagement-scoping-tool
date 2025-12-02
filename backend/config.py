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

# Tier definitions based on engagement weightage
TIERS = {
    1: {"name": "Tier 1 - Jumpstart", "range": (0, 60)},
    2: {"name": "Tier 2 - Foundation Plus", "range": (61, 100)},
    3: {"name": "Tier 3 - Enhanced Scope", "range": (101, 150)},
    4: {"name": "Tier 4 - Advanced Enablement", "range": (151, 200)},
    5: {"name": "Tier 5 - Full Spectrum", "range": (201, 999)}
}

# Available roles for implementation
AVAILABLE_ROLES = [
    "PM USA",
    "PM India",
    "Architect USA",
    "Delivery Lead India",
    "Sr. Delivery Lead India",
    "App Lead USA",
    "App Lead India",
    "App Developer USA",
    "App Developer India",
    "Integration Lead USA",
    "Integration Developer India",
    "Reporting Lead India",
    "Security Lead India"
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
