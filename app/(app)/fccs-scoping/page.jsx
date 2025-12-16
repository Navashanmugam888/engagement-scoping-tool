'use client';
import React, { useState, useRef, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { Card } from 'primereact/card';
import { InputNumber } from 'primereact/inputnumber';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { Dialog } from 'primereact/dialog';
import { Tag } from 'primereact/tag';
import { InputTextarea } from 'primereact/inputtextarea';
import { Checkbox } from 'primereact/checkbox';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { RadioButton } from 'primereact/radiobutton';

import { scopingSections } from './scopingData';

const ROLES_LIST = [
    "PM USA", "PM India", "Architect USA", "Delivery Lead India",
    "Sr. Delivery Lead India", "App Lead USA", "App Lead India",
    "App Developer USA", "App Developer India", "Integration Lead USA",
    "Integration Developer India", "Reporting Lead India", "Security Lead India"
];

const getSectionIcon = (title) => {
    if (title.includes("Dimension")) return "pi-sitemap";
    if (title.includes("Feature")) return "pi-star";
    if (title.includes("Customization")) return "pi-palette";
    if (title.includes("Calculation")) return "pi-function";
    if (title.includes("Security")) return "pi-lock";
    if (title.includes("Historical")) return "pi-history";
    if (title.includes("Integration")) return "pi-arrows-h";
    if (title.includes("Reporting")) return "pi-chart-bar";
    if (title.includes("Automation")) return "pi-cog";
    if (title.includes("Testing")) return "pi-check-circle";
    if (title.includes("Transition")) return "pi-step-forward";
    if (title.includes("Documentation")) return "pi-file";
    return "pi-list";
};

export default function EngagementScoping() {
    const { data: session } = useSession();
    const router = useRouter();
    const toast = useRef(null);
    const inputRefs = useRef({});

    // --- STATE ---
    const [activeSection, setActiveSection] = useState(0);
    const [formData, setFormData] = useState({});
    const [selectedRoles, setSelectedRoles] = useState([]);
    const [comments, setComments] = useState("");
    const [clientName, setClientName] = useState("");
    const [projectName, setProjectName] = useState("");

    // Dialogs
    const [showReviewDialog, setShowReviewDialog] = useState(false);
    const [showRolesDialog, setShowRolesDialog] = useState(false);
    const [showResult, setShowResult] = useState(false);
    const [showHistory, setShowHistory] = useState(false);

    // Data & Processing
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [calculationResult, setCalculationResult] = useState(null);
    const [historyData, setHistoryData] = useState([]);

    // Prevent page refresh on tab switch - save form data to sessionStorage
    useEffect(() => {
        // Load saved form data on mount
        const savedData = sessionStorage.getItem('fccs-scoping-form-data');
        if (savedData) {
            try {
                const parsed = JSON.parse(savedData);
                setFormData(parsed.formData || {});
                setSelectedRoles(parsed.selectedRoles || []);
                setComments(parsed.comments || '');
                setClientName(parsed.clientName || '');
                setProjectName(parsed.projectName || '');
                setActiveSection(parsed.activeSection || 0);
            } catch (e) {
                console.error('Error loading saved form data:', e);
            }
        }
    }, []);

    useEffect(() => {
        // Save form data whenever it changes
        sessionStorage.setItem('fccs-scoping-form-data', JSON.stringify({
            formData,
            selectedRoles,
            comments,
            clientName,
            projectName,
            activeSection
        }));
    }, [formData, selectedRoles, comments, clientName, projectName, activeSection]);

    // --- HANDLERS ---
    const handleOptionChange = (id, value) => {
        setFormData(prev => ({
            ...prev,
            [id]: { ...prev[id], value: value, count: value === 'YES' ? (prev[id]?.count || null) : null }
        }));
        
        // Auto-focus the input field when YES is selected and item has count
        if (value === 'YES') {
            // First blur any currently focused element to allow clicking other buttons
            if (document.activeElement) {
                document.activeElement.blur();
            }
            
            setTimeout(() => {
                if (inputRefs.current[id]) {
                    inputRefs.current[id].focus();
                }
            }, 100);
        }
    };

    const handleCountChange = (id, count) => {
        setFormData(prev => ({
            ...prev,
            [id]: { ...prev[id], count: count }
        }));
    };

    const handleNext = () => {
        // Validate client and project name
        if (!clientName.trim() || !projectName.trim()) {
            toast.current.show({ 
                severity: 'warn', 
                summary: 'Required Fields', 
                detail: 'Please enter both Client Name and Project Name before proceeding.',
                life: 3000
            });
            return;
        }
        setShowReviewDialog(true);
    };

    const handleFinalSubmit = async () => {
        setIsSubmitting(true);
        const submissionDate = new Date().toISOString();

        const payload = {
            userEmail: session.user.email,
            userName: session.user.name,
            clientName: clientName,
            projectName: projectName,
            scopingData: formData,
            selectedRoles: selectedRoles,
            comments: comments,
            submittedAt: submissionDate
        };

        try {
            // Call external backend API (configured in .env)
            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:5000';
            const response = await fetch(`${backendUrl}/api/scoping/submit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || "Submission failed");
            }

            const data = await response.json();
            
            // Store calculation result for popup display
            // Use effort_estimation.summary for total_hours and total_days (correct values)
            // Use fte_result for role-based hours distribution
            setCalculationResult({
                submissionId: data.submission_id || data.submissionId || data.id,
                totalHours: data.result?.effort_summary?.total_time_hours || data.result?.total_hours || 0,
                totalDays: data.result?.effort_summary?.total_days || data.result?.total_days || 0,
                totalMonths: data.result?.total_months || 0,
                tier: data.result?.tier || "Standard",
                weightage: data.result?.weightage || 0,
                categories: data.result?.categories || [],
                timestamp: submissionDate
            });

            // Close roles dialog and show result popup
            setShowRolesDialog(false);
            setShowResult(true);

            // Show success toast
            toast.current.show({ 
                severity: 'success', 
                summary: 'Calculation Complete', 
                detail: 'Your scoping has been calculated and saved to history.',
                life: 3000
            });

            // Clear form and session storage
            setFormData({});
            setSelectedRoles([]);
            setComments('');
            setClientName('');
            setProjectName('');
            setActiveSection(0);
            sessionStorage.removeItem('fccs-scoping-form-data');

        } catch (error) {
            console.error('Submit error:', error);
            toast.current.show({ 
                severity: 'error', 
                summary: 'Error', 
                detail: error.message || 'Failed to submit scope. Please try again.' 
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    // --- ROW RENDERER ---
    const renderRow = (item, level = 0) => {
        const itemState = formData[item.id] || { value: null, count: null };
        const isYes = itemState.value === 'YES';

        return (
            <div key={item.id} className={`mb-2 ${level > 0 ? 'ml-6 pl-4 border-l-2 border-indigo-50' : ''}`}>
                <div
                    className={`flex items-center justify-between p-3 rounded-lg border transition-all duration-200 h-14
                    ${isYes
                        ? 'bg-indigo-50 border-indigo-200 shadow-sm'
                        : 'bg-white border-gray-200 hover:bg-gray-50'}`}
                >
                    {/* Left side: label + count */}
                    <div className="flex items-center gap-4 flex-1 overflow-hidden">
                        <div className="flex items-center gap-2 min-w-fit">
                            <span
                                className={`text-sm font-semibold truncate ${
                                    isYes ? 'text-[#443575]' : 'text-gray-800'
                                }`}
                            >
                                {item.label}
                            </span>
                            {item.subItems && (
                                <Tag
                                    value="Parent"
                                    className="text-[9px] px-2 py-0 bg-blue-50 text-blue-700 border border-blue-200"
                                />
                            )}
                        </div>

                        {item.hasCount && (
                            <div
                                className={`transition-all duration-300 ease-out origin-left ${
                                    isYes ? 'w-20 opacity-100 scale-100' : 'w-0 opacity-0 scale-95 overflow-hidden'
                                }`}
                            >
                                <InputNumber
                                    ref={(el) => { if (el) inputRefs.current[item.id] = el.getInput(); }}
                                    value={itemState.count}
                                    onValueChange={(e) => handleCountChange(item.id, e.value)}
                                    placeholder="#"
                                    min={0}
                                    className="w-16 h-7 p-inputtext-sm"
                                    inputClassName="text-center font-bold text-[#443575] border-indigo-200 h-7 py-0 text-xs bg-white rounded-md"
                                />
                            </div>
                        )}
                    </div>

                    {/* Right side: custom HTML radio buttons */}
                    <div className="flex-shrink-0 flex items-center gap-6 text-sm font-semibold">
                        <div className="flex items-center gap-2">
                            <input
                                type="radio"
                                id={`${item.id}_yes`}
                                name={item.id}
                                value="YES"
                                onChange={(e) => handleOptionChange(item.id, e.target.value)}
                                checked={itemState.value === 'YES'}
                                className="custom-radio-input"
                            />
                            <label
                                htmlFor={`${item.id}_yes`}
                                className="cursor-pointer select-none text-gray-700"
                            >
                                Yes
                            </label>
                        </div>
                        <div className="flex items-center gap-2">
                            <input
                                type="radio"
                                id={`${item.id}_no`}
                                name={item.id}
                                value="NO"
                                onChange={(e) => handleOptionChange(item.id, e.target.value)}
                                checked={itemState.value === 'NO'}
                                className="custom-radio-input"
                            />
                            <label
                                htmlFor={`${item.id}_no`}
                                className="cursor-pointer select-none text-gray-700"
                            >
                                No
                            </label>
                        </div>
                    </div>
                </div>

                {item.subItems && isYes && (
                    <div className="mt-2 animate-fade-in">
                        {item.subItems.map(sub => renderRow(sub, level + 1))}
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="bg-slate-50 min-h-screen flex flex-col">
            <Toast ref={toast} />

            {/* --- HEADER --- */}
            <div className="bg-white border-b border-gray-200 px-8 py-4 sticky top-0 z-20 shadow-sm flex justify-between items-center h-18">
                <div className="flex items-center gap-3">
                    {/* Updated Icon Background to match brand */}
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#443575] to-[#2d234e] flex items-center justify-center text-white shadow-md">
                        <i className="pi pi-calculator text-lg"></i>
                    </div>
                    <div>
                        <h1 className="text-lg font-bold text-gray-800">FCCS Scoping Engine</h1>
                        <p className="text-xs text-gray-500">Project Estimation Tool</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    <div className="text-right hidden md:block mr-4">
                        <p className="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Active Items</p>
                        {/* Updated Text Color */}
                        <p className="text-lg font-black text-[#443575] leading-none">
                            {Object.values(formData).filter(x => x.value === 'YES').length}
                        </p>
                    </div>

                    {/* UPDATED NEXT BUTTON COLOR */}
                    <Button
                        label="Next: Resourcing"
                        icon="pi pi-arrow-right"
                        iconPos="right"
                        className="bg-[#443575] border-none hover:bg-[#362a5c] text-white shadow-md px-6 font-bold text-sm h-10"
                        onClick={handleNext}
                    />
                </div>
            </div>

            {/* --- MAIN CONTENT --- */}
            <div className="flex flex-1 overflow-hidden w-full max-w-[95%] mx-auto my-4 gap-2 px-2">
                {/* LEFT SIDEBAR */}
                <div className="w-64 flex-shrink-0 bg-white rounded-xl border border-gray-200 overflow-hidden h-[calc(100vh-100px)] flex flex-col shadow-sm">
                    <div className="p-4 bg-gray-50 border-b border-gray-100">
                        <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Categories</h3>
                    </div>
                    <div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
                        {scopingSections.map((section, i) => (
                            <button
                                key={i}
                                onClick={() => setActiveSection(i)}
                                className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 
                                ${activeSection === i
                                    // Updated Active State Color
                                    ? 'bg-[#443575] text-white shadow-sm'
                                    : 'text-gray-600 hover:bg-gray-50'}`}
                            >
                                <i
                                    className={`pi ${getSectionIcon(section.title)} ${
                                        activeSection === i ? 'text-indigo-100' : 'text-gray-400'
                                    }`}
                                ></i>
                                <span className="flex-1 text-left truncate">{section.title}</span>
                                <span
                                    className={`text-[10px] font-bold px-2 py-0.5 rounded-md border
                                    ${activeSection === i
                                        // Updated Badge Color (Lighter Purple)
                                        ? 'bg-[#5e4b9c] border-[#443575] text-white'
                                        : 'bg-white border-gray-200 text-gray-400'
                                    }`}
                                >
                                    {section.items.length}
                                </span>
                            </button>
                        ))}
                    </div>
                </div>

                {/* CENTER: FORM AREA */}
                <div className="flex-1 bg-white rounded-xl border border-gray-200 shadow-sm h-[calc(100vh-100px)] flex flex-col overflow-hidden">
                    <div className="p-5 border-b border-gray-100 bg-white flex justify-between items-center sticky top-0 z-10">
                        <div>
                            <h2 className="text-xl font-bold text-gray-800">
                                {scopingSections[activeSection].title}
                            </h2>
                            <p className="text-xs text-gray-500 mt-1">
                                Configure requirements for this section.
                            </p>
                        </div>
                        <div className="flex gap-2">
                            <Button
                                icon="pi pi-arrow-left"
                                className="p-button-rounded p-button-text p-button-secondary w-9 h-9"
                                disabled={activeSection === 0}
                                onClick={() => setActiveSection(prev => prev - 1)}
                            />
                            <Button
                                icon="pi pi-arrow-right"
                                className="p-button-rounded p-button-text p-button-secondary w-9 h-9"
                                disabled={activeSection === scopingSections.length - 1}
                                onClick={() => setActiveSection(prev => prev + 1)}
                            />
                        </div>
                    </div>

                    <div className="flex-1 overflow-y-auto p-6 custom-scrollbar bg-slate-50">
                        <div className="max-w-full">
                            {/* Client and Project Name Fields */}
                            {activeSection === 0 && (
                                <div className="mb-6 p-4 bg-white rounded-lg border border-gray-200 shadow-sm">
                                    <h3 className="text-sm font-bold text-gray-700 mb-4 flex items-center gap-2">
                                        <i className="pi pi-briefcase text-[#443575]"></i>
                                        Project Information
                                    </h3>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="text-xs font-bold text-gray-600 mb-2 block">
                                                Client Name <span className="text-red-500">*</span>
                                            </label>
                                            <InputText
                                                value={clientName}
                                                onChange={(e) => setClientName(e.target.value)}
                                                placeholder="Enter client name"
                                                className="w-full text-sm p-3 border-gray-300 rounded-lg focus:border-[#443575] focus:ring-1 focus:ring-[#443575]"
                                            />
                                        </div>
                                        <div>
                                            <label className="text-xs font-bold text-gray-600 mb-2 block">
                                                Project Name <span className="text-red-500">*</span>
                                            </label>
                                            <InputText
                                                value={projectName}
                                                onChange={(e) => setProjectName(e.target.value)}
                                                placeholder="Enter project name"
                                                className="w-full text-sm p-3 border-gray-300 rounded-lg focus:border-[#443575] focus:ring-1 focus:ring-[#443575]"
                                            />
                                        </div>
                                    </div>
                                </div>
                            )}
                            
                            {scopingSections[activeSection].items.map((item) => renderRow(item))}
                        </div>
                    </div>
                </div>
            </div>

            {/* --- REVIEW DIALOG --- */}
            <Dialog
                header="Review Your Selections"
                visible={showReviewDialog}
                style={{ width: '900px', maxHeight: '80vh' }}
                onHide={() => setShowReviewDialog(false)}
                modal
                dismissableMask
                className="custom-dialog-header"
            >
                <div className="p-4">
                    {/* Project Info Summary */}
                    <div className="bg-purple-50 p-4 rounded-lg mb-4 border border-purple-100">
                        <h4 className="text-sm font-bold text-[#443575] mb-3">Project Information</h4>
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <span className="text-xs text-gray-600">Client Name:</span>
                                <p className="text-sm font-semibold text-gray-900">{clientName}</p>
                            </div>
                            <div>
                                <span className="text-xs text-gray-600">Project Name:</span>
                                <p className="text-sm font-semibold text-gray-900">{projectName}</p>
                            </div>
                        </div>
                    </div>

                    {/* Selected Items Summary */}
                    <div className="bg-gray-50 p-4 rounded-lg mb-4 border border-gray-200">
                        <h4 className="text-sm font-bold text-gray-800 mb-3 flex items-center gap-2">
                            <i className="pi pi-check-circle text-green-600"></i>
                            Selected Items ({Object.values(formData).filter(x => x.value === 'YES').length})
                        </h4>
                        
                        {Object.values(formData).filter(x => x.value === 'YES').length === 0 ? (
                            <p className="text-xs text-gray-500 italic">No items selected</p>
                        ) : (
                            <div className="space-y-3 max-h-96 overflow-y-auto">
                                {scopingSections.map((section, sectionIdx) => {
                                    const sectionItems = section.items.filter(item => {
                                        const itemData = formData[item.id];
                                        if (itemData?.value === 'YES') return true;
                                        // Check sub-items
                                        if (item.subItems) {
                                            return item.subItems.some(sub => formData[sub.id]?.value === 'YES');
                                        }
                                        return false;
                                    });

                                    if (sectionItems.length === 0) return null;

                                    return (
                                        <div key={sectionIdx} className="mb-3">
                                            <h5 className="text-xs font-bold text-[#443575] mb-2 flex items-center gap-2">
                                                <i className={`pi ${getSectionIcon(section.title)} text-xs`}></i>
                                                {section.title}
                                            </h5>
                                            <div className="space-y-2 pl-4">
                                                {sectionItems.map(item => {
                                                    const renderItem = (itm, level = 0) => {
                                                        const itemData = formData[itm.id];
                                                        if (itemData?.value !== 'YES') return null;

                                                        return (
                                                            <div key={itm.id} className={`flex items-start gap-2 ${level > 0 ? 'ml-4' : ''}`}>
                                                                <i className="pi pi-check text-green-600 text-xs mt-0.5"></i>
                                                                <div className="flex-1">
                                                                    <span className="text-xs text-gray-700">{itm.label}</span>
                                                                    {itemData.count && (
                                                                        <span className="ml-2 text-xs font-bold text-[#443575]">
                                                                            (Count: {itemData.count})
                                                                        </span>
                                                                    )}
                                                                    {itm.subItems && (
                                                                        <div className="mt-1 space-y-1">
                                                                            {itm.subItems.map(sub => renderItem(sub, level + 1))}
                                                                        </div>
                                                                    )}
                                                                </div>
                                                            </div>
                                                        );
                                                    };
                                                    return renderItem(item);
                                                })}
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex justify-between items-center gap-3 pt-4 border-t border-gray-200">
                        <Button
                            label="Back to Edit"
                            icon="pi pi-arrow-left"
                            className="p-button-text p-button-secondary"
                            onClick={() => setShowReviewDialog(false)}
                        />
                        <Button
                            label="Continue to Resourcing"
                            icon="pi pi-arrow-right"
                            iconPos="right"
                            className="bg-[#443575] border-none hover:bg-[#362a5c] text-white"
                            onClick={() => {
                                setShowReviewDialog(false);
                                setShowRolesDialog(true);
                            }}
                        />
                    </div>
                </div>
            </Dialog>

            {/* --- ROLES DIALOG --- */}
            <Dialog
                header="Resourcing & Roles"
                visible={showRolesDialog}
                style={{ width: '650px' }}
                onHide={() => setShowRolesDialog(false)}
                modal
                dismissableMask
                className="custom-dialog-header"
            >
                <div className="p-4">
                    <div className="bg-indigo-50 p-4 rounded-lg mb-6 border border-indigo-100">
                        <h4 className="text-sm font-bold text-[#443575] mb-1">Select Engagement Roles</h4>
                        <p className="text-xs text-indigo-700">
                            Define the team composition for the scope estimation.
                        </p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-8">
                        {ROLES_LIST.map(role => (
                            <div
                                key={role}
                                className={`flex items-center p-3 rounded-lg border cursor-pointer transition-colors ${
                                    selectedRoles.includes(role)
                                        ? 'bg-indigo-50 border-[#443575] shadow-sm'
                                        : 'bg-white border-gray-200 hover:border-gray-300'
                                }`}
                                onClick={() => {
                                    let _roles = [...selectedRoles];
                                    if (_roles.includes(role)) _roles = _roles.filter(r => r !== role);
                                    else _roles.push(role);
                                    setSelectedRoles(_roles);
                                }}
                            >
                                <Checkbox
                                    inputId={role}
                                    checked={selectedRoles.includes(role)}
                                    readOnly
                                    className="mr-3"
                                    pt={{
                                        box: { className: selectedRoles.includes(role) ? 'bg-[#443575] border-[#443575]' : '' }
                                    }}
                                />
                                <label className="text-sm text-gray-700 cursor-pointer select-none flex-1">
                                    {role}
                                </label>
                            </div>
                        ))}
                    </div>
                    {/* UPDATED CALCULATE BUTTON COLOR */}
                    <Button
                        label="Calculate & Submit"
                        icon="pi pi-check-circle"
                        className="w-full bg-[#443575] border-none hover:bg-[#362a5c] p-button-lg shadow-md font-bold text-white"
                        onClick={handleFinalSubmit}
                        loading={isSubmitting}
                    />
                </div>
            </Dialog>

            {/* --- HISTORY DIALOG --- */}
            <Dialog
                header="Submission History"
                visible={showHistory}
                style={{ width: '900px' }}
                onHide={() => setShowHistory(false)}
                modal
                dismissableMask
            >
                <div className="p-2">
                    <DataTable
                        value={historyData}
                        stripedRows
                        paginator
                        rows={5}
                        tableStyle={{ minWidth: '50rem' }}
                        emptyMessage="No history found."
                    >
                        <Column
                            field="date"
                            header="Date"
                            body={(d) => new Date(d.date).toLocaleDateString()}
                            sortable
                        ></Column>
                        <Column field="user" header="User" sortable></Column>
                        <Column
                            field="complexity"
                            header="Complexity"
                            body={(d) => <Tag value={d.complexity} severity="info" />}
                        ></Column>
                        <Column field="weeks" header="Est. Weeks" sortable></Column>
                        <Column field="cost" header="Cost"></Column>
                        <Column
                            header="Action"
                            body={(d) => (
                                <Button
                                    icon="pi pi-eye"
                                    className="p-button-rounded p-button-text p-button-secondary"
                                    tooltip="View Result"
                                    onClick={() => {
                                        setCalculationResult(d.fullResult);
                                        setShowHistory(false);
                                        setShowResult(true);
                                    }}
                                />
                            )}
                        ></Column>
                    </DataTable>
                </div>
            </Dialog>

            {/* --- RESULT DIALOG --- */}
            <Dialog
                header="Calculation Complete"
                visible={showResult}
                style={{ width: '600px' }}
                onHide={() => setShowResult(false)}
                modal
                draggable={false}
                dismissableMask
            >
                {calculationResult && (
                    <div className="text-center p-4">
                        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 border-4 border-green-50">
                            <i className="pi pi-check-circle text-4xl text-green-600"></i>
                        </div>
                        
                        <h2 className="text-2xl font-bold text-gray-800 mb-2">
                            Scoping Calculation Successful!
                        </h2>
                        <p className="text-gray-600 mb-6">
                            Your FCCS implementation scoping has been calculated and saved to history.
                        </p>

                        {/* Summary Cards */}
                        <div className="grid grid-cols-2 gap-4 mb-6">
                            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-xl border border-blue-200">
                                <div className="text-3xl font-black text-blue-700 mb-1">
                                    {calculationResult.totalHours?.toLocaleString() || "0"}
                                </div>
                                <div className="text-xs text-blue-600 uppercase font-semibold tracking-wide">
                                    Total Hours
                                </div>
                            </div>
                            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-xl border border-purple-200">
                                <div className="text-3xl font-black text-purple-700 mb-1">
                                    {calculationResult.totalDays?.toFixed(1) || "0"}
                                </div>
                                <div className="text-xs text-purple-600 uppercase font-semibold tracking-wide">
                                    Total Days
                                </div>
                            </div>
                        </div>

                        {/* Details Box */}
                        <div className="bg-gray-50 p-5 rounded-xl text-left border border-gray-200 shadow-inner mb-6">
                            <div className="flex justify-between mb-3 pb-3 border-b border-gray-200">
                                <span className="text-gray-600 font-medium">Implementation Tier</span>
                                <span className="font-bold text-gray-900">
                                    {calculationResult.tier || "Standard"}
                                </span>
                            </div>
                            <div className="flex justify-between mb-3 pb-3 border-b border-gray-200">
                                <span className="text-gray-600 font-medium">Total Weightage</span>
                                <span className="font-bold text-gray-900">
                                    {calculationResult.weightage || 0}
                                </span>
                            </div>
                            <div className="flex justify-between mb-3 pb-3 border-b border-gray-200">
                                <span className="text-gray-600 font-medium">Duration</span>
                                <span className="font-bold text-indigo-600">
                                    {calculationResult.totalMonths?.toFixed(2) || "0"} months
                                </span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600 font-medium">Submission ID</span>
                                <span className="font-mono text-sm font-bold text-gray-900">
                                    #{calculationResult.submissionId || "N/A"}
                                </span>
                            </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="grid grid-cols-2 gap-3">
                            <Button
                                label="Close"
                                icon="pi pi-times"
                                className="p-button-text p-button-secondary text-gray-600 hover:bg-gray-100"
                                onClick={() => setShowResult(false)}
                            />
                            <Button
                                label="View Details"
                                icon="pi pi-eye"
                                className="bg-[#443575] border-none hover:bg-[#362a5c] shadow-md text-white"
                                onClick={() => {
                                    setShowResult(false);
                                    router.push(`/scoping-history/${calculationResult?.submissionId}`);
                                }}
                            />
                        </div>
                    </div>
                )}
            </Dialog>
        </div>
    );
}