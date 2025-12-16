'use client';

import { useState, useEffect } from 'react';
import { getUsers, updateUser, deleteUser } from '../utils/api';

export default function useUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getUsers();
      setUsers(data.users || []);
    } catch (err) {
      console.error('Error fetching users:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const updateUserData = async (userId, userData) => {
    try {
      await updateUser(userId, userData);
      await fetchUsers();
      return { success: true };
    } catch (err) {
      console.error('Error updating user:', err);
      return { success: false, error: err.message };
    }
  };

  const deleteUserData = async (userId) => {
    try {
      await deleteUser(userId);
      await fetchUsers();
      return { success: true };
    } catch (err) {
      console.error('Error deleting user:', err);
      return { success: false, error: err.message };
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return {
    users,
    loading,
    error,
    refetch: fetchUsers,
    updateUser: updateUserData,
    deleteUser: deleteUserData,
  };
}
