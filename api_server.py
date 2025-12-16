"""
Flask API Server for Engagement Scoping Tool
Bridges Next.js frontend with Python backend
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import json
import os
from datetime import datetime
import traceback

from backend.scoping_engine import ScopingEngine
from backend.config import OUTPUT_DIR, AVAILABLE_ROLES

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Directory to store results JSON files
RESULTS_DIR = OUTPUT_DIR / 'results'
RESULTS_DIR.mkdir(exist_ok=True, parents=True)


# Mapping from frontend IDs to backend names (matching Excel file)
FRONTEND_TO_BACKEND_MAP = {
    # Dimensions
    'account': 'Account',
    'acc_alt_hier': 'Account Alternate Hierarchies',
    'rat_coa': 'Rationalization of CoA',
    'multi_curr': 'Multi-Currency',
    'rep_curr': 'Reporting Currency',
    'entity': 'Entity',
    'ent_redesign': 'Entity Redesign',
    'ent_alt_hier': 'Entity Alternate Hierarchies',
    'scenario': 'Scenario',
    'multi_gaap': 'Multi-GAAP',
    'cust_dim': 'Custom Dimensions',
    'alt_hier_cust': 'Alternate Hierarchies in Custom Dimensions',
    'add_alias': 'Additional Alias Tables',
    
    # Application Features
    'elim': 'Elimination',
    'cust_elim': 'Custom Elimination Requirement',
    'consol_journ': 'Consolidation Journals',
    'journ_temp': 'Journal Templates',
    'parent_curr': 'Parent Currency Journals',
    'own_mgmt': 'Ownership Management',
    'enh_org': 'Enhanced Organization by Period',
    'equity_pickup': 'Equity Pickup',
    'partner_elim': 'Partner Elimination',
    'config_consol': 'Configurable Consolidation Rules',
    'cash_flow': 'Cash Flow',
    'supp_data': 'Supplemental Data Collection',
    'ent_journ': 'Enterprise Journals',
    'approval': 'Approval Process',
    'hist_over': 'Historic Overrides',
    'task_mgr': 'Task Manager',
    'audit': 'Audit',
    
    # Application Customization
    'data_forms': 'Data Forms',
    'dashboards': 'Dashboards',
    
    # Calculations
    'bus_rules': 'Business Rules',
    'mem_formula': 'Member Formula',
    'mem_form': 'Member Formula',  # Alternative frontend ID
    'ratios': 'Ratios',
    'cust_kpis': 'Custom KPIs',
    'cust_kpi': 'Custom KPIs',  # Alternative frontend ID
    
    # Security
    'sec_dim': 'Secured Dimensions',
    'num_users': 'Number of Users',
    
    # Historical Data
    'hist_data_val': 'Historical Data Validation',
    'hist_data': 'Historical Data Validation',  # Alternative frontend ID
    'data_val_acc': 'Data Validation for Account Alt Hierarchies',
    'val_acc_alt': 'Data Validation for Account Alt Hierarchies',  # Alternative frontend ID
    'data_val_ent': 'Data Validation for Entity Alt Hierarchies',
    'val_ent_alt': 'Data Validation for Entity Alt Hierarchies',  # Alternative frontend ID
    'hist_journ_conv': 'Historical Journal Conversion',
    'hist_journ': 'Historical Journal Conversion',  # Alternative frontend ID
    
    # Integrations
    'file_loads': 'Files Based Loads',
    'file_load': 'Files Based Loads',  # Alternative frontend ID
    'direct_connect': 'Direct Connect Integrations',
    'direct_conn': 'Direct Connect Integrations',  # Alternative frontend ID
    'outbound_int': 'Outbound Integrations',
    'outbound': 'Outbound Integrations',  # Alternative frontend ID
    'pipeline': 'Pipeline',
    'cust_script': 'Custom Scripting',
    
    # Reporting
    'mgmt_reports': 'Management Reports',
    'mgmt_rep': 'Management Reports',  # Alternative frontend ID
    'consol_reports': 'Consolidation Reports',
    'consol_rep': 'Consolidation Reports',  # Alternative frontend ID
    'consol_journ_reports': 'Consolidation Journal Reports',
    'consol_journ_rep': 'Consolidation Journal Reports',  # Alternative frontend ID
    'ic_reports': 'Intercompany Reports',
    'inter_rep': 'Intercompany Reports',  # Alternative frontend ID
    'task_mgr_reports': 'Task Manager Reports',
    'task_rep': 'Task Manager Reports',  # Alternative frontend ID
    'ent_journ_reports': 'Enterprise Journal Reports',
    'ent_journ_rep': 'Enterprise Journal Reports',  # Alternative frontend ID
    'smart_view': 'Smart View Reports',
    
    # Automations
    'auto_loads': 'Automated Data loads',
    'auto_load': 'Automated Data loads',  # Alternative frontend ID
    'auto_consol': 'Automated Consolidations',
    'backup_arch': 'Backup and Archival',
    'backup': 'Backup and Archival',  # Alternative frontend ID
    'meta_import': 'Metadata Import',
    'meta_imp': 'Metadata Import',  # Alternative frontend ID
    
    # Testing/Training
    'unit_test': 'Unit Testing',
    'uat': 'UAT',
    'sit': 'SIT',
    'parallel_test': 'Parallel Testing',
    'par_test': 'Parallel Testing',  # Alternative frontend ID
    'user_train': 'User Training',
    
    # Transition
    'go_live': 'Go Live',
    'hypercare': 'Hypercare',
    
    # Documentations
    'rtm': 'RTM',
    'design_doc': 'Design Document',
    'sys_config_doc': 'System Configuration Document',
    'sys_config': 'System Configuration Document',  # Alternative frontend ID
    
    # Change Management
    'admin_desktop': 'Admin Desktop Procedures',
    'admin_proc': 'Admin Desktop Procedures',  # Alternative frontend ID
    'user_desktop': 'End User Desktop Procedures',
    'end_user_proc': 'End User Desktop Procedures',  # Alternative frontend ID
    
    # Project Management
    'proj_mgmt': 'Project Management'
}


def transform_frontend_to_backend_format(scoping_data, selected_roles):
    """
    Transform frontend data format to backend format
    
    Frontend format: { 'scope_item_id': { value: 'YES/NO', count: 123 } }
    Backend format: [{ name: 'Item Name', in_scope: 'YES/NO', details: 123 }]
    """
    scope_inputs = []
    
    for item_id, data in scoping_data.items():
        # Use mapping to get exact name from Excel
        item_name = FRONTEND_TO_BACKEND_MAP.get(item_id)
        
        if not item_name:
            # Fallback: try to clean up the ID
            item_name = item_id.replace('_', ' ').replace('-', ' ').title()
            print(f"Warning: No mapping found for '{item_id}', using fallback: '{item_name}'")
        
        scope_inputs.append({
            'name': item_name,
            'in_scope': data.get('value', 'NO'),
            'details': data.get('count', 0) if data.get('value') == 'YES' else 0
        })
    
    return scope_inputs


def get_user_results_file(user_email):
    """Get the path to user's results JSON file"""
    # Sanitize email for filename
    safe_email = user_email.replace('@', '_at_').replace('.', '_')
    return RESULTS_DIR / f'user_{safe_email}.json'


def load_user_results(user_email):
    """Load user's previous results from JSON file"""
    results_file = get_user_results_file(user_email)
    if results_file.exists():
        try:
            with open(results_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading user results: {e}")
            return []
    return []


def save_user_result(user_email, result_data):
    """Save a new result to user's JSON file"""
    results_file = get_user_results_file(user_email)
    
    # Load existing results
    results = load_user_results(user_email)
    
    # Add new result
    results.append(result_data)
    
    # Save back to file
    try:
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user result: {e}")
        return False


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Engagement Scoping API',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/roles', methods=['GET'])
def get_roles():
    """Get available roles for selection"""
    return jsonify({
        'success': True,
        'roles': AVAILABLE_ROLES
    })


@app.route('/api/scoping/submit', methods=['POST'])
def submit_scoping():
    """
    Process scoping submission and generate results
    
    Expected payload:
    {
        "userEmail": "user@example.com",
        "userName": "John Doe",
        "clientName": "ABC Corp",
        "projectName": "FCCS Implementation",
        "scopingData": { "item-id": { "value": "YES/NO", "count": 123 } },
        "selectedRoles": ["PM USA", "PM India"],
        "comments": "Optional comments",
        "submittedAt": "2025-12-04T..."
    }
    """
    try:
        data = request.json
        
        # Extract data
        user_email = data.get('userEmail')
        user_name = data.get('userName')
        client_name = data.get('clientName', 'N/A')
        project_name = data.get('projectName', 'N/A')
        scoping_data = data.get('scopingData', {})
        selected_roles = data.get('selectedRoles', [])
        comments = data.get('comments', '')
        submitted_at = data.get('submittedAt', datetime.now().isoformat())
        
        # Validate required fields
        if not user_email:
            return jsonify({
                'success': False,
                'error': 'User email is required'
            }), 400
        
        if not scoping_data:
            return jsonify({
                'success': False,
                'error': 'Scoping data is required'
            }), 400
        
        if not selected_roles:
            return jsonify({
                'success': False,
                'error': 'At least one role must be selected'
            }), 400
        
        # Transform frontend data to backend format
        scope_inputs = transform_frontend_to_backend_format(scoping_data, selected_roles)
        
        # Create user input for backend
        user_input = {
            'scope_inputs': scope_inputs,
            'selected_roles': selected_roles
        }
        
        try:
            # Initialize scoping engine
            engine = ScopingEngine()
        except PermissionError as pe:
            print(f"Permission Error: {pe}")
            return jsonify({
                'success': False,
                'error': 'Cannot access Excel file. Please close "Engagement Scoping Tool - FCC.xlsx" in Excel and try again.',
                'details': 'The Excel template file is currently open in another application. Please close it and retry your submission.'
            }), 500
        
        # Process scope
        scope_result = engine.process_scope(user_input)
        
        # Calculate effort
        effort_result = engine.calculate_effort()
        
        # Calculate FTE allocation
        fte_result = engine.calculate_fte_allocation()
        
        # Generate unique filename based on user and timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_email = user_email.replace('@', '_at_').replace('.', '_')
        output_filename = f'scoping_result_{safe_email}_{timestamp}'
        
        # Generate report (JSON + Word)
        report_result = engine.generate_report(output_filename=output_filename)
        
        # Create submission ID from timestamp
        submission_id = f"{safe_email}_{timestamp}"
        
        # Transform effort categories to simple {category: hours} format for frontend
        effort_categories_simple = {}
        if effort_result and 'categories' in effort_result:
            for category, data in effort_result['categories'].items():
                if isinstance(data, dict) and 'final_estimate' in data:
                    effort_categories_simple[category] = data['final_estimate']
                else:
                    effort_categories_simple[category] = 0
        
        # Extract file paths from report_result
        files_data = report_result.get('files', {})
        json_report_path = str(files_data.get('json_report', ''))
        word_report_path = str(files_data.get('word_report', ''))
        
        print(f"DEBUG - Files from report_result:")
        print(f"  JSON: {json_report_path}")
        print(f"  Word: {word_report_path}")
        
        # Prepare result data to store
        result_data = {
            'submission_id': submission_id,
            'user_email': user_email,
            'user_name': user_name,
            'client_name': client_name,
            'project_name': project_name,
            'submitted_at': submitted_at,
            'comments': comments,
            'status': 'COMPLETED',
            'scoping_data': scoping_data,
            'selected_roles': selected_roles,
            'calculation_result': {
                'scope_definition': scope_result,
                'effort_estimation': {
                    'summary': effort_result.get('summary', {}),
                    'categories': effort_categories_simple  # Use simple format
                },
                'fte_allocation': fte_result,
                'tier': scope_result.get('tier_name', 'N/A'),
                'total_weightage': scope_result.get('total_weightage', 0),
                'total_hours': fte_result.get('total_hours', 0),
                'total_days': fte_result.get('total_days', 0),
                'total_months': fte_result.get('total_months', 0),
            },
            'files': {
                'json_report': json_report_path,
                'word_report': word_report_path
            }
        }
        
        # Save to user's results file
        save_success = save_user_result(user_email, result_data)
        
        if not save_success:
            print("Warning: Failed to save result to user file")
        
        # Return response
        # Get the correct total_months from effort_estimation.summary
        effort_summary = effort_result.get('summary', {})
        correct_total_months = effort_summary.get('total_months', 0)
        
        return jsonify({
            'success': True,
            'submission_id': submission_id,
            'message': 'Scoping calculation completed successfully',
            'result': {
                'tier': scope_result.get('tier_name', 'N/A'),
                'weightage': scope_result.get('total_weightage', 0),
                'total_hours': fte_result.get('total_hours', 0),
                'total_days': round(fte_result.get('total_days', 0), 2),
                'total_months': round(correct_total_months, 2),
                'status': 'COMPLETED',
                'effort_summary': {
                    'total_time_hours': effort_summary.get('total_time_hours', 0),
                    'total_days': round(effort_summary.get('total_days', 0), 2),
                    'total_months': round(correct_total_months, 2)
                }
            },
            'files': {
                'json_report': json_report_path,
                'word_report': word_report_path,
                'word_filename': Path(word_report_path).name if word_report_path else ''
            }
        })
        
    except Exception as e:
        print(f"Error processing scoping submission: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'details': traceback.format_exc()
        }), 500


@app.route('/api/scoping/history', methods=['GET'])
def get_scoping_history():
    """
    Get scoping history for a user
    
    Query params:
    - email: user email address
    """
    try:
        user_email = request.args.get('email')
        
        if not user_email:
            return jsonify({
                'success': False,
                'error': 'Email parameter is required'
            }), 400
        
        # Load user results
        results = load_user_results(user_email)
        
        # Format results for frontend
        submissions = []
        for result in results:
            calc_result = result.get('calculation_result', {})
            effort_est = calc_result.get('effort_estimation', {})
            effort_summary = effort_est.get('summary', {})
            
            # Get duration (months) from the same place as detail view uses
            duration_months = effort_summary.get('total_months', 0)
            
            submissions.append({
                'id': result.get('submission_id'),
                'user_name': result.get('user_name'),
                'client_name': result.get('client_name', 'N/A'),
                'project_name': result.get('project_name', 'N/A'),
                'submitted_at': result.get('submitted_at'),
                'status': result.get('status', 'COMPLETED'),
                'tier': calc_result.get('tier', 'N/A'),
                'total_weightage': calc_result.get('total_weightage', 0),
                'total_hours': calc_result.get('total_hours', 0),
                'total_days': calc_result.get('total_days', 0),
                'total_months': duration_months,  # Use the correct duration value
                'comments': result.get('comments', ''),
                'calculation_result': calc_result  # Include full calc_result for backward compatibility
            })
        
        return jsonify({
            'success': True,
            'submissions': submissions
        })
        
    except Exception as e:
        print(f"Error fetching history: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/scoping/result/<submission_id>', methods=['GET'])
def get_scoping_result(submission_id):
    """
    Get detailed result for a specific submission
    """
    try:
        # submission_id format: email_YYYYMMDD_HHMMSS
        # We need to extract everything except the last two parts (date and time)
        parts = submission_id.split('_')
        
        if len(parts) < 3:
            return jsonify({
                'success': False,
                'error': 'Invalid submission ID format'
            }), 400
        
        # Last 2 parts are date and time, everything before is the email
        date_part = parts[-2]  # YYYYMMDD
        time_part = parts[-1]  # HHMMSS
        
        # Check if last two parts look like date and time
        if not (date_part.isdigit() and len(date_part) == 8 and time_part.isdigit() and len(time_part) == 6):
            return jsonify({
                'success': False,
                'error': 'Invalid submission ID format - cannot parse date/time'
            }), 400
        
        # Email is everything except last 2 parts
        email_part = '_'.join(parts[:-2])
        user_email = email_part.replace('_at_', '@').replace('_', '.')
        
        # Load user results
        results = load_user_results(user_email)
        
        # Find specific submission
        submission = None
        for result in results:
            if result.get('submission_id') == submission_id:
                submission = result
                break
        
        if not submission:
            return jsonify({
                'success': False,
                'error': 'Submission not found'
            }), 404
        
        return jsonify({
            'success': True,
            'submission': submission
        })
        
    except Exception as e:
        print(f"Error fetching result: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/scoping/download/<submission_id>', methods=['GET'])
def download_report(submission_id):
    """
    Download Word report for a specific submission
    """
    try:
        # submission_id format: email_YYYYMMDD_HHMMSS
        # We need to extract everything except the last two parts (date and time)
        parts = submission_id.split('_')
        
        if len(parts) < 3:
            return jsonify({
                'success': False,
                'error': 'Invalid submission ID format'
            }), 400
        
        # Last 2 parts are date and time, everything before is the email
        date_part = parts[-2]  # YYYYMMDD
        time_part = parts[-1]  # HHMMSS
        
        # Check if last two parts look like date and time
        if not (date_part.isdigit() and len(date_part) == 8 and time_part.isdigit() and len(time_part) == 6):
            return jsonify({
                'success': False,
                'error': 'Invalid submission ID format - cannot parse date/time'
            }), 400
        
        # Email is everything except last 2 parts
        email_part = '_'.join(parts[:-2])
        user_email = email_part.replace('_at_', '@').replace('_', '.')
        
        print(f"Download request - Submission ID: {submission_id}")
        print(f"Extracted email: {user_email}")
        
        # Load user results
        results = load_user_results(user_email)
        
        print(f"Found {len(results)} results for user")
        
        # Find specific submission
        submission = None
        for result in results:
            if result.get('submission_id') == submission_id:
                submission = result
                break
        
        if not submission:
            return jsonify({
                'success': False,
                'error': f'Submission not found: {submission_id}'
            }), 404
        
        # Get Word report path
        word_report_path = submission.get('files', {}).get('word_report')
        
        print(f"Word report path from submission: {word_report_path}")
        
        # If path is empty or None, try to construct expected filename
        if not word_report_path or word_report_path == '':
            # Try multiple possible filenames
            possible_filenames = [
                f'scoping_result_{submission_id}.docx',  # Current naming
                f'scoping_report_{submission_id}.docx',  # Alternative naming
                # Also try looking for files with similar patterns
            ]
            
            word_report_file = None
            for filename in possible_filenames:
                test_path = OUTPUT_DIR / filename
                print(f"Trying: {test_path}")
                if test_path.exists():
                    word_report_file = test_path
                    print(f"Found file: {word_report_file}")
                    break
            
            # If still not found, list all .docx files and try to match
            if not word_report_file and OUTPUT_DIR.exists():
                print(f"File not found in expected locations, checking all .docx files...")
                all_docx = list(OUTPUT_DIR.glob('*.docx'))
                print(f"Available .docx files: {[f.name for f in all_docx]}")
                
                # Try to find a file that contains the submission ID
                for docx_file in all_docx:
                    if submission_id in docx_file.name:
                        word_report_file = docx_file
                        print(f"Found matching file: {word_report_file}")
                        break
            
            if not word_report_file:
                print(f"File not found, checking directory contents...")
                print(f"Output directory: {OUTPUT_DIR}")
                if OUTPUT_DIR.exists():
                    print(f"Files in output dir: {list(OUTPUT_DIR.glob('*.docx'))}")
                
                return jsonify({
                    'success': False,
                    'error': f'Report file not found. The report may not have been generated. Please try submitting the scoping data again.'
                }), 404
        else:
            word_report_file = Path(word_report_path)
            
        if not word_report_file.exists():
            return jsonify({
                'success': False,
                'error': f'Report file not found at: {word_report_file}. Please regenerate by resubmitting your scoping data.'
            }), 404
        
        print(f"Sending file: {word_report_file}")
        
        # Send file
        return send_file(
            str(word_report_file),
            as_attachment=True,
            download_name=word_report_file.name,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        print(f"Error downloading report: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("="*80)
    print("🚀 Starting Engagement Scoping API Server")
    print("="*80)
    print(f"\n📁 Output Directory: {OUTPUT_DIR}")
    print(f"📁 Results Directory: {RESULTS_DIR}")
    print(f"\n🌐 Server running on: http://localhost:5000")
    print(f"🔗 Health check: http://localhost:5000/health")
    print("\n" + "="*80 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
