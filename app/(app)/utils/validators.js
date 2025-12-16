export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validateRequired = (value) => {
  return value !== null && value !== undefined && value !== '';
};

export const validateUserName = (name) => {
  if (!name || name.trim().length < 2) {
    return { valid: false, error: 'Name must be at least 2 characters' };
  }
  if (name.length > 100) {
    return { valid: false, error: 'Name must be less than 100 characters' };
  }
  return { valid: true, error: null };
};

export const validateUserEmail = (email) => {
  if (!validateRequired(email)) {
    return { valid: false, error: 'Email is required' };
  }
  if (!validateEmail(email)) {
    return { valid: false, error: 'Invalid email format' };
  }
  return { valid: true, error: null };
};

export const validatePercentage = (value) => {
  const num = parseFloat(value);
  if (isNaN(num)) return false;
  return num >= 0 && num <= 100;
};
