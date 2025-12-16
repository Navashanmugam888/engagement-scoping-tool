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

export default function ScopingHistory() {
    const { data: session } = useSession();
    const router = useRouter();
    const toast = useRef(null);
    
    const [submissions, setSubmissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [globalFilter, setGlobalFilter] = useState('');
    const [selectedTier, setSelectedTier] = useState('');
    const [selectedStatus, setSelectedStatus] = useState('');

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
                // Handle non-2xx responses gracefully - set empty submissions
                setSubmissions([]);
                return;
            }
            
            const data = await response.json();
            
            // Handle both { submissions: [...] } and direct array formats
            const submissions = Array.isArray(data.submissions) ? data.submissions : (Array.isArray(data) ? data : []);
            setSubmissions(submissions);
        } catch (error) {
            console.error('Error fetching history:', error);
            // Set empty submissions for new users instead of showing error
            setSubmissions([]);
        } finally {
            setLoading(false);
        }
    };

    const viewResult = async (submission) => {
        // Navigate to detail page instead of showing dialog
        router.push(`/scoping-history/${submission.id}`);
    };

    const downloadReport = async (submissionId) => {
        try {
            console.log('Starting download for submission:', submissionId);
            
            toast.current?.show({ 
                severity: 'info', 
                summary: 'Downloading', 
                detail: 'Preparing your report...' 
            });

            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:5000';
            const downloadUrl = `${backendUrl}/api/scoping/download/${submissionId}`;
            
            console.log('Download URL:', downloadUrl);
            
            const response = await fetch(downloadUrl);
            
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            
            if (!response.ok) {
                // Try to get error message from response
                try {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `HTTP ${response.status}: Failed to download report`);
                } catch (e) {
                    throw new Error(`HTTP ${response.status}: Failed to download report`);
                }
            }

            const blob = await response.blob();
            console.log('Blob received, size:', blob.size);
            
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
            console.error('Error downloading report:', error);
            toast.current?.show({ 
                severity: 'error', 
                summary: 'Error', 
                detail: error.message || 'Failed to download report',
                life: 6000
            });
        }
    };

    // --- Templates ---

    const dateTemplate = (rowData) => {
        // Handle various date formats
        let dateObj;
        
        if (!rowData.submitted_at) {
            return <span className="text-gray-500">Invalid Date</span>;
        }
        
        try {
            // Try parsing as ISO string first
            dateObj = new Date(rowData.submitted_at);
            
            // Check if date is valid
            if (isNaN(dateObj.getTime())) {
                // Try to parse if it's a timestamp number
                if (typeof rowData.submitted_at === 'number') {
                    dateObj = new Date(rowData.submitted_at);
                } else {
                    return <span className="text-gray-500">Invalid Date</span>;
                }
            }
            
            // Double check it's still valid
            if (isNaN(dateObj.getTime())) {
                return <span className="text-gray-500">Invalid Date</span>;
            }
        } catch (error) {
            console.error('Date parsing error:', error, rowData.submitted_at);
            return <span className="text-gray-500">Invalid Date</span>;
        }
        
        return (
            <div className="flex flex-col">
                <span className="font-medium text-gray-700">
                    {dateObj.toLocaleDateString()}
                </span>
                <span className="text-xs text-gray-500">
                    {dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
            </div>
        );
    };

    const statusTemplate = (rowData) => {
        const statusConfig = {
            'COMPLETED': { severity: 'success', icon: 'pi pi-check-circle', label: 'Completed', color: '#443575' },
            'PENDING': { severity: 'warning', icon: 'pi pi-spin pi-spinner', label: 'Processing', color: '#443575' },
            'FAILED': { severity: 'danger', icon: 'pi pi-times-circle', label: 'Failed', color: '#443575' }
        };
        
        const config = statusConfig[rowData.status] || statusConfig['PENDING'];
        return (
            <Tag 
                className="px-3 py-1 text-xs"
                icon={config.icon}
                value={config.label}
                rounded
                style={{ backgroundColor: config.color, color: 'white' }}
            />
        );
    };

    const actionTemplate = (rowData) => {
        return (
            <div className="flex gap-3 justify-center items-center w-full">
                <Button
                    icon="pi pi-eye"
                    className="p-button-rounded p-button-text p-button-secondary p-button-sm hover:bg-[#443575]/10 hover:text-[#443575]"
                    onClick={() => viewResult(rowData)}
                    disabled={rowData.status !== 'COMPLETED'}
                    tooltip="View Details"
                    tooltipPosition="top"
                />
                <Button
                    icon="pi pi-download"
                    className="p-button-rounded p-button-text p-button-success p-button-sm hover:text-green-600"
                    onClick={() => downloadReport(rowData.id)}
                    disabled={rowData.status !== 'COMPLETED'}
                    tooltip="Download Report"
                    tooltipPosition="top"
                />
            </div>
        );
    };

    // Filter submissions based on search and filter criteria
    const filteredSubmissions = submissions.filter(submission => {
        // Global search filter
        const searchMatch = !globalFilter || 
            submission.tier?.toLowerCase().includes(globalFilter.toLowerCase()) ||
            submission.status?.toLowerCase().includes(globalFilter.toLowerCase()) ||
            submission.submitted_at?.toLowerCase().includes(globalFilter.toLowerCase());

        // Tier filter
        const tierMatch = !selectedTier || submission.tier === selectedTier;

        // Status filter
        const statusMatch = !selectedStatus || submission.status?.toUpperCase() === selectedStatus.toUpperCase();

        return searchMatch && tierMatch && statusMatch;
    });



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
        <div className="min-h-screen bg-gray-100 font-sans">
            <Toast ref={toast} />
            
            <div className="p-2">
                {/* Single Card containing everything */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-4">
                    {/* Page Header Section */}
                    <div className="bg-white rounded-xl p-3 mb-3 border border-gray-200 shadow-md">
                        <div className="flex items-center justify-between">
                            <div>
                                <h1 className="text-xl font-bold text-gray-900">Scoping History</h1>
                                <p className="text-gray-500 text-xs mt-0.5">Review and manage your past FCCS scoping entries</p>
                            </div>
                            <Button
                                label="New Scoping"
                                icon="pi pi-plus"
                                className="p-button-sm text-white"
                                style={{ backgroundColor: '#443575', borderColor: '#443575', color: 'white', fontSize: '11px', padding: '6px 12px' }}
                                onClick={() => router.push('/fccs-scoping')}
                            />
                        </div>
                    </div>

                    {/* Search and Filters Section */}
                    <div className="bg-white rounded-xl p-4 mb-4 border border-gray-200 shadow-md">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <label className="text-sm font-medium text-gray-700 mb-2 block">Search</label>
                                <span className="p-input-icon-left w-full">
                                    <i className="pi pi-search" />
                                    <input
                                        type="text"
                                        placeholder="Search by project, client, or submitter..."
                                        className="p-inputtext p-component w-full shadow-sm"
                                        style={{ paddingLeft: '2.5rem' }}
                                        value={globalFilter}
                                        onChange={(e) => setGlobalFilter(e.target.value)}
                                    />
                                </span>
                            </div>
                            <div>
                                <label className="text-sm font-medium text-gray-700 mb-2 block">Tier</label>
                                <select 
                                    className="p-inputtext p-component w-full shadow-sm"
                                    value={selectedTier}
                                    onChange={(e) => setSelectedTier(e.target.value)}
                                >
                                    <option value="">All Tiers</option>
                                    <option value="Tier 1 - Jumpstart">Tier 1 - Jumpstart</option>
                                    <option value="Tier 2 - Foundation Plus">Tier 2 - Foundation Plus</option>
                                    <option value="Tier 3 - Enhanced Scope">Tier 3 - Enhanced Scope</option>
                                    <option value="Tier 4 - Advanced Enablement">Tier 4 - Advanced Enablement</option>
                                    <option value="Tier 5 - Full Spectrum">Tier 5 - Full Spectrum</option>
                                </select>
                            </div>
                            <div>
                                <label className="text-sm font-medium text-gray-700 mb-2 block">Status</label>
                                <select 
                                    className="p-inputtext p-component w-full shadow-sm"
                                    value={selectedStatus}
                                    onChange={(e) => setSelectedStatus(e.target.value)}
                                >
                                    <option value="">All Status</option>
                                    <option value="COMPLETED">Completed</option>
                                    <option value="PENDING">Pending</option>
                                    <option value="FAILED">Failed</option>
                                </select>
                            </div>
                        </div>
                        <p className="text-xs text-gray-500 mt-3">Showing {filteredSubmissions.length} of {submissions.length} results</p>
                    </div>

                    {/* Main Data Table Section */}
                    <div className="bg-white rounded-xl border border-gray-200 shadow-md overflow-hidden">
                        <DataTable 
                            value={filteredSubmissions} 
                            paginator 
                            rows={10}
                            rowsPerPageOptions={[5, 10, 25, 50]}
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
                            header="Submission Date" 
                            body={dateTemplate}
                            sortable
                            style={{ minWidth: '180px' }}
                        />
                        <Column 
                            field="client_name" 
                            header="Client Name" 
                            body={(rowData) => (
                                <span className="font-medium text-gray-800">{rowData.client_name || 'N/A'}</span>
                            )}
                            sortable
                            style={{ minWidth: '150px' }}
                        />
                        <Column 
                            field="project_name" 
                            header="Project Name" 
                            body={(rowData) => (
                                <span className="text-gray-700">{rowData.project_name || 'N/A'}</span>
                            )}
                            sortable
                            style={{ minWidth: '150px' }}
                        />
                        <Column 
                            field="total_weightage" 
                            header="Engagement Weightage" 
                            body={(rowData) => {
                                // Try top-level first, then nested (for backward compatibility)
                                const weightage = rowData.total_weightage ?? rowData.calculation_result?.total_weightage;
                                return <span className="font-semibold text-[#443575]">{weightage ? Number(weightage).toFixed(0) : 'N/A'}</span>;
                            }}
                            align="center"
                            sortable
                            style={{ minWidth: '180px' }}
                        />
                        <Column 
                            field="tier" 
                            header="Tier" 
                            body={(rowData) => {
                                // Try top-level first, then nested (for backward compatibility)
                                const tier = rowData.tier ?? rowData.calculation_result?.tier;
                                return (
                                    <Tag 
                                        value={tier || 'N/A'} 
                                        className="px-3 py-1"
                                        style={{ backgroundColor: '#443575', color: 'white' }}
                                    />
                                );
                            }}
                            sortable
                            style={{ minWidth: '150px' }}
                        />
                        <Column 
                            field="total_months" 
                            header="Estimated Effort" 
                            body={(rowData) => {
                                // Use the exact same data path as the detail page
                                const months = rowData.calculation_result?.effort_estimation?.summary?.total_months 
                                    ?? rowData.calculation_result?.total_months
                                    ?? rowData.total_months;
                                
                                return <span className="font-medium text-gray-900">{months ? `${Number(months).toFixed(1)} months` : 'N/A'}</span>;
                            }}
                            align="left"
                            sortable
                            style={{ minWidth: '150px' }}
                        />
                        <Column 
                            field="status" 
                            header="Status" 
                            body={statusTemplate}
                            align="left"
                            sortable
                            style={{ minWidth: '130px' }}
                        />
                        <Column 
                            header="Actions" 
                            body={actionTemplate}
                            align="center"
                            style={{ minWidth: '120px' }}
                        />
                    </DataTable>
                    </div>
                </div>
            </div>

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
            `}</style>
        </div>
    );
}