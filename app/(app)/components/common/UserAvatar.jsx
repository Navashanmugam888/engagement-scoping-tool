import React from 'react';
import { Avatar } from 'primereact/avatar';

export default function UserAvatar({ name, size = 'md', className = '' }) {
  const getInitials = (fullName) => {
    if (!fullName) return '?';
    return fullName.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  const sizes = {
    sm: { width: '28px', height: '28px', fontSize: '11px' },
    md: { width: '36px', height: '36px', fontSize: '14px' },
    lg: { width: '48px', height: '48px', fontSize: '18px' }
  };

  return (
    <Avatar 
      label={getInitials(name)} 
      shape="circle" 
      className={`bg-[#2d1b4e] text-white ${className}`}
      style={sizes[size]}
    />
  );
}
