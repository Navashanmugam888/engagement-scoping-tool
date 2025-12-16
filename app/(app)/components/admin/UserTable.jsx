'use client';

import React from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button as PrimeButton } from 'primereact/button';
import UserAvatar from '../common/UserAvatar';
import RoleBadge from '../common/RoleBadge';
import StatusBadge from '../common/StatusBadge';
import { formatDate } from '../../utils/formatters';

export default function UserTable({ 
  users, 
  globalFilterValue,
  onEdit,
  onDelete 
}) {
  const userTemplate = (rowData) => (
    <div className="flex items-center gap-2">
      <UserAvatar name={rowData.user_name} size="sm" />
      <div>
        <div className="font-medium text-sm">{rowData.user_name}</div>
        <div className="text-xs text-gray-500">{rowData.email}</div>
      </div>
    </div>
  );

  const roleTemplate = (rowData) => <RoleBadge role={rowData.role} />;

  const statusTemplate = (rowData) => <StatusBadge status={rowData.status} />;

  const lastLoginTemplate = (rowData) => (
    <span className="text-xs text-gray-600">{formatDate(rowData.last_login)}</span>
  );

  const actionsTemplate = (rowData) => (
    <div className="flex gap-2">
      <PrimeButton
        icon="pi pi-pencil"
        className="p-button-text p-button-sm"
        onClick={() => onEdit(rowData)}
        style={{ padding: '4px 8px', fontSize: '11px' }}
      />
      <PrimeButton
        icon="pi pi-trash"
        className="p-button-text p-button-danger p-button-sm"
        onClick={() => onDelete(rowData)}
        style={{ padding: '4px 8px', fontSize: '11px' }}
      />
    </div>
  );

  return (
    <DataTable
      value={users}
      paginator
      rows={10}
      globalFilter={globalFilterValue}
      emptyMessage="No users found"
      className="text-xs"
      style={{ fontSize: '12px' }}
    >
      <Column field="user_name" header="User" body={userTemplate} style={{ minWidth: '200px' }} />
      <Column field="role" header="Role" body={roleTemplate} style={{ minWidth: '120px' }} />
      <Column field="status" header="Status" body={statusTemplate} style={{ minWidth: '100px' }} />
      <Column field="last_login" header="Last Login" body={lastLoginTemplate} style={{ minWidth: '150px' }} />
      <Column header="Actions" body={actionsTemplate} style={{ minWidth: '100px', textAlign: 'center' }} />
    </DataTable>
  );
}
