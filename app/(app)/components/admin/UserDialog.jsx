'use client';

import React from 'react';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import Button from '../common/Button';
import { ROLE_OPTIONS } from '../../constants/roles';
import { STATUS_OPTIONS } from '../../constants/status';

export default function UserDialog({ 
  visible, 
  onHide, 
  user, 
  onChange, 
  onSave,
  title = 'Edit User'
}) {
  return (
    <Dialog
      visible={visible}
      onHide={onHide}
      header={title}
      modal
      style={{ width: '500px' }}
    >
      <div className="flex flex-col gap-4 p-2">
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-2">
            User Name
          </label>
          <InputText
            value={user?.user_name || ''}
            onChange={(e) => onChange('user_name', e.target.value)}
            className="w-full text-sm"
            style={{ fontSize: '12px', padding: '8px' }}
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-700 mb-2">
            Email
          </label>
          <InputText
            value={user?.email || ''}
            onChange={(e) => onChange('email', e.target.value)}
            className="w-full text-sm"
            style={{ fontSize: '12px', padding: '8px' }}
            disabled
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-700 mb-2">
            Role
          </label>
          <Dropdown
            value={user?.role || ''}
            options={ROLE_OPTIONS}
            onChange={(e) => onChange('role', e.value)}
            className="w-full text-sm"
            style={{ fontSize: '12px' }}
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-700 mb-2">
            Status
          </label>
          <Dropdown
            value={user?.status || ''}
            options={STATUS_OPTIONS}
            onChange={(e) => onChange('status', e.value)}
            className="w-full text-sm"
            style={{ fontSize: '12px' }}
          />
        </div>

        <div className="flex justify-end gap-2 mt-4">
          <Button
            label="Cancel"
            variant="outlined"
            onClick={onHide}
          />
          <Button
            label="Save"
            variant="primary"
            onClick={onSave}
          />
        </div>
      </div>
    </Dialog>
  );
}
