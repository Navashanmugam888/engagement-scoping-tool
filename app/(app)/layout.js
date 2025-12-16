'use client';
import Sidebar from '@/app/(app)/components/Sidebar/Sidebar';
import Header from '@/app/(app)/components/Header/Header';
import SubLayout from '@/app/(app)/components/SubLayout/SubLayout';
import PageLoader from '@/app/(app)/components/Loader/Loader';
import { SidebarProvider, useSidebar } from '@/app/(app)/components/SidebarContext';

function AppLayoutContent({ children }) {
  const { isExpanded } = useSidebar();
  
  return (
    <div className="bg-gray-100 min-h-screen">
      <PageLoader />
      <Header />
      <Sidebar />
      <div 
        className="flex flex-col min-h-screen pt-20 transition-all duration-300"
        style={{ marginLeft: isExpanded ? '220px' : '60px' }}
      >
        <SubLayout>{children}</SubLayout>
      </div>
    </div>
  );
}

export default function AppLayout({ children }) {
  return (
    <SidebarProvider>
      <AppLayoutContent>{children}</AppLayoutContent>
    </SidebarProvider>
  );
}
