import React from 'react';
import { Tag } from 'primereact/tag';
import { ROLE_CONFIG } from '../../constants/roles';

export default function RoleBadge({ role }) {
  const config = ROLE_CONFIG[role] || ROLE_CONFIG['GUEST'];
  
  return (
    <Tag 
      value={config.label} 
      style={{ 
        backgroundColor: config.color, 
        color: 'white', 
        fontSize: '11px', 
        padding: '4px 10px', 
        borderRadius: '6px', 
        border: 'none' 
      }}
    />
  );
}
