'use client';
import React, { useState, useEffect, useRef } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Tag } from 'primereact/tag';
import { Toast } from 'primereact/toast';
import { ProgressSpinner } from 'primereact/progressspinner';
import { ProgressBar } from 'primereact/progressbar';
import { Avatar } from 'primereact/avatar';

// Helper component for Stat Cards
const StatCard = ({ title, value, subtext, icon, color = "text-[#443575]" }) => (
    <div className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm flex items-start justify-between hover:shadow-md transition-shadow duration-200">
        <div>
            <p className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-0.5">{title}</p>
            <h3 className="text-lg font-bold text-gray-800">{value}</h3>
            {subtext && <p className="text-[10px] text-gray-500 mt-0.5">{subtext}</p>}
        </div>
        <div className={`p-2 rounded-full bg-gray-50 ${color}`}>
            <i className={`${icon} text-sm`}></i>
        </div>
    </div>
);

export default function ScopingDetail() {
    const router = useRouter();
    const params = useParams();
    const toast = useRef(null);
    const [submission, setSubmission] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (params.id) {
            fetchDetail();
        }
    }, [params.id]);

    const fetchDetail = async () => {
        try {
            setLoading(true);
            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:5000';
            const response = await fetch(`${backendUrl}/api/scoping/result/${params.id}`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch result');
            }
            
            const data = await response.json();
            
            if (data.success || data.submission) {
                setSubmission(data.submission || data);
            }
        } catch (error) {
            console.error('Error fetching result:', error);
            toast.current?.show({ 
                severity: 'error', 
                summary: 'Error', 
                detail: error.message || 'Failed to load result' 
            });
        } finally {
            setLoading(false);
        }
    };

    const downloadReport = async (submissionId) => {
        try {
            toast.current?.show({ 
                severity: 'info', 
                summary: 'Downloading', 
                detail: 'Preparing your report...' 
            });

            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:5000';
            const downloadUrl = `${backendUrl}/api/scoping/download/${submissionId}`;
            
            const response = await fetch(downloadUrl);
            
            if (!response.ok) {
                throw new Error('Failed to download report');
            }

            const blob = await response.blob();
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

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-100">
                <div className="text-center">
                    <ProgressSpinner style={{width: '50px', height: '50px'}} strokeWidth="4" animationDuration=".5s" />
                    <p className="text-gray-500 mt-4 text-sm">Loading details...</p>
                </div>
            </div>
        );
    }

    if (!submission) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-100">
                <div className="text-center">
                    <p className="text-gray-500">Submission not found</p>
                    <Button 
                        label="Back to History" 
                        icon="pi pi-arrow-left"
                        className="mt-4"
                        style={{ backgroundColor: '#443575', borderColor: '#443575' }}
                        onClick={() => router.push('/scoping-history')}
                    />
                </div>
            </div>
        );
    }

    const result = submission.calculation_result;
    const scopeDef = result?.scope_definition;
    const effortEst = result?.effort_estimation;
    const fteAlloc = result?.fte_allocation;
    
    // Extract values from scoping_data
    const scopingData = submission.scoping_data || {};
    const entityCount = scopingData.entity?.count || 0;
    const customDimCount = scopingData.cust_dim?.count || 0;
    const accountData = scopingData.account;
    const hasCustomElim = scopingData.cust_elim?.value === 'YES';

    return (
        <div className="min-h-screen bg-gray-100 p-2 font-sans">
            <Toast ref={toast} />
            
            {/* Main Container - Similar to History Page */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-3">
                {/* Header Section */}
                <div className="bg-white rounded-xl p-3 mb-3 border border-gray-200 shadow-md">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <button
                                onClick={() => router.push('/scoping-history')}
                                className="flex items-center gap-2 text-[#443575] hover:text-[#2d1b4e] transition-colors text-sm"
                            >
                                <i className="pi pi-arrow-left text-sm"></i>
                                <span className="font-medium">Back to History</span>
                            </button>
                        </div>
                        <Button
                            label="Download Report"
                            icon="pi pi-download"
                            className="p-button-sm text-xs"
                            style={{ backgroundColor: '#443575', borderColor: '#443575', color: 'white', fontSize: '12px', padding: '6px 12px' }}
                            onClick={() => downloadReport(submission.submission_id)}
                        />
                    </div>
                </div>

                {/* Title Section */}
                <div className="bg-white rounded-xl p-4 mb-3 border border-gray-200 shadow-md">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-xl font-bold text-gray-900 mb-1">Scoping Details</h1>
                            <p className="text-xs text-gray-500">View the complete scoping submission and calculated results</p>
                        </div>
                        <div className="text-right">
                            <span className="text-[10px] text-gray-500 block mb-0.5">Reference ID</span>
                            <span className="text-xs font-semibold text-gray-900">{submission.submission_id}</span>
                        </div>
                    </div>
                </div>

                {/* Project Info Card */}
                <div className="bg-white rounded-xl p-4 mb-3 border border-gray-200 shadow-md">
                    <h2 className="text-base font-bold text-gray-900 mb-3">{submission.project_name || 'Project Details'}</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                        <div className="flex items-start gap-2">
                            <i className="pi pi-briefcase text-gray-400 mt-0.5 text-sm"></i>
                            <div>
                                <p className="text-[10px] text-gray-500 mb-0.5">Project Name</p>
                                <p className="text-xs font-medium text-gray-900">{submission.project_name || 'N/A'}</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-2">
                            <i className="pi pi-building text-gray-400 mt-0.5 text-sm"></i>
                            <div>
                                <p className="text-[10px] text-gray-500 mb-0.5">Client Name</p>
                                <p className="text-xs font-medium text-gray-900">{submission.client_name || 'N/A'}</p>
                            </div>
                        </div>
                        <div className="flex items-start gap-2">
                            <i className="pi pi-calendar text-gray-400 mt-0.5 text-sm"></i>
                            <div>
                                <p className="text-[10px] text-gray-500 mb-0.5">Submission Date</p>
                                <p className="text-xs font-medium text-gray-900">
                                    {new Date(submission.submitted_at || submission.timestamp).toLocaleDateString()}
                                </p>
                            </div>
                        </div>
                        <div className="flex items-start gap-2">
                            <i className="pi pi-user text-gray-400 mt-0.5 text-sm"></i>
                            <div>
                                <p className="text-[10px] text-gray-500 mb-0.5">Submitted By</p>
                                <p className="text-xs font-medium text-gray-900">{submission.user_name}</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Content Section */}
                <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-md">
                    {/* Executive Summary Cards */}
                    <div className="mb-4">
                        <h4 className="text-sm font-semibold text-gray-900 mb-3">Project Summary</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
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
                                title="Engagement Weightage" 
                                value={result?.total_weightage || scopeDef?.total_weightage || 0}
                                subtext="Complexity Score"
                                icon="pi pi-chart-line"
                                color="text-purple-600"
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
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                        {/* FTE Allocation */}
                        <div className="lg:col-span-2 space-y-3">
                            {fteAlloc && fteAlloc.by_role && (
                                <div className="bg-gray-50 border border-gray-200 rounded-lg overflow-hidden">
                                    <div className="px-4 py-3 border-b border-gray-200 flex justify-between items-center bg-white">
                                        <h3 className="text-sm font-semibold text-gray-800 flex items-center gap-2">
                                            <i className="pi pi-chart-bar text-[#443575] text-sm"></i> Resource Allocation
                                        </h3>
                                        <span className="text-[10px] font-medium bg-purple-50 text-[#443575] px-2 py-1 rounded">
                                            {fteAlloc.total_hours?.toFixed(0)} Total Hours
                                        </span>
                                    </div>
                                    <DataTable 
                                        value={Object.entries(fteAlloc.by_role).map(([role, data]) => ({
                                            role,
                                            hours: data.hours,
                                            percentage: ((data.hours / fteAlloc.total_hours) * 100)
                                        }))}
                                        className="p-datatable-sm custom-table text-xs"
                                        stripedRows
                                    >
                                        <Column field="role" header="Role" className="text-xs font-medium text-gray-700" style={{fontSize: '11px'}} />
                                        <Column field="hours" header="Hours" align="right" body={d => <span className="text-xs">{d.hours.toFixed(1)}</span>} style={{fontSize: '11px'}} />
                                        <Column 
                                            field="percentage" 
                                            header="Allocation %" 
                                            body={(d) => (
                                                <div className="flex items-center gap-2">
                                                    <ProgressBar value={d.percentage} showValue={false} style={{ height: '4px', width: '50px' }} color="#443575"></ProgressBar>
                                                    <span className="text-[10px] text-gray-500 w-8">{d.percentage.toFixed(1)}%</span>
                                                </div>
                                            )} 
                                            style={{fontSize: '11px'}}
                                        />
                                    </DataTable>
                                </div>
                            )}

                            {/* Effort Breakdown */}
                            {effortEst && effortEst.categories && (
                                <div className="bg-gray-50 border border-gray-200 rounded-lg overflow-hidden">
                                    <div className="px-4 py-3 border-b border-gray-200 bg-white">
                                        <h3 className="text-sm font-semibold text-gray-800 flex items-center gap-2">
                                            <i className="pi pi-list text-[#443575] text-sm"></i> Effort Breakdown
                                        </h3>
                                    </div>
                                    <DataTable 
                                        value={Object.entries(effortEst.categories)
                                            .map(([cat, hrs]) => ({ category: cat, hours: Number(hrs) }))
                                            .sort((a, b) => b.hours - a.hours)
                                        }
                                        className="p-datatable-sm text-xs"
                                        stripedRows
                                        paginator
                                        rows={5}
                                    >
                                        <Column field="category" header="Category" style={{fontSize: '11px'}} />
                                        <Column 
                                            field="hours" 
                                            header="Hours" 
                                            align="right" 
                                            body={d => <span className="font-mono text-xs">{d.hours.toFixed(1)}</span>} 
                                            style={{fontSize: '11px'}}
                                        />
                                    </DataTable>
                                </div>
                            )}
                        </div>

                        {/* Sidebar */}
                        <div className="space-y-3">
                            {/* Scope Summary */}
                            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                                <h3 className="text-xs font-bold text-gray-900 uppercase tracking-wide mb-3 pb-2 border-b border-gray-300">Scope Metrics</h3>
                                <div className="space-y-3">
                                    <div className="flex justify-between items-center">
                                        <span className="text-gray-600 text-xs">Weightage</span>
                                        <span className="font-bold text-gray-900 text-sm">{scopeDef?.total_weightage}</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <span className="text-gray-600 text-xs">In Scope Items</span>
                                        <Tag severity="success" value={scopeDef?.summary?.in_scope_count} rounded className="text-xs" style={{fontSize: '10px', padding: '2px 8px'}} />
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <span className="text-gray-600 text-xs">Out of Scope</span>
                                        <Tag severity="warning" value={scopeDef?.summary?.out_of_scope_count} rounded className="text-xs" style={{fontSize: '10px', padding: '2px 8px'}} />
                                    </div>
                                </div>

                                {scopeDef?.selected_roles && (
                                    <div className="mt-4">
                                        <p className="text-[10px] text-gray-500 mb-2">Required Roles</p>
                                        <div className="flex flex-wrap gap-1.5">
                                            {scopeDef.selected_roles.map((role, idx) => (
                                                <span key={idx} className="text-[10px] px-2 py-0.5 bg-white text-gray-700 rounded border border-gray-300">
                                                    {role}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* Submission Metadata */}
                            <div className="bg-purple-50 border border-purple-100 rounded-lg p-4">
                                <h3 className="text-xs font-bold text-[#443575] uppercase tracking-wide mb-3">Submission Info</h3>
                                <div className="flex items-center gap-2 mb-3">
                                    <Avatar label={submission.user_name?.charAt(0)} shape="circle" className="bg-[#443575] text-white" size="normal" style={{width: '32px', height: '32px', fontSize: '14px'}} />
                                    <div>
                                        <p className="text-xs font-medium text-gray-900">{submission.user_name}</p>
                                        <p className="text-[10px] text-gray-500">Submitter</p>
                                    </div>
                                </div>
                                {submission.comments && (
                                    <div className="text-[10px] text-gray-600 bg-white p-2 rounded border border-gray-200">
                                        <span className="block font-semibold mb-1">Comments:</span>
                                        {submission.comments}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <style jsx global>{`
                .p-progressbar .p-progressbar-value {
                    background: #443575;
                }
            `}</style>
        </div>
    );
}
