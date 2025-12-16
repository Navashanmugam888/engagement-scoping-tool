// app/(auth)/layout.js
'use client';
import React from 'react';

// This is the "clean" layout for your login page.
// It has no Header or Sidebar.
export default function AuthLayout({ children }) {
  return (
    <>
      {children}
    </>
  );
}