'use client';
import { useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import AdminPanelSettingsOutlinedIcon from '@mui/icons-material/AdminPanelSettingsOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';
import AssignmentOutlinedIcon from '@mui/icons-material/AssignmentOutlined';
import BarChartOutlinedIcon from '@mui/icons-material/BarChartOutlined';

export default function AdminDashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/');
    } else if (status === 'authenticated' && session?.user?.role !== 'SUPER_ADMIN') {
      router.push('/dashboard');
    }
  }, [status, session, router]);

  if (status === 'loading' || !session || session?.user?.role !== 'SUPER_ADMIN') {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2d1b4e]"></div>
      </div>
    );
  }

  const statsCards = [
    {
      title: 'Total Users',
      value: '124',
      icon: <PeopleOutlinedIcon fontSize="large" />,
      color: 'bg-blue-500',
      change: '+12%'
    },
    {
      title: 'Active Sessions',
      value: '48',
      icon: <AssignmentOutlinedIcon fontSize="large" />,
      color: 'bg-green-500',
      change: '+5%'
    },
    {
      title: 'Pending Approvals',
      value: '8',
      icon: <AdminPanelSettingsOutlinedIcon fontSize="large" />,
      color: 'bg-orange-500',
      change: '-3%'
    },
    {
      title: 'System Health',
      value: '98%',
      icon: <BarChartOutlinedIcon fontSize="large" />,
      color: 'bg-purple-500',
      change: '+2%'
    }
  ];

  return (
    <div className="p-4">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
          <AdminPanelSettingsOutlinedIcon fontSize="large" className="text-[#2d1b4e]" />
          Admin Dashboard
        </h1>
        <p className="text-sm text-gray-600 mt-1">
          Monitor and manage your system from this central hub
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {statsCards.map((stat, index) => (
          <div
            key={index}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between mb-3">
              <div className={`${stat.color} text-white p-2.5 rounded-lg`}>
                {stat.icon}
              </div>
              <span className={`text-xs font-semibold ${stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                {stat.change}
              </span>
            </div>
            <h3 className="text-xs text-gray-600 mb-1">{stat.title}</h3>
            <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            onClick={() => router.push('/admin/users')}
            className="flex items-center gap-3 p-3 bg-[#2d1b4e] text-white rounded-lg hover:bg-[#3d2b5e] transition-colors"
          >
            <PeopleOutlinedIcon fontSize="small" />
            <span className="text-sm font-medium">Manage Users</span>
          </button>
          <button
            onClick={() => router.push('/admin/role-allocations')}
            className="flex items-center gap-3 p-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <AssignmentOutlinedIcon fontSize="small" />
            <span className="text-sm font-medium">Manage Scoping</span>
          </button>
          <button
            className="flex items-center gap-3 p-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            <BarChartOutlinedIcon fontSize="small" />
            <span className="text-sm font-medium">View Reports</span>
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h2>
        <div className="space-y-3">
          <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm text-gray-800">New user registered</p>
              <p className="text-xs text-gray-500">2 minutes ago</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm text-gray-800">Role updated for user</p>
              <p className="text-xs text-gray-500">15 minutes ago</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm text-gray-800">Pending approval request</p>
              <p className="text-xs text-gray-500">1 hour ago</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
