# Metric Name Mapping - Excel vs CSV vs Image

## NAME MISMATCHES FOUND:

### Dimensions Section
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Multi-GAAP | Multi-GAAP | ✓ Match |

### Application Features Section
| Image Name | CSV/Current Name | Status | Action Needed |
|------------|------------------|--------|---------------|
| Elimination | Elimination | ✓ Match | - |
| Custom Elimination Requirement | (Not in CSV) | ❌ MISSING | ADD |
| Consolidation Journals | Consolidation Journals | ✓ Match | - |
| Journal Templates | Journal Templates | ✓ Match (sub) | - |
| Parent Currency Journals | Parent Currency Journals | ✓ Match (sub) | - |
| Ownership Management | Ownership Management | ✓ Match | - |
| Enhanced Organization by Period | Enhanced Organization by Period | ✓ Match (sub) | - |
| Equity Pickup | Equity Pickup | ✓ Match (sub) | - |
| Partner Elimination | Partner Elimination | ✓ Match (sub) | - |
| Configurable Consolidation Rules | Configurable Consolidation Rules | ✓ Match (sub) | - |
| Cash Flow | Cash Flow | ✓ Match | - |
| Supplemental Data Collection | Supplemental Data Collection | ✓ Match | - |
| Enterprise Journals | Enterprise Journals | ✓ Match | - |
| Approval Process | Approval Process | ✓ Match | - |
| Historic Overrides | Historic Overrides | ✓ Match | - |
| Task Manager | Task Manager | ✓ Match | - |
| Audit | Audit | ✓ Match | - |

### Application Customization
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Data Forms | Data Forms (array supplement) | ✓ Match |
| Dashboards | Dashboards (array supplement) | ✓ Match |

### Calculations
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Business Rules | Business Rules (array supplement) | ✓ Match |
| Member Formula | Member Formula (array supplement) | ✓ Match |
| Ratios | Ratios | ✓ Match |
| Custom KPIs | Custom KPIs | ✓ Match |

### Security
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Secured Dimensions | Secured Dimensions (array supplement) | ✓ Match |
| Number of Users | Number of Users (array supplement) | ✓ Match |

### Historical Data
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Historical Data Validation | Historical Data Validation (array supplement) | ✓ Match |
| Data Validation for Account Alt Hierarchies | Data Validation for Account Alt Hierarchies | ✓ Match |
| Data Validation for Entity Alt Hierarchies | Data Validation for Entity Alt Hierarchies | ✓ Match |
| Historical Journal Conversion | Historical Journal Conversion | ✓ Match |

### Integrations
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Files Based Loads | Files Based Loads | ✓ Match |
| Direct Connect Integrations | Direct Connect Integrations | ✓ Match |
| Outbound Integrations | Outbound Integrations | ✓ Match |
| Pipeline | Pipeline | ✓ Match |
| Custom Scripting | Custom Scripting | ✓ Match |

### Reporting
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Management Reports | Management Reports | ✓ Match |
| Consolidation Reports | Consolidation Reports | ✓ Match |
| Consolidation Journal Reports | Consolidation Journal Reports | ✓ Match |
| Intercompany Reports | Intercompany Reports | ✓ Match |
| Task Manager Reports | Task Manager Reports | ✓ Match |
| Enterprise Journal Reports | Enterprise Journal Reports | ✓ Match |
| Smart View Reports | Smart View Reports | ✓ Match |

### Automations
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Automated Data loads | Automated Data loads | ✓ Match |
| Automated Consolidations | Automated Consolidations | ✓ Match |
| Backup and Archival | Backup and Archival | ✓ Match |
| Metadata Import | Metadata Import | ✓ Match |

### Testing/Training
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Unit Testing | Unit Testing | ✓ Match |
| UAT | UAT | ✓ Match |
| SIT | SIT | ✓ Match |
| Parallel Testing | Parallel Testing | ✓ Match |
| User Training | User Training | ✓ Match |

### Transition
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Go Live | Go Live | ✓ Match |
| Hypercare | Hypercare | ✓ Match |

### Documentations
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| RTM | RTM | ✓ Match |
| Design Document | Design Document | ✓ Match |
| System Configuration Document | System Configuration Document | ✓ Match |

### Change Management
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Admin Desktop Procedures | Admin Desktop Procedures | ✓ Match |
| End User Desktop Procedures | End User Desktop Procedures | ✓ Match |

### Project Management
| Image Name | CSV/Current Name | Status |
|------------|------------------|--------|
| Project Management | Project Management (array supplement) | ✓ Match |

## GREY CELL ANALYSIS (Details NOT Required)

From Image (Grey cells = NO details needed):
1. Entity (grey)
2. Entity Redesign (grey) 
3. Scenario (white - NEEDS details)
4. Custom Elimination Requirement (grey)
5. Journal Templates (white - NEEDS details)
6. Historic Overrides (grey)
7. Parallel Testing (white - NEEDS details)
8. Historical Journal Conversion (grey)

## MISSING METRIC:

**"Custom Elimination Requirement"** - This appears in the image but NOT in formulas_expanded.csv

## RECOMMENDATIONS:

1. ✅ Most metric names match correctly
2. ❌ ADD: "Custom Elimination Requirement" formula to CSV
3. ✅ Grey cell detection logic is in place (checks cell fill color)
4. ✅ Formula evaluation working correctly
5. ⚠️  Need to verify grey cell detection matches image exactly
