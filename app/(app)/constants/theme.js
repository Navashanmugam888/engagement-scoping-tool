// Theme colors and styles
export const COLORS = {
  primary: '#2d1b4e',
  primaryHover: '#3d2b5e',
  secondary: '#8b5cf6',
  success: '#22c55e',
  warning: '#eab308',
  danger: '#ef4444',
  info: '#3b82f6',
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827'
  }
};

export const BUTTON_STYLES = {
  primary: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.primary,
    color: 'white',
    fontSize: '10px',
    fontWeight: '400'
  },
  secondary: {
    backgroundColor: 'white',
    borderColor: COLORS.gray[300],
    color: COLORS.gray[700],
    fontSize: '10px',
    fontWeight: '400'
  },
  outlined: {
    backgroundColor: 'transparent',
    borderColor: COLORS.primary,
    color: COLORS.primary,
    fontSize: '10px',
    fontWeight: '400'
  }
};
