'use client';
import { Suspense } from 'react';
import PageLoader from '../Loader/Loader';
import { ToastContainer } from 'react-toastify';

export default function SubLayout({ children }) {
  return (
    // FIX: Removed the horizontal padding classes (px-4 md:px-8)
    // The padding is now handled by the dashboard page itself.
    <main className="transition-all duration-300 min-h-screen">
      <Suspense fallback={<PageLoader />}>
        <ToastContainer />
        <div>{children}</div>
      </Suspense>
    </main>
  );
}