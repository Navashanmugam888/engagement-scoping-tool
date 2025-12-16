'use client';
import { useEffect, useState, useRef } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { InputText } from 'primereact/inputtext';
import CalculateOutlinedIcon from '@mui/icons-material/CalculateOutlined';
import AdminPanelSettingsOutlinedIcon from '@mui/icons-material/AdminPanelSettingsOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';

export default function ManageScoping() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const toast = useRef(null);
  const [tierData, setTierData] = useState([]);
  const [tierThresholds, setTierThresholds] = useState([]);
  const [availableRoles, setAvailableRoles] = useState([]);
  const [expandedEffortCategories, setExpandedEffortCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(0);

  // Role columns - mapped from backend APP_TIERS_ROLES
  const roles = [
    { field: 'pm1', header: 'PM USA', backendName: 'PM USA' },
    { field: 'pm2', header: 'PM India', backendName: 'PM India' },
    { field: 'architect', header: 'Architect USA', backendName: 'Architect USA' },
    { field: 'srDeliveryLead', header: 'Sr. Delivery Lead India', backendName: 'Sr. Delivery Lead India' },
    { field: 'deliveryLead', header: 'Delivery Lead India', backendName: 'Delivery Lead India' },
    { field: 'appLead1', header: 'App Lead USA', backendName: 'App Lead USA' },
    { field: 'appLead2', header: 'App Lead India', backendName: 'App Lead India' },
    { field: 'appDeveloper1', header: 'App Developer USA', backendName: 'App Developer USA' },
    { field: 'appDeveloper2', header: 'App Developer India', backendName: 'App Developer India' },
    { field: 'integrationLead', header: 'Integration Lead USA', backendName: 'Integration Lead USA' },
    { field: 'integrationDeveloper', header: 'Integration Developer India', backendName: 'Integration Developer India' },
    { field: 'reportingLead', header: 'Reporting Lead India', backendName: 'Reporting Lead India' },
    { field: 'securityLead', header: 'Security Lead India', backendName: 'Security Lead India' }
  ];

  // Initial data from your Excel table with effort template
  const initialData = [
    { activity: 'Project Initiation and Planning', total_hours: 12, pm1: 50, pm2: 50, architect: 100, srDeliveryLead: 50, deliveryLead: 50, appLead1: 0, appLead2: 0, appDeveloper1: 0, appDeveloper2: 0, integrationLead: 0, integrationDeveloper: 0, reportingLead: 0, securityLead: 0 },
    { activity: 'Creating and Managing EPM Cloud Infrastructure', total_hours: 6, pm1: 50, pm2: 50, architect: 0, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 0, appDeveloper2: 0, integrationLead: 0, integrationDeveloper: 0, reportingLead: 0, securityLead: 0 },
    { activity: 'Requirement Gathering, Read back and Client Sign-off', total_hours: 32, pm1: 50, pm2: 50, architect: 100, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 0, appDeveloper2: 0, integrationLead: 20, integrationDeveloper: 20, reportingLead: 0, securityLead: 0 },
    { activity: 'Design', total_hours: 26, pm1: 50, pm2: 50, architect: 100, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 0, appDeveloper2: 0, integrationLead: 20, integrationDeveloper: 20, reportingLead: 0, securityLead: 0 },
    { activity: 'Build and Configure FCC', total_hours: 88, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 0, integrationDeveloper: 0, reportingLead: 0, securityLead: 0 },
    { activity: 'Setup Application Features', total_hours: 79.5, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 0, integrationDeveloper: 0, reportingLead: 0, securityLead: 0 },
    { activity: 'Application Customization', total_hours: 8, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 0, integrationDeveloper: 0, reportingLead: 0, securityLead: 0 },
    { activity: 'Calculations', total_hours: 15, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 0, integrationDeveloper: 0, reportingLead: 0, securityLead: 0 },
    { activity: 'Security', total_hours: 4, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 20, integrationDeveloper: 20, reportingLead: 0, securityLead: 100 },
    { activity: 'Historical Data', total_hours: 60, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 0, integrationDeveloper: 0, reportingLead: 0, securityLead: 0 },
    { activity: 'Integrations', total_hours: 80, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 100, integrationDeveloper: 100, reportingLead: 0, securityLead: 0 },
    { activity: 'Reporting', total_hours: 40, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 0, integrationDeveloper: 0, reportingLead: 100, securityLead: 0 },
    { activity: 'Automations', total_hours: 52, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 100, integrationDeveloper: 100, reportingLead: 0, securityLead: 0 },
    { activity: 'Testing/Training', total_hours: 152, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 50, integrationDeveloper: 50, reportingLead: 20, securityLead: 0 },
    { activity: 'Transition', total_hours: 80, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 50, integrationDeveloper: 50, reportingLead: 0, securityLead: 0 },
    { activity: 'Documentations', total_hours: 24, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 50, integrationDeveloper: 50, reportingLead: 0, securityLead: 0 },
    { activity: 'Change Management', total_hours: 32, pm1: 50, pm2: 50, architect: 20, srDeliveryLead: 50, deliveryLead: 50, appLead1: 100, appLead2: 100, appDeveloper1: 100, appDeveloper2: 100, integrationLead: 50, integrationDeveloper: 50, reportingLead: 0, securityLead: 0 }
  ];

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/');
    } else if (status === 'authenticated' && session?.user?.role !== 'SUPER_ADMIN') {
      router.push('/dashboard');
    } else if (status === 'authenticated') {
      fetchTemplateData();
    }
  }, [status, session, router]);

  const fetchTemplateData = async () => {
    try {
      console.log('Fetching template data from backend...');
      const response = await fetch('/api/admin/role-allocations');
      const data = await response.json();
      
      if (data.success) {
        console.log('Data loaded from backend:', data);
        console.log('Total categories received:', data.tierData.length);
        
        // Log detailed info about each category
        data.tierData.forEach((tier, idx) => {
          console.log(`Category ${idx}: "${tier.activity}"`, {
            total_hours: tier.total_hours,
            subtasks_count: Object.keys(tier.subtasks || {}).length,
            subtasks: tier.subtasks
          });
        });
        
        setTierData(data.tierData);
        setTierThresholds(data.tierThresholds);
        setAvailableRoles(data.availableRoles);
        // Expand first category by default for effort template
        setExpandedEffortCategories([0]);
      } else {
        console.warn('Failed to fetch data, using defaults');
        setTierData(initialData);
        setTierThresholds([
          { tier: 'Tier 1 - Jumpstart', minWeightage: 0, maxWeightage: 60 },
          { tier: 'Tier 2 - Foundation Plus', minWeightage: 61, maxWeightage: 100 },
          { tier: 'Tier 3 - Enhanced Scope', minWeightage: 101, maxWeightage: 150 },
          { tier: 'Tier 4 - Advanced Enablement', minWeightage: 151, maxWeightage: 200 },
          { tier: 'Tier 5 - Full Spectrum', minWeightage: 201, maxWeightage: 999 }
        ]);
        setAvailableRoles([
          { id: 1, roleName: 'PM USA', location: 'USA' },
          { id: 2, roleName: 'PM India', location: 'India' },
          { id: 3, roleName: 'Architect USA', location: 'USA' },
          { id: 4, roleName: 'Sr. Delivery Lead USA', location: 'USA' },
          { id: 5, roleName: 'Delivery Lead India', location: 'India' },
          { id: 6, roleName: 'App Lead USA', location: 'USA' },
          { id: 7, roleName: 'App Lead India', location: 'India' },
          { id: 8, roleName: 'App Developer USA', location: 'USA' },
          { id: 9, roleName: 'App Developer India', location: 'India' },
          { id: 10, roleName: 'Integration Lead USA', location: 'USA' },
          { id: 11, roleName: 'Integration Developer India', location: 'India' },
          { id: 12, roleName: 'Reporting Lead USA', location: 'USA' },
          { id: 13, roleName: 'Security Lead USA', location: 'USA' }
        ]);
      }
    } catch (error) {
      console.error('Error fetching template data:', error);
      setTierData(initialData);
      setTierThresholds([
        { tier: 'Tier 1 - Jumpstart', minWeightage: 0, maxWeightage: 60 },
        { tier: 'Tier 2 - Foundation Plus', minWeightage: 61, maxWeightage: 100 },
        { tier: 'Tier 3 - Enhanced Scope', minWeightage: 101, maxWeightage: 150 },
        { tier: 'Tier 4 - Advanced Enablement', minWeightage: 151, maxWeightage: 200 },
        { tier: 'Tier 5 - Full Spectrum', minWeightage: 201, maxWeightage: 999 }
      ]);
      setAvailableRoles([
        { id: 1, roleName: 'PM USA', location: 'USA' },
        { id: 2, roleName: 'PM India', location: 'India' },
        { id: 3, roleName: 'Architect USA', location: 'USA' },
        { id: 4, roleName: 'Sr. Delivery Lead USA', location: 'USA' },
        { id: 5, roleName: 'Delivery Lead India', location: 'India' },
        { id: 6, roleName: 'App Lead USA', location: 'USA' },
        { id: 7, roleName: 'App Lead India', location: 'India' },
        { id: 8, roleName: 'App Developer USA', location: 'USA' },
        { id: 9, roleName: 'App Developer India', location: 'India' },
        { id: 10, roleName: 'Integration Lead USA', location: 'USA' },
        { id: 11, roleName: 'Integration Developer India', location: 'India' },
        { id: 12, roleName: 'Reporting Lead USA', location: 'USA' },
        { id: 13, roleName: 'Security Lead USA', location: 'USA' }
      ]);
    }
  };

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/');
    } else if (status === 'authenticated' && session?.user?.role !== 'SUPER_ADMIN') {
      router.push('/dashboard');
    } else if (status === 'authenticated') {
      fetchTemplateData();
    }
  }, [status, session, router]);

  const onRowEditComplete = (e) => {
    let _tierData = [...tierData];
    let { newData, index } = e;
    _tierData[index] = newData;
    setTierData(_tierData);
    toast.current?.show({ severity: 'success', summary: 'Success', detail: 'Row updated successfully', life: 3000 });
  };

  const cellEditor = (options) => {
    return (
      <InputText
        type="text"
        value={options.value}
        onChange={(e) => options.editorCallback(e.target.value)}
        className="w-full p-1 text-xs"
      />
    );
  };

  const percentageTemplate = (rowData, column) => {
    return <span className="text-xs">{rowData[column.field]}%</span>;
  };

  const saveAllChanges = async () => {
    setLoading(true);
    try {
      console.log('💾 Saving changes to backend...');
      
      // Extract effort template data from tierData
      // Format: { "Category Name": { "total": sum_of_tasks, "tasks": { "Task": hours, ... } } }
      const effortData = {};
      tierData.forEach((tier) => {
        const categoryName = tier.activity;
        if (categoryName && tier.subtasks) {
          // Calculate total as sum of all subtasks
          const total = Object.values(tier.subtasks).reduce((sum, hours) => sum + (parseFloat(hours) || 0), 0);
          effortData[categoryName] = {
            total: total,
            tasks: tier.subtasks
          };
        }
      });

      console.log('Effort data to save:', effortData);

      const response = await fetch('/api/admin/role-allocations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tierData: tierData,
          tierThresholds: tierThresholds,
          availableRoles: availableRoles,
          effortData: effortData,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Failed to save changes');
      }

      console.log('Save successful, reloading data from backend...');
      
      toast.current?.show({ 
        severity: 'success', 
        summary: 'Success', 
        detail: 'All changes saved to backend successfully', 
        life: 3000 
      });
      
      // Reload data from backend after save (keeps user on current tab)
      setTimeout(() => {
        fetchTemplateData();
      }, 1000);
    } catch (error) {
      console.error('Error saving changes:', error);
      toast.current?.show({ 
        severity: 'error', 
        summary: 'Error', 
        detail: error.message || 'Failed to save changes', 
        life: 3000 
      });
    } finally {
      setLoading(false);
    }
  };

  const onTierEditComplete = (e) => {
    let _tierThresholds = [...tierThresholds];
    let { newData, index } = e;
    _tierThresholds[index] = newData;
    setTierThresholds(_tierThresholds);
    toast.current?.show({ severity: 'success', summary: 'Success', detail: 'Tier threshold updated', life: 3000 });
  };

  const onRoleEditComplete = (e) => {
    let _availableRoles = [...availableRoles];
    let { newData, index } = e;
    _availableRoles[index] = newData;
    setAvailableRoles(_availableRoles);
    toast.current?.show({ severity: 'success', summary: 'Success', detail: 'Role updated', life: 3000 });
  };

  const addNewRole = () => {
    const newRole = {
      id: availableRoles.length + 1,
      roleName: 'New Role',
      location: 'USA'
    };
    setAvailableRoles([...availableRoles, newRole]);
    toast.current?.show({ severity: 'info', summary: 'Role Added', detail: 'Edit the new role details', life: 3000 });
  };

  const deleteRole = (rowData) => {
    const _roles = availableRoles.filter(r => r.id !== rowData.id);
    setAvailableRoles(_roles);
    toast.current?.show({ severity: 'success', summary: 'Deleted', detail: 'Role removed', life: 3000 });
  };

  if (status === 'loading' || !session || session?.user?.role !== 'SUPER_ADMIN') {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2d1b4e]"></div>
      </div>
    );
  }

  return (
    <div className="p-4">
      <Toast ref={toast} />

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <CalculateOutlinedIcon fontSize="large" className="text-[#2d1b4e]" />
            Manage Scoping
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Configure tier definitions and role allocation percentages for scoping calculations
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            label="Manage Users"
            icon="pi pi-users"
            className="p-button-outlined"
            style={{ fontSize: '12px', padding: '8px 16px' }}
            onClick={() => router.push('/admin/users')}
          />
          <Button
            label="Admin Dashboard"
            icon="pi pi-home"
            style={{ fontSize: '10px', padding: '8px 16px', backgroundColor: '#2d1b4e', border: 'none', color: 'white', fontWeight: '400' }}
            onClick={() => router.push('/admin/dashboard')}
          />
        </div>
      </div>

      {/* Info Banner */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-xs text-blue-800">
          <strong>Note:</strong> Configure scoping calculation parameters. Changes will affect all future scoping submissions.
        </p>
      </div>

      {/* Save Button */}
      <div className="mb-4 flex justify-end">
        <Button
          label={loading ? "Saving..." : "Save All Changes"}
          icon={loading ? "pi pi-spin pi-spinner" : "pi pi-save"}
          style={{ backgroundColor: '#2d1b4e', border: 'none', fontSize: '10px', padding: '8px 16px', color: 'white', fontWeight: '400' }}
          onClick={saveAllChanges}
          disabled={loading}
        />
      </div>

      {/* Custom Tab Buttons */}
      <div className="mb-4 flex gap-2 bg-white p-2 rounded-lg border border-gray-200">
        <button
          onClick={() => setActiveTab(0)}
          className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
            activeTab === 0
              ? 'bg-[#2d1b4e] text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Role Allocations
        </button>
        <button
          onClick={() => setActiveTab(1)}
          className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
            activeTab === 1
              ? 'bg-[#2d1b4e] text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Tier Thresholds
        </button>
        <button
          onClick={() => setActiveTab(2)}
          className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
            activeTab === 2
              ? 'bg-[#2d1b4e] text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Available Roles
        </button>
        <button
          onClick={() => setActiveTab(3)}
          className={`px-4 py-2 rounded-lg text-xs font-medium transition-all ${
            activeTab === 3
              ? 'bg-[#2d1b4e] text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <CalculateOutlinedIcon style={{ fontSize: 14, marginRight: '4px', verticalAlign: 'middle' }} />
          Effort Template
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 0 && (
        <div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-x-auto">
            <DataTable
              value={tierData}
              loading={loading}
              editMode="row"
              dataKey="activity"
              onRowEditComplete={onRowEditComplete}
              className="text-xs"
              scrollable
              scrollHeight="600px"
              style={{ fontSize: '11px' }}
            >
              <Column 
                field="activity" 
                header="Activity" 
                style={{ minWidth: '250px', fontWeight: '600' }} 
                frozen
              />
              
              {roles.map((role) => (
                <Column
                  key={role.field}
                  field={role.field}
                  header={role.header}
                  body={percentageTemplate}
                  editor={(options) => cellEditor(options)}
                  style={{ minWidth: '100px', textAlign: 'center' }}
                />
              ))}

              <Column 
                rowEditor 
                headerStyle={{ width: '80px', minWidth: '80px' }} 
                bodyStyle={{ textAlign: 'center' }}
              />
            </DataTable>
          </div>
        </div>
      )}

      {activeTab === 1 && (
        <div>
          <div className="mb-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-xs text-yellow-800">
              <strong>Info:</strong> Tier thresholds determine which tier a project falls into based on total weightage score.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <DataTable
              value={tierThresholds}
              loading={loading}
              editMode="row"
              dataKey="tier"
              onRowEditComplete={onTierEditComplete}
              className="text-xs"
              style={{ fontSize: '11px' }}
            >
              <Column 
                field="tier" 
                header="Tier Name" 
                style={{ minWidth: '300px', fontWeight: '600' }}
              />
              <Column 
                field="minWeightage" 
                header="Min Weightage" 
                editor={(options) => cellEditor(options)}
                style={{ minWidth: '150px' }}
              />
              <Column 
                field="maxWeightage" 
                header="Max Weightage" 
                editor={(options) => cellEditor(options)}
                style={{ minWidth: '150px' }}
              />
              <Column 
                rowEditor 
                headerStyle={{ width: '80px', minWidth: '80px' }} 
                bodyStyle={{ textAlign: 'center' }}
              />
            </DataTable>
          </div>
        </div>
      )}

      {activeTab === 2 && (
        <div>
          <div className="mb-3 flex justify-between items-center">
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg flex-1 mr-3">
              <p className="text-xs text-green-800">
                <strong>Info:</strong> Manage the list of roles available for scoping calculations.
              </p>
            </div>
            <Button
              label="Add New Role"
              icon="pi pi-plus"
              style={{ backgroundColor: 'rgba(22, 163, 74, 0.5)', border: 'none', fontSize: '10px', padding: '8px 16px', color: '#2d1b4e', fontWeight: '500' }}
              onClick={addNewRole}
            />
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <DataTable
              value={availableRoles}
              loading={loading}
              editMode="row"
              dataKey="id"
              onRowEditComplete={onRoleEditComplete}
              className="text-xs"
              style={{ fontSize: '11px' }}
            >
              <Column 
                field="roleName" 
                header="Role Name" 
                editor={(options) => cellEditor(options)}
                style={{ minWidth: '300px', fontWeight: '600' }}
              />
              <Column 
                field="location" 
                header="Location" 
                editor={(options) => cellEditor(options)}
                style={{ minWidth: '150px' }}
              />
              <Column 
                rowEditor 
                headerStyle={{ width: '80px', minWidth: '80px' }} 
                bodyStyle={{ textAlign: 'center' }}
              />
              <Column 
                body={(rowData) => (
                  <Button
                    icon="pi pi-trash"
                    className="p-button-text p-button-sm"
                    onClick={() => deleteRole(rowData)}
                    style={{ fontSize: '10px', color: '#dc2626' }}
                  />
                )}
                headerStyle={{ width: '80px', minWidth: '80px' }} 
                bodyStyle={{ textAlign: 'center' }}
              />
            </DataTable>
          </div>
        </div>
      )}

      {activeTab === 3 && (
        <div>
          <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg mb-3">
            <p className="text-xs text-purple-800">
              <strong>Info:</strong> Manage baseline effort hours for each engagement activity. Expand each category to view and edit subtasks. These hours form the foundation for effort estimation.
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="space-y-2 p-3">
              {tierData.map((category, idx) => (
                <div key={idx} className="border border-gray-200 rounded-lg overflow-hidden">
                  {/* Category Header */}
                  <div className="bg-gradient-to-r from-gray-50 to-gray-100 p-4 cursor-pointer hover:from-gray-100 hover:to-gray-150 transition-colors flex items-center justify-between"
                    onClick={() => {
                      const expandedList = [...expandedEffortCategories];
                      if (expandedList.includes(idx)) {
                        expandedList.splice(expandedList.indexOf(idx), 1);
                      } else {
                        expandedList.push(idx);
                      }
                      setExpandedEffortCategories(expandedList);
                    }}>
                    <div className="flex items-center flex-1 gap-3">
                      <span className={`text-gray-600 transition-transform ${expandedEffortCategories.includes(idx) ? 'rotate-90' : ''}`}>
                        ▶
                      </span>
                      <div className="flex-1">
                        <p className="font-semibold text-gray-800 text-sm">{category.activity}</p>
                        <p className="text-xs text-gray-500">Baseline: {category.total_hours || 0} hours</p>
                      </div>
                    </div>
                    <button className="px-3 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium hover:bg-blue-200 transition-colors"
                      onClick={(e) => {
                        e.stopPropagation();
                        // Edit mode for baseline hours
                      }}>
                      Edit
                    </button>
                  </div>

                  {/* Expanded Category Details */}
                  {expandedEffortCategories.includes(idx) && (
                    <div className="bg-white p-4 border-t border-gray-200">
                      {/* Baseline Hours Row - Auto-calculated from subtasks */}
                      {(() => {
                        // Calculate total from subtasks
                        const calculatedTotal = Object.values(category.subtasks || {}).reduce((sum, hours) => sum + (parseFloat(hours) || 0), 0);
                        
                        // Update category.total_hours if different
                        if (Math.abs((category.total_hours || 0) - calculatedTotal) > 0.01) {
                          setTimeout(() => {
                            const newTierData = [...tierData];
                            newTierData[idx].total_hours = calculatedTotal;
                            setTierData(newTierData);
                          }, 0);
                        }
                        
                        return (
                          <div className="mb-4 p-3 bg-purple-50 rounded-lg border border-purple-200">
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="text-xs font-semibold text-gray-700 mb-1">BASELINE HOURS (Auto-calculated from subtasks)</p>
                                <p className="text-2xl font-bold text-purple-700">{calculatedTotal.toFixed(1)}</p>
                                <p className="text-xs text-gray-500 mt-1">Sum of all subtask hours</p>
                              </div>
                            </div>
                          </div>
                        );
                      })()}
                      

                      {/* Subtasks Table */}
                      <div className="overflow-x-auto">
                        {Object.keys(category.subtasks || {}).length === 0 ? (
                          <div className="text-center py-6 text-gray-500">
                            <p className="text-sm">No subtasks defined for this category</p>
                          </div>
                        ) : (
                          <table className="w-full text-xs border-collapse">
                            <thead>
                              <tr className="bg-gray-100 border-b-2 border-gray-300">
                                <th className="text-left px-3 py-2 font-semibold text-gray-700">Sub-Task</th>
                                <th className="text-right px-3 py-2 font-semibold text-gray-700 w-24">Hours</th>
                                <th className="text-right px-3 py-2 font-semibold text-gray-700 w-20">% of Total</th>
                                <th className="text-center px-3 py-2 font-semibold text-gray-700 w-16">Action</th>
                              </tr>
                            </thead>
                            <tbody>
                              {Object.entries(category.subtasks || {}).map(([taskName, hours], taskIdx) => (
                                <tr key={taskIdx} className="border-b border-gray-200 hover:bg-gray-50">
                                  <td className="px-3 py-2 text-gray-700">{taskName}</td>
                                  <td className="px-3 py-2 text-right">
                                    <input
                                      type="number"
                                      value={hours || 0}
                                      onChange={(e) => {
                                        const newTierData = [...tierData];
                                        const newSubtasks = { ...category.subtasks };
                                        newSubtasks[taskName] = parseFloat(e.target.value) || 0;
                                        newTierData[idx].subtasks = newSubtasks;
                                        setTierData(newTierData);
                                      }}
                                      className="border border-gray-300 rounded px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 w-20"
                                    />
                                  </td>
                                  <td className="px-3 py-2 text-right font-semibold text-gray-600">
                                    {((hours / (category.total_hours || 1)) * 100).toFixed(1)}%
                                  </td>
                                  <td className="px-3 py-2 text-center">
                                    <button
                                      onClick={() => {
                                        const newTierData = [...tierData];
                                        const newSubtasks = { ...category.subtasks };
                                        delete newSubtasks[taskName];
                                        newTierData[idx].subtasks = newSubtasks;
                                        setTierData(newTierData);
                                      }}
                                      className="text-red-500 hover:text-red-700 text-xs font-semibold"
                                    >
                                      ✕
                                    </button>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        )}
                      </div>

                      {/* Add Subtask Button */}
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <button
                          onClick={() => {
                            const taskName = prompt("Enter sub-task name:");
                            if (taskName) {
                              const newTierData = [...tierData];
                              if (!newTierData[idx].subtasks) {
                                newTierData[idx].subtasks = {};
                              }
                              newTierData[idx].subtasks[taskName] = 0;
                              setTierData(newTierData);
                            }
                          }}
                          className="px-3 py-1 bg-green-100 text-green-700 rounded text-xs font-medium hover:bg-green-200 transition-colors"
                        >
                          + Add Sub-Task
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
