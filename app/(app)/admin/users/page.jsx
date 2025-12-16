'use client';
import React, { useState, useEffect, useRef } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Tag } from 'primereact/tag';
import { Toast } from 'primereact/toast';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Avatar } from 'primereact/avatar';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';

export default function ManageUsers() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [globalFilter, setGlobalFilter] = useState('');
    const [showAddDialog, setShowAddDialog] = useState(false);
    const [showEditDialog, setShowEditDialog] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const [editedUser, setEditedUser] = useState({ role: '', status: '' });
    const [newUser, setNewUser] = useState({ name: '', email: '', role: 'GUEST', status: 'PENDING' });
    const toast = useRef(null);
    const { data: session } = useSession();
    const router = useRouter();

    const roleOptions = [
        { label: 'Administrator', value: 'SUPER_ADMIN' },
        { label: 'Super User', value: 'SUPER_USER' },
        { label: 'History Viewer', value: 'HISTORY_VIEWER' },
        { label: 'Scoping Editor', value: 'SCOPING_EDITOR' },
        { label: 'Guest', value: 'GUEST' }
    ];

    const statusOptions = [
        { label: 'Active', value: 'ACTIVE' },
        { label: 'Inactive', value: 'INACTIVE' },
        { label: 'Pending', value: 'PENDING' }
    ];

    useEffect(() => {
        if (session && session.user.role !== 'SUPER_ADMIN') {
            router.push('/dashboard');
        } else {
            fetchUsers();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [session]);

    const fetchUsers = async () => {
        try {
            setLoading(true);
            const res = await fetch('/api/admin/users');
            if (res.ok) {
                const data = await res.json();
                setUsers(data);
            } else {
                toast.current?.show({ severity: 'error', summary: 'Error', detail: 'Unauthorized' });
            }
        } catch (error) {
            console.error('Error fetching users:', error);
            toast.current?.show({ severity: 'error', summary: 'Error', detail: 'Failed to load users' });
        } finally {
            setLoading(false);
        }
    };

    const updateUser = async (email, updates) => {
        try {
            const res = await fetch('/api/admin/users', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, ...updates })
            });
            
            if (!res.ok) throw new Error('Failed to update');
            
            toast.current?.show({ severity: 'success', summary: 'Success', detail: 'User updated successfully' });
            fetchUsers();
        } catch (error) {
            console.error('Error updating user:', error);
            toast.current?.show({ severity: 'error', summary: 'Error', detail: 'Update failed' });
        }
    };

    const deleteUser = async (email) => {
        if (!confirm('Are you sure you want to delete this user?')) return;
        
        try {
            const res = await fetch('/api/admin/users', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            
            if (!res.ok) throw new Error('Failed to delete');
            
            toast.current?.show({ severity: 'success', summary: 'Success', detail: 'User deleted successfully' });
            fetchUsers();
        } catch (error) {
            console.error('Error deleting user:', error);
            toast.current?.show({ severity: 'error', summary: 'Error', detail: 'Delete failed' });
        }
    };

    const userTemplate = (rowData) => {
        const initials = rowData.user_name?.split(' ').map(n => n[0]).join('').toUpperCase() || 'U';
        return (
            <div className="flex items-center gap-3">
                <Avatar 
                    label={initials} 
                    shape="circle" 
                    className="bg-[#2d1b4e] text-white"
                    style={{ width: '36px', height: '36px', fontSize: '14px' }}
                />
                <div>
                    <div className="font-semibold text-gray-900 text-sm">{rowData.user_name}</div>
                    <div className="text-xs text-gray-500">{rowData.email}</div>
                </div>
            </div>
        );
    };

    const roleTemplate = (rowData) => {
        const roleConfig = {
            'SUPER_ADMIN': { label: 'Administrator', color: '#3b82f6' },
            'SUPER_USER': { label: 'Super User', color: '#8b5cf6' },
            'HISTORY_VIEWER': { label: 'History Viewer', color: '#f59e0b' },
            'SCOPING_EDITOR': { label: 'Scoping Editor', color: '#10b981' },
            'GUEST': { label: 'Guest', color: '#6b7280' }
        };
        
        const config = roleConfig[rowData.role] || roleConfig['GUEST'];
        // use inline backgroundColor (valid color string) and a small class to ensure font/shape
        return (
            <Tag 
                value={config.label} 
                style={{ backgroundColor: config.color, color: 'white', fontSize: '11px', padding: '4px 10px', borderRadius: '6px', border: 'none' }}
            />
        );
    };

    const statusTemplate = (rowData) => {
        const statusConfig = {
            'ACTIVE': { bgColor: '#dcfce7', textColor: '#166534', label: 'Active' },
            'INACTIVE': { bgColor: '#fee2e2', textColor: '#991b1b', label: 'Inactive' },
            'PENDING': { bgColor: '#fef9c3', textColor: '#854d0e', label: 'Pending' }
        };
        
        const config = statusConfig[rowData.status] || { bgColor: '#fef9c3', textColor: '#854d0e', label: rowData.status };
        return (
            <span 
                style={{ 
                    display: 'inline-block',
                    backgroundColor: config.bgColor,
                    color: config.textColor,
                    fontSize: '10px', 
                    padding: '3px 8px',
                    borderRadius: '4px',
                    fontWeight: '500',
                    textAlign: 'center'
                }}
            >
                {config.label}
            </span>
        );
    };

    const lastLoginTemplate = (rowData) => {
        if (!rowData.last_login) return <span className="text-xs text-gray-500">N/A</span>;
        const date = new Date(rowData.last_login);
        return (
            <span className="text-xs text-gray-700">
                {date.toLocaleString('en-US', { 
                    year: 'numeric', 
                    month: '2-digit', 
                    day: '2-digit', 
                    hour: '2-digit', 
                    minute: '2-digit' 
                })}
            </span>
        );
    };

    const actionsTemplate = (rowData) => {
        return (
            <div className="flex gap-2 justify-end">
                <Button
                    icon="pi pi-pencil"
                    className="p-button-text p-button-sm"
                    style={{ color: '#2d1b4e' }}
                    onClick={() => openEditDialog(rowData)}
                    tooltip="Edit User"
                />
                <Button
                    icon="pi pi-trash"
                    className="p-button-text p-button-sm p-button-danger"
                    onClick={() => deleteUser(rowData.email)}
                    tooltip="Delete User"
                />
            </div>
        );
    };

    const openEditDialog = (user) => {
        setSelectedUser(user);
        setEditedUser({ role: user.role, status: user.status });
        setShowEditDialog(true);
    };

    const handleEditUser = async () => {
        try {
            const res = await fetch('/api/admin/users', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email: selectedUser.email, 
                    role: editedUser.role, 
                    status: editedUser.status 
                })
            });
            
            if (!res.ok) throw new Error('Failed to update');
            
            toast.current?.show({ severity: 'success', summary: 'Success', detail: 'User updated successfully' });
            setShowEditDialog(false);
            fetchUsers();
        } catch (error) {
            console.error('Error updating user:', error);
            toast.current?.show({ severity: 'error', summary: 'Error', detail: 'Update failed' });
        }
    };

    const header = (
        <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
                <span className="p-input-icon-left">
                    <i className="pi pi-search" />
                    <InputText
                        value={globalFilter}
                        onChange={(e) => setGlobalFilter(e.target.value)}
                        placeholder="Search by name or email..."
                        className="text-sm"
                        style={{ width: '300px' }}
                    />
                </span>
            </div>
            <Button
                label="Add New User"
                icon="pi pi-plus"
                className="p-button-sm"
                style={{ backgroundColor: '#2d1b4e', borderColor: '#2d1b4e', fontSize: '10px', color: 'white', fontWeight: '400' }}
                onClick={() => setShowAddDialog(true)}
            />
        </div>
    );

    return (
        <div className="min-h-screen bg-gray-100 p-4">
            <Toast ref={toast} />
            
            {/* Header */}
            <div className="bg-white rounded-xl p-4 mb-4 border border-gray-200 shadow-md">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900">Manage Users</h1>
                        <p className="text-xs text-gray-500 mt-0.5">View and manage system user accounts and permissions</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <button
                            onClick={() => router.push('/admin/role-allocations')}
                            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                        >
                            <i className="pi pi-users text-sm"></i>
                            Role Allocations
                        </button>
                        <button
                            onClick={() => router.push('/dashboard')}
                            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                        >
                            <i className="pi pi-th-large text-sm"></i>
                            Admin Dashboard
                        </button>
                    </div>
                </div>
            </div>

            {/* Users Table */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-md overflow-hidden">
                <div className="p-4 border-b border-gray-200">
                    {header}
                </div>
                <DataTable
                    value={users}
                    loading={loading}
                    globalFilter={globalFilter}
                    emptyMessage="No users found"
                    className="text-sm"
                    stripedRows
                    paginator
                    rows={10}
                    rowsPerPageOptions={[10, 25, 50]}
                >
                    <Column field="user_name" header="User" body={userTemplate} style={{ minWidth: '250px' }} />
                    <Column field="role" header="Role" body={roleTemplate} style={{ minWidth: '150px' }} />
                    <Column field="status" header="Status" body={statusTemplate} style={{ minWidth: '120px' }} />
                    <Column field="last_login" header="Last Login" body={lastLoginTemplate} style={{ minWidth: '180px' }} />
                    <Column header="Actions" body={actionsTemplate} style={{ width: '120px' }} />
                </DataTable>
            </div>

            {/* Add User Dialog */}
            <Dialog
                header="Add New User"
                visible={showAddDialog}
                style={{ width: '500px' }}
                onHide={() => setShowAddDialog(false)}
            >
                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                        <InputText
                            value={newUser.name}
                            onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                            placeholder="Enter user name"
                            className="w-full"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                        <InputText
                            value={newUser.email}
                            onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                            placeholder="Enter email"
                            className="w-full"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                        <Dropdown
                            value={newUser.role}
                            options={roleOptions}
                            onChange={(e) => setNewUser({ ...newUser, role: e.value })}
                            placeholder="Select Role"
                            className="w-full"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                        <Dropdown
                            value={newUser.status}
                            options={statusOptions}
                            onChange={(e) => setNewUser({ ...newUser, status: e.value })}
                            placeholder="Select Status"
                            className="w-full"
                        />
                    </div>
                    <div className="flex gap-2 justify-end pt-4">
                        <Button
                            label="Cancel"
                            className="p-button-text"
                            onClick={() => setShowAddDialog(false)}
                        />
                        <Button
                            label="Add User"
                            style={{ backgroundColor: '#2d1b4e', borderColor: '#2d1b4e' }}
                            onClick={() => {
                                // Add user logic here (call API to create)
                                setShowAddDialog(false);
                            }}
                        />
                    </div>
                </div>
            </Dialog>

            {/* Edit User Dialog */}
            <Dialog
                header="Edit User"
                visible={showEditDialog}
                style={{ width: '500px' }}
                onHide={() => setShowEditDialog(false)}
            >
                {selectedUser && (
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">User</label>
                            <div className="p-3 bg-gray-50 rounded-lg">
                                <div className="text-sm font-medium text-gray-800">{selectedUser.user_name}</div>
                                <div className="text-xs text-gray-500">{selectedUser.email}</div>
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                            <Dropdown
                                value={editedUser.role}
                                options={roleOptions}
                                onChange={(e) => setEditedUser({ ...editedUser, role: e.value })}
                                placeholder="Select Role"
                                className="w-full"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                            <Dropdown
                                value={editedUser.status}
                                options={statusOptions}
                                onChange={(e) => setEditedUser({ ...editedUser, status: e.value })}
                                placeholder="Select Status"
                                className="w-full"
                            />
                        </div>
                        <div className="flex gap-2 justify-end pt-4">
                            <Button
                                label="Cancel"
                                className="p-button-text"
                                onClick={() => setShowEditDialog(false)}
                            />
                            <Button
                                label="Save Changes"
                                style={{ backgroundColor: '#2d1b4e', borderColor: '#2d1b4e' }}
                                onClick={handleEditUser}
                            />
                        </div>
                    </div>
                )}
            </Dialog>

            {/* Global CSS overrides to ensure tag colors win over PrimeReact defaults */}
            <style jsx global>{`
                /* Use !important so PrimeReact's built-in classes cannot override this */
                .tag-active {
                    background-color: #22c55e !important;
                    color: #ffffff !important;
                    border: none !important;
                }
                .tag-inactive {
                    background-color: #ef4444 !important;
                    color: #ffffff !important;
                    border: none !important;
                }
                .tag-pending {
                    background-color: #eab308 !important;
                    color: #ffffff !important;
                    border: none !important;
                }

                /* Make sure tag text has consistent font-size/padding if needed */
                .tag-active .p-tag-value,
                .tag-inactive .p-tag-value,
                .tag-pending .p-tag-value {
                    font-size: 11px !important;
                    padding: 4px 10px !important;
                }
            `}</style>
        </div>
    );
}
