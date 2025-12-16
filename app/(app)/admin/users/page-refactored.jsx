'use client';

import React, { useState } from 'react';
import { Toast } from 'primereact/toast';
import { InputText } from 'primereact/inputtext';
import { useRouter } from 'next/navigation';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';

import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import UserTable from '../../components/admin/UserTable';
import UserDialog from '../../components/admin/UserDialog';
import useAuth from '../../hooks/useAuth';
import useUsers from '../../hooks/useUsers';
import useToast from '../../hooks/useToast';

export default function ManageUsers() {
  const [globalFilter, setGlobalFilter] = useState('');
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [editedUser, setEditedUser] = useState({});

  const { isSuperAdmin } = useAuth();
  const { users, loading, updateUser, deleteUser } = useUsers();
  const { toastRef, showSuccess, showError } = useToast();
  const router = useRouter();

  // Redirect if not super admin
  React.useEffect(() => {
    if (!loading && !isSuperAdmin()) {
      router.push('/dashboard');
    }
  }, [isSuperAdmin, loading, router]);

  const openEditDialog = (user) => {
    setSelectedUser(user);
    setEditedUser({
      user_name: user.user_name,
      email: user.email,
      role: user.role,
      status: user.status
    });
    setShowEditDialog(true);
  };

  const handleEditUser = async () => {
    if (!editedUser.user_name || !editedUser.email) {
      showError('Validation Error', 'Name and email are required');
      return;
    }

    const result = await updateUser(selectedUser.email, {
      user_name: editedUser.user_name,
      role: editedUser.role,
      status: editedUser.status
    });

    if (result.success) {
      showSuccess('Success', 'User updated successfully');
      setShowEditDialog(false);
      setSelectedUser(null);
    } else {
      showError('Error', result.error || 'Failed to update user');
    }
  };

  const handleDeleteUser = async (user) => {
    if (!confirm(`Are you sure you want to delete ${user.user_name}?`)) return;

    const result = await deleteUser(user.email);

    if (result.success) {
      showSuccess('Success', 'User deleted successfully');
    } else {
      showError('Error', result.error || 'Failed to delete user');
    }
  };

  const handleDialogChange = (field, value) => {
    setEditedUser(prev => ({ ...prev, [field]: value }));
  };

  const headerActions = (
    <>
      <span className="p-input-icon-left">
        <i className="pi pi-search" style={{ fontSize: '11px' }} />
        <InputText
          type="search"
          value={globalFilter}
          onChange={(e) => setGlobalFilter(e.target.value)}
          placeholder="Search users..."
          style={{ fontSize: '11px', padding: '6px 10px 6px 32px', width: '250px' }}
        />
      </span>
      <Button
        label="Admin Dashboard"
        icon="pi pi-home"
        onClick={() => router.push('/admin/dashboard')}
        variant="primary"
        size="sm"
      />
    </>
  );

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  return (
    <div className="p-4">
      <Toast ref={toastRef} />
      
      <PageHeader
        title="Manage Users"
        subtitle="View and manage all system users"
        icon={PeopleOutlinedIcon}
        actions={headerActions}
      />

      <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-md">
        <UserTable
          users={users}
          globalFilterValue={globalFilter}
          onEdit={openEditDialog}
          onDelete={handleDeleteUser}
        />
      </div>

      <UserDialog
        visible={showEditDialog}
        onHide={() => setShowEditDialog(false)}
        user={editedUser}
        onChange={handleDialogChange}
        onSave={handleEditUser}
        title="Edit User"
      />
    </div>
  );
}
