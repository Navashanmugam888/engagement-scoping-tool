import React from 'react';

export default function PageHeader({ 
  title, 
  subtitle, 
  icon: Icon, 
  actions 
}) {
  return (
    <div className="bg-white rounded-xl p-4 mb-4 border border-gray-200 shadow-md">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {Icon && <Icon fontSize="large" className="text-[#2d1b4e]" />}
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
            {subtitle && <p className="text-xs text-gray-500 mt-0.5">{subtitle}</p>}
          </div>
        </div>
        {actions && (
          <div className="flex items-center gap-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
}
