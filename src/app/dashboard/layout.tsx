'use client';

import { useState } from 'react';
import Sidebar from '../../components/dashboard/Sidebar';
import NavBar from '../../components/dashboard/NavBar';
import { useAuth } from '../../components/providers/AuthProvider';

// Force dynamic rendering to prevent SSR issues
export const dynamic = 'force-dynamic';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Redirect to signin if not authenticated
  if (!user) {
    if (typeof window !== 'undefined') {
      window.location.href = '/signin';
    }
    return null;
  }

  return (
    <div className="h-full flex bg-gray-50">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
      
      {/* Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden lg:ml-0">
        {/* NavBar */}
        <NavBar onMenuClick={toggleSidebar} />
        
        {/* Page content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
          <div className="container mx-auto px-4 py-6 lg:px-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
