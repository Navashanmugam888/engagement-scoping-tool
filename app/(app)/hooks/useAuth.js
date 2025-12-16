'use client';

import { useSession } from 'next-auth/react';

export default function useAuth() {
  const { data: session, status } = useSession();

  const isLoading = status === 'loading';
  const isAuthenticated = status === 'authenticated';
  const user = session?.user || null;

  const hasRole = (role) => {
    if (!user) return false;
    if (Array.isArray(role)) {
      return role.includes(user.role);
    }
    return user.role === role;
  };

  const isSuperAdmin = () => hasRole('SUPER_ADMIN');
  const isSuperUser = () => hasRole('SUPER_USER');
  const isHistoryViewer = () => hasRole('HISTORY_VIEWER');
  const isScopingEditor = () => hasRole('SCOPING_EDITOR');
  const isGuest = () => hasRole('GUEST');

  const canAccessAdmin = () => isSuperAdmin();
  const canEditScoping = () => hasRole(['SUPER_ADMIN', 'SUPER_USER', 'SCOPING_EDITOR']);
  const canViewHistory = () => hasRole(['SUPER_ADMIN', 'SUPER_USER', 'HISTORY_VIEWER']);

  return {
    session,
    user,
    isLoading,
    isAuthenticated,
    hasRole,
    isSuperAdmin,
    isSuperUser,
    isHistoryViewer,
    isScopingEditor,
    isGuest,
    canAccessAdmin,
    canEditScoping,
    canViewHistory,
  };
}
