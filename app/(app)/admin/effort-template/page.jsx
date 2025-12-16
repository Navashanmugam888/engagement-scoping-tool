'use client';
import { useEffect, useState, useRef } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { InputNumber } from 'primereact/inputnumber';
import CalculateOutlinedIcon from '@mui/icons-material/CalculateOutlined';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';

export default function EffortTemplate() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const toast = useRef(null);
  const [effortData, setEffortData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedRows, setExpandedRows] = useState({});

  // Complete effort template data with ALL subtasks from backend
  const initialEffortData = [
    {
      id: 1,
      category: 'Project Initiation and Planning',
      total: 12,
      subtasks: [
        { name: 'Kickoff Meetings', hours: 1 },
        { name: 'Project Governance', hours: 1 },
        { name: 'Communication Plan', hours: 1 },
        { name: 'Resource Allocation', hours: 2 },
        { name: 'RAID Log', hours: 1 },
        { name: 'Project Plan', hours: 4 },
        { name: 'Plan Status Meetings and SteerCo Meeting Schedule', hours: 2 }
      ]
    },
    {
      id: 2,
      category: 'Creating and Managing EPM Cloud Infrastructure',
      total: 6,
      subtasks: [
        { name: 'Creating and Setting up Oracle EPM Cloud instances', hours: 2 },
        { name: 'Prelim FCC User Provisioning', hours: 4 }
      ]
    },
    {
      id: 3,
      category: 'Requirement Gathering, Read back and Client Sign-off',
      total: 32,
      subtasks: [
        { name: 'Requirement Gathering Sessions', hours: 8 },
        { name: 'Current CoA details', hours: 4 },
        { name: 'CoA Hierarchies', hours: 4 },
        { name: 'Current Consolidation Model', hours: 4 },
        { name: 'Sample Reports', hours: 2 },
        { name: 'Dimension Details', hours: 4 },
        { name: 'Develop Requirement Traceability Matrix', hours: 4 },
        { name: 'Formal RTM Signoff', hours: 2 }
      ]
    },
    {
      id: 4,
      category: 'Design',
      total: 26,
      subtasks: [
        { name: 'Design Document', hours: 8 },
        { name: 'Key Design Decision Document', hours: 8 },
        { name: 'Internal Peer Review', hours: 4 },
        { name: 'Design and KDD Reviews', hours: 4 },
        { name: 'Design Approval from Client', hours: 2 }
      ]
    },
    {
      id: 5,
      category: 'Build and Configure FCC',
      total: 88,
      subtasks: [
        { name: 'Application Configuration', hours: 2 },
        { name: 'Account', hours: 16 },
        { name: 'Account Alternate Hierarchies', hours: 8 },
        { name: 'Rationalization of CoA', hours: 24 },
        { name: 'Multi Currency', hours: 1 },
        { name: 'Reporting Currency', hours: 0.5 },
        { name: 'Data Source', hours: 0.5 },
        { name: 'Entity', hours: 8 },
        { name: 'Entity Redesign', hours: 8 },
        { name: 'Entity Alternate Hierarchies', hours: 4 },
        { name: 'Movement', hours: 4 },
        { name: 'Scenario', hours: 1 },
        { name: 'Multi-GAAP', hours: 2 },
        { name: 'Custom Dimensions', hours: 4 },
        { name: 'Alternate Hierarchies in Custom Dimensions', hours: 4 },
        { name: 'Additional Alias Tables', hours: 1 }
      ]
    },
    {
      id: 6,
      category: 'Setup Application Features',
      total: 79.5,
      subtasks: [
        { name: 'Elimination', hours: 0.5 },
        { name: 'Consolidation Journals', hours: 1 },
        { name: 'Journal Templates', hours: 1 },
        { name: 'Ownership Management', hours: 4 },
        { name: 'Enhanced Organization by Period', hours: 4 },
        { name: 'Equity Pickup', hours: 8 },
        { name: 'Partner Elimination', hours: 8 },
        { name: 'Configurable Consolidation Rules', hours: 8 },
        { name: 'Cash Flow', hours: 8 },
        { name: 'Supplemental Data Collection', hours: 8 },
        { name: 'Enterprise Journals', hours: 8 },
        { name: 'Approval Process', hours: 8 },
        { name: 'Historic Overrides', hours: 4 },
        { name: 'Task Manager', hours: 8 },
        { name: 'Audit', hours: 1 }
      ]
    },
    {
      id: 7,
      category: 'Application Customization',
      total: 8,
      subtasks: [
        { name: 'Data Forms', hours: 4 },
        { name: 'Dashboards', hours: 4 }
      ]
    },
    {
      id: 8,
      category: 'Calculations',
      total: 15,
      subtasks: [
        { name: 'Business Rules', hours: 8 },
        { name: 'Member Formula', hours: 1 },
        { name: 'Ratios', hours: 4 },
        { name: 'Custom KPIs', hours: 2 }
      ]
    },
    {
      id: 9,
      category: 'Security',
      total: 4,
      subtasks: [
        { name: 'Secured Dimensions', hours: 2 },
        { name: 'Number of Users', hours: 2 }
      ]
    },
    {
      id: 10,
      category: 'Historical Data',
      total: 60,
      subtasks: [
        { name: 'Historical Data Validation', hours: 0 },
        { name: 'Data Validation for Account Alt Hierarchies', hours: 20 },
        { name: 'Data Validation for Entity Alt Hierarchies', hours: 20 },
        { name: 'Historical Journal Conversion', hours: 20 }
      ]
    },
    {
      id: 11,
      category: 'Integrations',
      total: 80,
      subtasks: [
        { name: 'Files Based Loads', hours: 16 },
        { name: 'Direct Connect Integrations', hours: 16 },
        { name: 'Outbound Integrations', hours: 16 },
        { name: 'Pipeline', hours: 16 },
        { name: 'Custom Scripting', hours: 16 }
      ]
    },
    {
      id: 12,
      category: 'Reporting',
      total: 40,
      subtasks: [
        { name: 'Management Reports', hours: 8 },
        { name: 'Consolidation Reports', hours: 4 },
        { name: 'Consolidation Journal Reports', hours: 4 },
        { name: 'Intercompany Reports', hours: 8 },
        { name: 'Task Manager Reports', hours: 4 },
        { name: 'Enterprise Journal Reports', hours: 4 },
        { name: 'Smart View Reports', hours: 8 }
      ]
    },
    {
      id: 13,
      category: 'Automations',
      total: 52,
      subtasks: [
        { name: 'Automated Data loads', hours: 16 },
        { name: 'Automated Consolidations', hours: 8 },
        { name: 'Backup and Archival', hours: 12 },
        { name: 'Metadata Import', hours: 16 }
      ]
    },
    {
      id: 14,
      category: 'Testing/Training',
      total: 152,
      subtasks: [
        { name: 'Unit Testing', hours: 40 },
        { name: 'UAT', hours: 40 },
        { name: 'SIT', hours: 16 },
        { name: 'Parallel Testing', hours: 40 },
        { name: 'User Training', hours: 16 }
      ]
    },
    {
      id: 15,
      category: 'Transition',
      total: 80,
      subtasks: [
        { name: 'Go Live', hours: 40 },
        { name: 'Hypercare', hours: 40 }
      ]
    },
    {
      id: 16,
      category: 'Documentations',
      total: 24,
      subtasks: [
        { name: 'RTM', hours: 8 },
        { name: 'Design Document', hours: 8 },
        { name: 'System Configuration Document', hours: 8 }
      ]
    },
    {
      id: 17,
      category: 'Change Management',
      total: 32,
      subtasks: [
        { name: 'Admin Desktop Procedures', hours: 16 },
        { name: 'End user Desktop Procedures', hours: 16 }
      ]
    }
  ];

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/');
    } else if (status === 'authenticated' && session?.user?.role !== 'SUPER_ADMIN') {
      router.push('/dashboard');
    } else if (status === 'authenticated') {
      setEffortData(initialEffortData);
    }
  }, [status, session, router]);

  const toggleExpand = (id) => {
    setExpandedRows(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const saveTotalHours = async (rowData) => {
    try {
      toast.current?.show({
        severity: 'info',
        summary: 'Saving',
        detail: 'Updating effort hours...'
      });

      // TODO: Connect to backend API endpoint
      toast.current?.show({
        severity: 'success',
        summary: 'Success',
        detail: `Updated ${rowData.category}`
      });
    } catch (error) {
      console.error('Error saving effort template:', error);
      toast.current?.show({
        severity: 'error',
        summary: 'Error',
        detail: 'Failed to save effort template'
      });
    }
  };



  const getTotalBaselineHours = () => {
    return effortData.reduce((sum, item) => sum + (item.total || 0), 0);
  };

  const rowExpansionTemplate = (rowData) => {
    if (!expandedRows[rowData.id]) return null;

    const subtotal = rowData.subtasks.reduce((sum, st) => sum + st.hours, 0);

    return (
      <div className="p-6 bg-gradient-to-r from-gray-50 to-gray-100 border-t-2 border-[#443575]">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-6 bg-[#443575] rounded"></div>
          <h4 className="font-bold text-gray-800 text-lg">Subtasks Breakdown</h4>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {rowData.subtasks.map((subtask, idx) => (
            <div 
              key={idx} 
              className="p-3 bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md hover:border-[#443575] transition-all"
            >
              <div className="flex justify-between items-start gap-2">
                <div className="flex-1">
                  <p className="text-gray-700 font-medium text-sm">{subtask.name}</p>
                </div>
                <span className="px-2 py-1 bg-[#443575] text-white rounded text-xs font-semibold whitespace-nowrap">
                  {subtask.hours} hrs
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 pt-4 border-t border-gray-300 flex justify-between items-center bg-white px-4 py-3 rounded-lg">
          <span className="text-gray-600 font-semibold">Subtotal:</span>
          <span className="text-xl font-bold text-[#443575]">{subtotal} hours</span>
        </div>

        {subtotal === rowData.total ? (
          <div className="mt-3 p-2 bg-green-50 border border-green-200 rounded text-xs text-green-800">
            ✓ Subtasks total matches category total ({rowData.total} hrs)
          </div>
        ) : (
          <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
            ⚠ Subtasks total ({subtotal} hrs) differs from category total ({rowData.total} hrs)
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#443575] mx-auto"></div>
          <p className="text-gray-500 mt-4 text-sm">Loading effort template...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <Toast ref={toast} />

      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
          <CalculateOutlinedIcon style={{ fontSize: 32, color: '#443575' }} />
          Effort Estimation Template
        </h1>
        <p className="text-gray-600">
          Manage baseline effort hours including all subtasks for each engagement activity
        </p>
      </div>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
        {/* Data Table with Expandable Rows */}
        <div className="space-y-0">
          {effortData.map((rowData) => (
            <div key={rowData.id}>
              {/* Row */}
              <div className="flex items-center bg-white border border-gray-200 hover:bg-gray-50 transition-colors">
                <div className="flex-1 flex items-center gap-4 p-4">
                  <div className="flex items-center gap-2 flex-1">
                    <button
                      onClick={() => toggleExpand(rowData.id)}
                      className="p-1 hover:bg-gray-100 rounded transition-colors flex-shrink-0"
                    >
                      {expandedRows[rowData.id] ? (
                        <ExpandMoreIcon fontSize="small" />
                      ) : (
                        <ChevronRightIcon fontSize="small" />
                      )}
                    </button>
                    <span className="font-semibold text-gray-800">{rowData.category}</span>
                  </div>
                  <div className="flex-shrink-0 flex items-center gap-4">
                    <span className="font-bold text-[#443575] text-lg">{rowData.total} hrs</span>
                    <Button
                      icon="pi pi-save"
                      className="p-button-rounded p-button-text p-button-success p-button-sm hover:text-green-600"
                      onClick={() => saveTotalHours(rowData)}
                      tooltip="Save Changes"
                      tooltipPosition="top"
                    />
                  </div>
                </div>
              </div>

              {/* Expanded Content */}
              {expandedRows[rowData.id] && rowExpansionTemplate(rowData)}
            </div>
          ))}
        </div>

        {/* Footer Info */}
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Note:</strong> These baseline hours include all subtasks and are used as the foundation for effort estimation. 
            Hours are adjusted based on tier weightage and scope requirements during the scoping process. Click the expand icon to view subtasks.
          </p>
        </div>
      </div>
    </div>
  );
}
