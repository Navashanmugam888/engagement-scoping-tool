"use client";
import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { signOut, useSession } from "next-auth/react";
import LogoutOutlinedIcon from "@mui/icons-material/LogoutOutlined";
import CalculateOutlinedIcon from "@mui/icons-material/CalculateOutlined";
import HistoryOutlinedIcon from "@mui/icons-material/HistoryOutlined";
import DashboardOutlinedIcon from "@mui/icons-material/DashboardOutlined";
import PeopleOutlinedIcon from "@mui/icons-material/PeopleOutlined";
import AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import { useSidebar } from "../SidebarContext";

export default function Sidebar() {
  const pathname = usePathname();
  const { data: session, status } = useSession();
  const { isExpanded, setIsExpanded } = useSidebar();

  // Don't render anything while loading
  if (status === "loading") {
    return null;
  }

  // Don't render if not authenticated
  if (status === "unauthenticated") {
    return null;
  }

  const items = [
    {
      label: "Dashboard",
      href: "/dashboard",
      icon: <DashboardOutlinedIcon fontSize="small" />,
      activeClass: "bg-[#443575] text-white shadow-md",
    },
    {
      label: "Scoping Tool",
      href: "/fccs-scoping",
      icon: <CalculateOutlinedIcon fontSize="small" />,
      activeClass: "bg-[#443575] text-white shadow-md",
    },
    {
      label: "History",
      href: "/scoping-history",
      icon: <HistoryOutlinedIcon fontSize="small" />,
      activeClass: "bg-[#443575] text-white shadow-md",
    },
  ];

  // Admin-only items
  const adminItems =
    session?.user?.role === "SUPER_ADMIN"
      ? [
          // {
          //   label: "Admin Dashboard",
          //   href: "/admin/dashboard",
          //   icon: <AdminPanelSettingsOutlinedIcon fontSize="small" />,
          //   activeClass: "bg-[#443575] text-white shadow-md",
          //   section: "Administration",
          // },
          {
            label: "Manage Users",
            href: "/admin/users",
            icon: <PeopleOutlinedIcon fontSize="small" />,
            activeClass: "bg-[#443575] text-white shadow-md",
            section: "Administration",
          },
          {
            label: "Manage Scoping",
            href: "/admin/role-allocations",
            icon: <CalculateOutlinedIcon fontSize="small" />,
            activeClass: "bg-[#443575] text-white shadow-md",
            section: "Administration",
          },
        ]
      : [];

  const handleLogout = async () => {
    await signOut({ callbackUrl: "/" });
  };

  return (
    <aside
      className={`fixed top-20 left-0 h-[calc(100vh-70px)] bg-[#2d1b4e] shadow-lg z-40 flex flex-col py-4 transition-all duration-300 ${
        isExpanded ? "w-64" : "w-20"
      }`}
    >
      {/* Toggle Button */}
      <div className="flex justify-end px-3 mb-3">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-white hover:bg-white/10 p-1.5 rounded-lg transition-colors duration-200"
          title={isExpanded ? "Collapse" : "Expand"}
        >
          {isExpanded ? (
            <ChevronLeftIcon fontSize="small" />
          ) : (
            <MenuIcon fontSize="small" />
          )}
        </button>
      </div>

      {/* Logo/Brand Area */}
      <div
        className={`px-4 mb-4 transition-all duration-300 ${
          isExpanded ? "opacity-100" : "opacity-0 h-0"
        }`}
      >
        {isExpanded && (
          <div className="text-white">
            <h2 className="text-lg font-bold text-white">FCCS Tool</h2>
            <p className="text-[10px] text-white/80 mt-0.5">
              Scoping Management
            </p>
          </div>
        )}
      </div>

      {/* Navigation Items */}
      <nav className="flex flex-col gap-2 px-3 flex-1 overflow-y-auto">
        {/* Main Navigation */}
        {isExpanded && (
          <div className="text-white/60 text-[10px] font-semibold uppercase tracking-wider px-3 mb-1">
            Main Navigation
          </div>
        )}
        {items.map(({ label, href, icon, activeClass }) => {
          const isActive = pathname.startsWith(href);

          return (
            <Link
              key={href}
              href={href}
              title={label}
              className={`
                flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 cursor-pointer
                ${
                  isActive
                    ? activeClass
                    : "text-white hover:bg-white/10 hover:text-white"
                }
                ${isExpanded ? "justify-start" : "justify-center"}
              `}
            >
              {React.cloneElement(icon, { style: { color: "white" } })}
              {isExpanded && (
                <span className="font-medium text-xs whitespace-nowrap">
                  {label}
                </span>
              )}
            </Link>
          );
        })}

        {/* Admin Section */}
        {adminItems.length > 0 && (
          <>
            {isExpanded && (
              <div className="text-white/60 text-[10px] font-semibold uppercase tracking-wider px-3 mb-1 mt-4">
                Administration
              </div>
            )}
            {adminItems.map(({ label, href, icon, activeClass }) => {
              const isActive = pathname.startsWith(href);

              return (
                <Link
                  key={href}
                  href={href}
                  title={label}
                  className={`
                    flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 cursor-pointer
                    ${
                      isActive
                        ? activeClass
                        : "text-white hover:bg-white/10 hover:text-white"
                    }
                    ${isExpanded ? "justify-start" : "justify-center"}
                  `}
                >
                  {React.cloneElement(icon, { style: { color: "white" } })}
                  {isExpanded && (
                    <span className="font-medium text-xs whitespace-nowrap">
                      {label}
                    </span>
                  )}
                </Link>
              );
            })}
          </>
        )}
      </nav>

      {/* Logout Section */}
      <div className="px-3 mt-auto">
        {isExpanded && session?.user && (
          <div className="mb-0 px-3 py-2 bg-white/10 rounded-lg">
            <p className="text-[10px] text-white/70 mb-0.5">Signed in as</p>
            <p className="text-xs text-white font-medium truncate">
              {session.user.name}
            </p>
            <p className="text-[10px] text-white/70 truncate">
              {session.user.email}
            </p>
          </div>
        )}

        <button
          title="Logout"
          onClick={handleLogout}
          className={`
              flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 cursor-pointer 
              text-white hover:bg-red-500/20 w-full
              ${isExpanded ? "justify-start" : "justify-center"}
            `}
        >
          <LogoutOutlinedIcon fontSize="small" />
          {isExpanded && <span className="font-medium text-xs">Logout</span>}
        </button>
      </div>
    </aside>
  );
}
