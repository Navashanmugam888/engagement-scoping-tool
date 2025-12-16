// User status configuration
export const STATUS = {
  ACTIVE: 'ACTIVE',
  INACTIVE: 'INACTIVE',
  PENDING: 'PENDING'
};

export const STATUS_OPTIONS = [
  { label: 'Active', value: STATUS.ACTIVE },
  { label: 'Inactive', value: STATUS.INACTIVE },
  { label: 'Pending', value: STATUS.PENDING }
];

export const STATUS_CONFIG = {
  [STATUS.ACTIVE]: { bgColor: '#dcfce7', textColor: '#166534', label: 'Active' },
  [STATUS.INACTIVE]: { bgColor: '#fee2e2', textColor: '#991b1b', label: 'Inactive' },
  [STATUS.PENDING]: { bgColor: '#fef9c3', textColor: '#854d0e', label: 'Pending' }
};
