import React from 'react';
import { STATUS_CONFIG } from '../../constants/status';

export default function StatusBadge({ status }) {
  const config = STATUS_CONFIG[status] || STATUS_CONFIG['PENDING'];
  
  return (
    <span 
      style={{ 
        display: 'inline-block',
        backgroundColor: config.bgColor,
        color: config.textColor,
        fontSize: '10px', 
        padding: '3px 8px',
        borderRadius: '4px',
        fontWeight: '500',
        textAlign: 'center'
      }}
    >
      {config.label}
    </span>
  );
}
