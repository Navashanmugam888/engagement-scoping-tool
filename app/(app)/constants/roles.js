// User roles configuration
export const ROLES = {
  SUPER_ADMIN: 'SUPER_ADMIN',
  SUPER_USER: 'SUPER_USER',
  HISTORY_VIEWER: 'HISTORY_VIEWER',
  SCOPING_EDITOR: 'SCOPING_EDITOR',
  GUEST: 'GUEST'
};

export const ROLE_OPTIONS = [
  { label: 'Administrator', value: ROLES.SUPER_ADMIN },
  { label: 'Super User', value: ROLES.SUPER_USER },
  { label: 'History Viewer', value: ROLES.HISTORY_VIEWER },
  { label: 'Scoping Editor', value: ROLES.SCOPING_EDITOR },
  { label: 'Guest', value: ROLES.GUEST }
];

export const ROLE_CONFIG = {
  [ROLES.SUPER_ADMIN]: { label: 'Administrator', color: '#3b82f6' },
  [ROLES.SUPER_USER]: { label: 'Super User', color: '#8b5cf6' },
  [ROLES.HISTORY_VIEWER]: { label: 'History Viewer', color: '#f59e0b' },
  [ROLES.SCOPING_EDITOR]: { label: 'Scoping Editor', color: '#10b981' },
  [ROLES.GUEST]: { label: 'Guest', color: '#6b7280' }
};
