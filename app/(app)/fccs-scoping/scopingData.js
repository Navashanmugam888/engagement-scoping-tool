export const scopingSections = [
    {
        title: "Dimensions",
        items: [
            { id: "account", label: "Account", hasCount: true, subItems: [
                { id: "acc_alt_hier", label: "Account Alternate Hierarchies", hasCount: true },
                { id: "rat_coa", label: "Rationalization of CoA", hasCount: false }
            ]},
            { id: "multi_curr", label: "Multi-Currency", hasCount: true },
            { id: "rep_curr", label: "Reporting Currency", hasCount: true },
            { id: "entity", label: "Entity", hasCount: true, subItems: [
                 { id: "ent_redesign", label: "Entity Redesign", hasCount: false },
                 { id: "ent_alt_hier", label: "Entity Alternate Hierarchies", hasCount: true }
            ]},
            { id: "scenario", label: "Scenario", hasCount: true },
            { id: "multi_gaap", label: "Multi-GAAP", hasCount: false },
            { id: "cust_dim", label: "Custom Dimensions", hasCount: true, subItems: [
                 { id: "alt_hier_cust", label: "Alternate Hierarchies in Custom Dimensions", hasCount: true }
            ]},
            { id: "add_alias", label: "Additional Alias Tables", hasCount: true }
        ]
    },
    {
        title: "Application Features",
        items: [
            { id: "elim", label: "Elimination", hasCount: false },
            { id: "cust_elim", label: "Custom Elimination Requirement", hasCount: false },
            { id: "consol_journ", label: "Consolidation Journals", hasCount: false, subItems: [
                { id: "journ_temp", label: "Journal Templates", hasCount: true },
                { id: "parent_curr", label: "Parent Currency Journals", hasCount: false }
            ]},
            { id: "own_mgmt", label: "Ownership Management", hasCount: false, subItems: [
                { id: "enh_org", label: "Enhanced Organization by Period", hasCount: false },
                { id: "equity_pickup", label: "Equity Pickup", hasCount: false },
                { id: "partner_elim", label: "Partner Elimination", hasCount: false },
                { id: "config_consol", label: "Configurable Consolidation Rules", hasCount: false }
            ]},
            { id: "cash_flow", label: "Cash Flow", hasCount: false },
            { id: "supp_data", label: "Supplemental Data Collection", hasCount: false },
            { id: "ent_journ", label: "Enterprise Journals", hasCount: false },
            { id: "approval", label: "Approval Process", hasCount: false },
            { id: "hist_over", label: "Historic Overrides", hasCount: false },
            { id: "task_mgr", label: "Task Manager", hasCount: false },
            { id: "audit", label: "Audit", hasCount: false }
        ]
    },
    {
        title: "Application Customization",
        items: [
            { id: "data_forms", label: "Data Forms", hasCount: true },
            { id: "dashboards", label: "Dashboards", hasCount: true }
        ]
    },
    {
        title: "Calculations",
        items: [
            { id: "bus_rules", label: "Business Rules", hasCount: true },
            { id: "mem_form", label: "Member Formula", hasCount: true },
            { id: "ratios", label: "Ratios", hasCount: false },
            { id: "cust_kpi", label: "Custom KPIs", hasCount: false }
        ]
    },
    {
        title: "Security",
        items: [
            { id: "sec_dim", label: "Secured Dimensions", hasCount: true },
            { id: "num_users", label: "Number of Users", hasCount: true }
        ]
    },
    {
        title: "Historical Data",
        items: [
            { id: "hist_data", label: "Historical Data Validation", hasCount: true },
            { id: "val_acc_alt", label: "Data Validation for Account Alt Hierarchies", hasCount: false },
            { id: "val_ent_alt", label: "Data Validation for Entity Alt Hierarchies", hasCount: false },
            { id: "hist_journ", label: "Historical Journal Conversion", hasCount: false }
        ]
    },
    {
        title: "Integrations",
        items: [
            { id: "file_load", label: "Files Based Loads", hasCount: true },
            { id: "direct_conn", label: "Direct Connect Integrations", hasCount: true },
            { id: "outbound", label: "Outbound Integrations", hasCount: true },
            { id: "pipeline", label: "Pipeline", hasCount: true },
            { id: "cust_script", label: "Custom Scripting", hasCount: true }
        ]
    },
    {
        title: "Reporting",
        items: [
            { id: "mgmt_rep", label: "Management Reports", hasCount: true },
            { id: "consol_rep", label: "Consolidation Reports", hasCount: false },
            { id: "consol_journ_rep", label: "Consolidation Journal Reports", hasCount: true },
            { id: "inter_rep", label: "Intercompany Reports", hasCount: true },
            { id: "task_rep", label: "Task Manager Reports", hasCount: false },
            { id: "ent_journ_rep", label: "Enterprise Journal Reports", hasCount: false },
            { id: "smart_view", label: "Smart View Reports", hasCount: true }
        ]
    },
    {
        title: "Automations",
        items: [
            { id: "auto_load", label: "Automated Data Loads", hasCount: false },
            { id: "auto_consol", label: "Automated Consolidations", hasCount: false },
            { id: "backup", label: "Backup and Archival", hasCount: false },
            { id: "meta_imp", label: "Metadata Import", hasCount: false }
        ]
    },
    {
        title: "Testing / Training",
        items: [
            { id: "unit_test", label: "Unit Testing", hasCount: false },
            { id: "uat", label: "UAT", hasCount: false },
            { id: "sit", label: "SIT", hasCount: false },
            { id: "par_test", label: "Parallel Testing", hasCount: true },
            { id: "user_train", label: "User Training", hasCount: false }
        ]
    },
    {
        title: "Transition",
        items: [
            { id: "go_live", label: "Go Live", hasCount: false },
            { id: "hypercare", label: "Hypercare", hasCount: false }
        ]
    },
    {
        title: "Documentations",
        items: [
            { id: "rtm", label: "RTM", hasCount: false },
            { id: "design_doc", label: "Design Document", hasCount: false },
            { id: "sys_config", label: "System Configuration Document", hasCount: false }
        ]
    },
    {
        title: "Change Management",
        items: [
            { id: "admin_proc", label: "Admin Desktop Procedures", hasCount: false },
            { id: "end_user_proc", label: "End User Desktop Procedures", hasCount: false }
        ]
    },
    {
        title: "Project Management",
        items: [
            { id: "proj_mgmt", label: "Project Management", hasCount: false }
        ]
    }
];