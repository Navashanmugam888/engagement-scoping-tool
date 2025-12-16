export const apiRequest = async (url, options = {}) => {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || data.message || 'An error occurred');
  }

  return data;
};

export const getUsers = async () => {
  return apiRequest('/api/admin/users');
};

export const updateUser = async (userId, userData) => {
  return apiRequest(`/api/admin/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  });
};

export const deleteUser = async (userId) => {
  return apiRequest(`/api/admin/users/${userId}`, {
    method: 'DELETE',
  });
};

export const getScopingSubmissions = async () => {
  return apiRequest('/api/scoping/submissions');
};

export const getScopingSubmission = async (id) => {
  return apiRequest(`/api/scoping/submissions/${id}`);
};
