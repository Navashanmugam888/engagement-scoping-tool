'use client';
import React, { useState, useEffect, useRef } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Tag } from 'primereact/tag';
import { Toast } from 'primereact/toast';
import { ProgressSpinner } from 'primereact/progressspinner';
import { Dialog } from 'primereact/dialog';
import { ProgressBar } from 'primereact/progressbar';
import { Avatar } from 'primereact/avatar';

// Helper component for Stat Cards
const StatCard = ({ title, value, subtext, icon, color = "text-[#443575]" }) => (
    <div className="bg-white p-4 rounded-lg border border-gray-100 shadow-sm flex items-start justify-between hover:shadow-md transition-shadow duration-200">
        <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">{title}</p>
            <h3 className="text-2xl font-bold text-gray-800">{value}</h3>
            {subtext && <p className="text-xs text-gray-500 mt-1">{subtext}</p>}
        </div>
        <div className={`p-3 rounded-full bg-gray-50 ${color}`}>
            <i className={`${icon} text-xl`}></i>
        </div>
    </div>
);

export default function ScopingHistory() {
    const { data: session } = useSession();
    const router = useRouter();
    const toast = useRef(null);
    
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedSubmission, setSelectedSubmission] = useState(null);
    const [showResultDialog, setShowResultDialog] = useState(false);

    useEffect(() => {
        if (session?.user?.email) {
            fetchHistory();
        }
    }, [session]);

    const fetchHistory = async () => {
        try {
            setLoading(true);
            // Call external backend API (configured in .env)
            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:5000';
            const response = await fetch(`${backendUrl}/api/scoping/history?email=${session.user.email}`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch history');
            }
            
            const data = await response.json();
            
            if (data.success || data.submissions) {
                setSubmissions(data.submissions || data);
            } else {
                toast.current?.show({ 
                    severity: 'error', 
                    summary: 'Error', 
                    detail: 'Failed to load history' 
                });
            }
        } catch (error) {
            console.error('Error fetching history:', error);
            toast.current?.show({ 
                severity: 'error', 
                summary: 'Error', 
                detail: error.message || 'Failed to load history' 
            });
        } finally {
            setLoading(false);
        }
    };

    const viewResult = async (submission) => {
        try {
            // Call external backend API (configured in .env)
            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:5000';
            const response = await fetch(`${backendUrl}/api/scoping/result/${submission.id}`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch result');
            }
            
            const data = await response.json();
            
            if (data.success || data.submission) {
                setSelectedSubmission(data.submission || data);
                setShowResultDialog(true);
            }
        } catch (error) {
            console.error('Error fetching result:', error);
            toast.current?.show({ 
                severity: 'error', 
                summary: 'Error', 
                detail: error.message || 'Failed to load result' 
            });
        }
    };

    const downloadReport = async (submissionId) => {
        try {
            console.log('Attempting to download report for:', submissionId);
            
            toast.current?.show({ 
                severity: 'info', 
                summary: 'Downloading', 
                detail: 'Preparing your report...' 
            });

            // Call external backend API (configured in .env)
            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:5000';
            const downloadUrl = `${backendUrl}/api/scoping/download/${submissionId}`;
            console.log('Download URL:', downloadUrl);
            
            const response = await fetch(downloadUrl);
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('Download error data:', errorData);
                
                // Show user-friendly message for missing files
                if (response.status === 404 && errorData.error?.includes('not found')) {
                    throw new Error('Report file not found. This may be an old submission. Please submit your scoping data again to generate a new report.');
                }
                
                throw new Error(errorData.error || `Server returned ${response.status}`);
            }

            // Get the blob
            const blob = await response.blob();
            console.log('Blob size:', blob.size);
            
            // Create a download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scoping_report_${submissionId}.docx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            toast.current?.show({ 
                severity: 'success', 
                summary: 'Success', 
                detail: 'Report downloaded successfully' 
            });
        } catch (error) {
            console.error('Download error:', error);
            toast.current?.show({ 
                severity: 'error', 
                summary: 'Download Failed', 
                detail: error.message || 'Failed to download report',
                life: 6000
            });
        }
    };

    // --- Templates ---

    const dateTemplate = (rowData) => {
        return (
            <div className="flex flex-col">
                <span className="font-medium text-gray-700">
                    {new Date(rowData.submitted_at).toLocaleDateString()}
                </span>
                <span className="text-xs text-gray-500">
                    {new Date(rowData.submitted_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
            </div>
        );
    };

    const statusTemplate = (rowData) => {
        const statusConfig = {
            'COMPLETED': { severity: 'success', icon: 'pi pi-check-circle', label: 'Completed' },
            'PENDING': { severity: 'warning', icon: 'pi pi-spin pi-spinner', label: 'Processing' },
            'FAILED': { severity: 'danger', icon: 'pi pi-times-circle', label: 'Failed' }
        };
        
        const config = statusConfig[rowData.status] || statusConfig['PENDING'];
        return (
            <Tag 
                severity={config.severity} 
                className="px-3 py-1 text-xs"
                icon={config.icon}
                value={config.label}
                rounded
            />
        );
    };

    const actionTemplate = (rowData) => {
        return (
            <div className="flex gap-2 justify-end">
                <Button
                    icon="pi pi-eye"
                    className="p-button-text p-button-secondary p-button-sm hover:bg-[#443575]/10 hover:text-[#443575]"
                    onClick={() => viewResult(rowData)}
                    disabled={rowData.status !== 'COMPLETED'}
                    tooltip="View Details"
                />
                <Button
                    icon="pi pi-download"
                    className="p-button-outlined p-button-success p-button-sm"
                    onClick={() => downloadReport(rowData.id)}
                    disabled={rowData.status !== 'COMPLETED'}
                    tooltip="Download Report"
                />
            </div>
        );
    };

    // --- Dialog Content ---

    const resultDialogContent = () => {
        if (!selectedSubmission) return null;

        const result = selectedSubmission.calculation_result;
        const scopeDef = result?.scope_definition;
        const effortEst = result?.effort_estimation;
        const fteAlloc = result?.fte_allocation;
        
        return (
            <div className="bg-gray-50/50 p-2">
                {/* 1. Executive Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
                    <StatCard 
                        title="Project Tier" 
                        value={scopeDef?.tier_name || 'N/A'} 
                        icon="pi pi-tag"
                        subtext={`Range: ${scopeDef?.tier_range?.[0]} - ${scopeDef?.tier_range?.[1]}`}
                    />
                    <StatCard 
                        title="Total Effort" 
                        value={`${effortEst?.summary?.total_time_hours?.toFixed(0) || 0} hrs`}
                        subtext={`Approx. ${effortEst?.summary?.total_days?.toFixed(0) || 0} days`}
                        icon="pi pi-clock"
                        color="text-blue-600"
                    />
                    <StatCard 
                        title="Duration" 
                        value={`${effortEst?.summary?.total_months?.toFixed(1) || 0} mo`}
                        subtext="Estimated Timeline"
                        icon="pi pi-calendar"
                        color="text-orange-600"
                    />
                    <StatCard 
                        title="Resource Count" 
                        value={scopeDef?.selected_roles?.length || 0}
                        subtext="Unique Roles"
                        icon="pi pi-users"
                        color="text-green-600"
                    />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                    {/* 2. FTE Allocation (Takes up 2 columns) */}
                    <div className="lg:col-span-2 space-y-4">
                        {fteAlloc && fteAlloc.by_role && (
                            <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
                                <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                                    <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                                        <i className="pi pi-chart-bar text-[#443575]"></i> Resource Allocation
                                    </h3>
                                    <span className="text-xs font-medium bg-indigo-50 text-[#443575] px-2 py-1 rounded">
                                        {fteAlloc.total_hours?.toFixed(0)} Total Hours
                                    </span>
                                </div>
                                <DataTable 
                                    value={Object.entries(fteAlloc.by_role).map(([role, data]) => ({
                                        role,
                                        hours: data.hours,
                                        percentage: ((data.hours / fteAlloc.total_hours) * 100)
                                    }))}
                                    className="p-datatable-sm custom-table"
                                    stripedRows
                                >
                                    <Column field="role" header="Role" className="font-medium text-gray-700" />
                                    <Column field="hours" header="Hours" align="right" body={d => d.hours.toFixed(1)} />
                                    <Column 
                                        field="percentage" 
                                        header="Allocation %" 
                                        body={(d) => (
                                            <div className="flex items-center gap-3">
                                                <ProgressBar value={d.percentage} showValue={false} style={{ height: '6px', width: '60px' }} color="#443575"></ProgressBar>
                                                <span className="text-xs text-gray-500 w-8">{d.percentage.toFixed(1)}%</span>
                                            </div>
                                        )} 
                                    />
                                </DataTable>
                            </div>
                        )}

                        {/* 3. Effort Breakdown */}
                        {effortEst && effortEst.categories && (
                            <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
                                <div className="px-6 py-4 border-b border-gray-100 bg-gray-50">
                                    <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                                        <i className="pi pi-list text-[#443575]"></i> Effort Breakdown
                                    </h3>
                                </div>
                                <DataTable 
                                    value={Object.entries(effortEst.categories)
                                        .map(([cat, hrs]) => ({ category: cat, hours: Number(hrs) }))
                                        .sort((a, b) => b.hours - a.hours)
                                    }
                                    className="p-datatable-sm"
                                    stripedRows
                                    paginator
                                    rows={5}
                                >
                                    <Column field="category" header="Category" />
                                    <Column 
                                        field="hours" 
                                        header="Hours" 
                                        align="right" 
                                        body={d => <span className="font-mono text-sm">{d.hours.toFixed(1)}</span>} 
                                    />
                                </DataTable>
                            </div>
                        )}
                    </div>

                    {/* 4. Sidebar (Scope Summary & Meta) */}
                    <div className="space-y-4">
                         {/* Scope Summary */}
                         <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-5">
                            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wide mb-4 border-b pb-2">Scope Metrics</h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600 text-sm">Weightage</span>
                                    <span className="font-bold text-gray-900">{scopeDef?.total_weightage}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600 text-sm">In Scope Items</span>
                                    <Tag severity="success" value={scopeDef?.summary?.in_scope_count} rounded />
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600 text-sm">Out of Scope</span>
                                    <Tag severity="warning" value={scopeDef?.summary?.out_of_scope_count} rounded />
                                </div>
                            </div>

                            {scopeDef?.selected_roles && (
                                <div className="mt-6">
                                    <p className="text-xs text-gray-500 mb-2">Required Roles</p>
                                    <div className="flex flex-wrap gap-2">
                                        {scopeDef.selected_roles.map((role, idx) => (
                                            <span key={idx} className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded border border-gray-200">
                                                {role}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Submission Metadata */}
                        <div className="bg-[#443575]/5 border border-[#443575]/10 rounded-lg p-5">
                            <h3 className="text-sm font-bold text-[#443575] uppercase tracking-wide mb-3">Submission Info</h3>
                            <div className="flex items-center gap-3 mb-4">
                                <Avatar label={selectedSubmission.user_name?.charAt(0)} shape="circle" className="bg-[#443575] text-white" />
                                <div>
                                    <p className="text-sm font-medium text-gray-900">{selectedSubmission.user_name}</p>
                                    <p className="text-xs text-gray-500">Submitter</p>
                                </div>
                            </div>
                            <div className="text-xs text-gray-600 bg-white p-3 rounded border border-gray-200">
                                <span className="block font-semibold mb-1">Comments:</span>
                                {selectedSubmission.comments || "No comments provided."}
                            </div>
                            <Button 
                                label="Download Full Report" 
                                icon="pi pi-file-pdf" 
                                className="w-full mt-4 p-button-sm"
                                style={{ backgroundColor: '#443575', borderColor: '#443575' }}
                                onClick={() => downloadReport(selectedSubmission.submission_id)}
                            />
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="text-center">
                    <ProgressSpinner style={{width: '50px', height: '50px'}} strokeWidth="4" animationDuration=".5s" />
                    <p className="text-gray-500 mt-4 text-sm">Loading history...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50/50 p-4 font-sans">
            <Toast ref={toast} />
            
            <div className="max-w-full mx-auto space-y-4">
                {/* Page Header */}
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900">Scoping History</h1>
                        <p className="text-gray-500 text-sm mt-1">Track project estimations and resource allocations</p>
                    </div>
                </div>

                {/* Main Data Table */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                    <DataTable 
                        value={submissions} 
                        paginator 
                        rows={10}
                        emptyMessage={
                            <div className="text-center py-8">
                                <i className="pi pi-folder-open text-gray-300 text-4xl mb-3"></i>
                                <p className="text-gray-500">No submissions found.</p>
                            </div>
                        }
                        className="p-datatable-lg header-transparent"
                        stripedRows
                        rowHover
                        pt={{
                            header: { className: 'bg-white border-b border-gray-200' },
                            thead: { className: 'bg-gray-50 text-gray-600 text-sm' }
                        }}
                    >
                        <Column 
                            field="submitted_at" 
                            header="Date Submitted" 
                            body={dateTemplate}
                            sortable
                            style={{ width: '20%' }}
                        />
                        <Column 
                            field="tier" 
                            header="Calculated Tier" 
                            body={(rowData) => <span className="font-semibold text-[#443575]">{rowData.tier}</span>}
                        />
                        <Column 
                            field="total_hours" 
                            header="Effort (Hrs)" 
                            body={(rowData) => <span className="font-mono text-sm">{rowData.total_hours?.toFixed(0)}</span>}
                            align="right"
                        />
                         <Column 
                            field="status" 
                            header="Status" 
                            body={statusTemplate}
                            align="center"
                        />
                        <Column 
                            header="" 
                            body={actionTemplate}
                            align="right"
                        />
                    </DataTable>
                </div>
            </div>

            {/* Results Modal */}
            <Dialog
                header={
                    <div className="flex items-center gap-3 pb-2 border-b border-gray-100">
                        <div className="bg-[#443575]/10 p-2 rounded-lg">
                            <i className="pi pi-chart-pie text-xl text-[#443575]"></i>
                        </div>
                        <div>
                            <h2 className="text-lg font-bold text-gray-800">Scoping Analysis Result</h2>
                            <p className="text-xs text-gray-500 font-normal">Ref ID: {selectedSubmission?.submission_id}</p>
                        </div>
                    </div>
                }
                visible={showResultDialog}
                style={{ width: '95vw', maxWidth: '1400px' }}
                maximizableStyle={{ width: '100vw', height: '100vh', maxWidth: '100vw', margin: 0 }}
                onHide={() => setShowResultDialog(false)}
                modal
                maximizable
                contentStyle={{ padding: '1.5rem', overflow: 'auto' }}
                className="custom-dialog"
            >
                {resultDialogContent()}
            </Dialog>

            {/* Global Styles helper (if you don't have these in global css) */}
            <style jsx global>{`
                .p-datatable .p-datatable-thead > tr > th {
                    background: #f9fafb;
                    color: #4b5563;
                    font-weight: 600;
                    padding: 1rem;
                }
                .p-datatable .p-datatable-tbody > tr > td {
                    padding: 1rem;
                    border-bottom: 1px solid #f3f4f6;
                }
                .p-progressbar .p-progressbar-value {
                    background: #443575;
                }
                .p-dialog-header {
                    border-top-left-radius: 12px;
                    border-top-right-radius: 12px;
                }
                
                /* Fullscreen dialog styles */
                .p-dialog-maximized {
                    width: 100vw !important;
                    height: 100vh !important;
                    max-width: 100vw !important;
                    max-height: 100vh !important;
                    top: 0 !important;
                    left: 0 !important;
                    margin: 0 !important;
                    border-radius: 0 !important;
                }
                
                .p-dialog-maximized .p-dialog-content {
                    height: calc(100vh - 120px) !important;
                    overflow-y: auto !important;
                }
            `}</style>
        </div>
    );
}