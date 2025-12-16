import React from 'react';
import { Button as PrimeButton } from 'primereact/button';
import { BUTTON_STYLES } from '../../constants/theme';

export default function Button({ 
  label, 
  icon, 
  onClick, 
  variant = 'primary',
  size = 'md',
  className = '',
  style = {},
  ...props 
}) {
  const sizeStyles = {
    sm: { padding: '6px 12px', fontSize: '9px' },
    md: { padding: '8px 16px', fontSize: '10px' },
    lg: { padding: '10px 20px', fontSize: '12px' }
  };

  const buttonStyle = {
    ...BUTTON_STYLES[variant],
    ...sizeStyles[size],
    ...style
  };

  return (
    <PrimeButton
      label={label}
      icon={icon}
      onClick={onClick}
      className={className}
      style={buttonStyle}
      {...props}
    />
  );
}
