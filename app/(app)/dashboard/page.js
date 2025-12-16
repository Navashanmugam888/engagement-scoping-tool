"use client";
import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Button } from "primereact/button";
import { Tag } from "primereact/tag";
import { Toast } from "primereact/toast";
import CalculateOutlinedIcon from "@mui/icons-material/CalculateOutlined";
import HistoryOutlinedIcon from "@mui/icons-material/HistoryOutlined";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

export default function Dashboard() {
  const router = useRouter();
  const { data: session } = useSession();
  const toast = useRef(null);
  const [greeting, setGreeting] = useState("");
  const [currentDate, setCurrentDate] = useState("");
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) {
      setGreeting("Good Morning");
    } else if (hour < 17) {
      setGreeting("Good Afternoon");
    } else {
      setGreeting("Good Evening");
    }

    const options = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    setCurrentDate(new Date().toLocaleDateString("en-US", options));

    if (session?.user?.email) {
      fetchSubmissions();
    }
  }, [session]);

  const fetchSubmissions = async () => {
    try {
      setLoading(true);
      const backendUrl =
        process.env.NEXT_PUBLIC_BACKEND_API_URL || "http://localhost:5000";
      const response = await fetch(
        `${backendUrl}/api/scoping/history?email=${session.user.email}`
      );

      if (response.ok) {
        const data = await response.json();
        const submissions = Array.isArray(data.submissions)
          ? data.submissions
          : Array.isArray(data)
          ? data
          : [];
        setSubmissions(submissions);
      } else {
        setSubmissions([]);
      }
    } catch (error) {
      console.error("Error fetching submissions:", error);
      setSubmissions([]);
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async (submissionId) => {
    try {
      toast.current?.show({
        severity: "info",
        summary: "Downloading",
        detail: "Preparing your report...",
      });

      const backendUrl =
        process.env.NEXT_PUBLIC_BACKEND_API_URL || "http://localhost:5000";
      const downloadUrl = `${backendUrl}/api/scoping/download/${submissionId}`;

      const response = await fetch(downloadUrl);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        if (response.status === 404 && errorData.error?.includes("not found")) {
          throw new Error("Report file not found");
        }
        throw new Error(
          errorData.error || `Server returned ${response.status}`
        );
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `scoping_report_${submissionId}.docx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.current?.show({
        severity: "success",
        summary: "Success",
        detail: "Report downloaded successfully",
      });
    } catch (error) {
      console.error("Download error:", error);
      toast.current?.show({
        severity: "error",
        summary: "Download Failed",
        detail: error.message || "Failed to download report",
        life: 6000,
      });
    }
  };

  const viewDetails = (rowData) => {
    router.push(`/scoping-history`);
  };

  const dateTemplate = (rowData) => {
    // Use submitted_at if timestamp is not available (fallback for API data)
    const dateValue = rowData.submitted_at || rowData.timestamp;

    if (!dateValue) {
      return <span className="text-gray-500">Invalid Date</span>;
    }

    try {
      const dateObj = new Date(dateValue);

      // Check if date is valid
      if (isNaN(dateObj.getTime())) {
        return <span className="text-gray-500">Invalid Date</span>;
      }

      return (
        <div className="flex flex-col">
          <span className="font-medium text-gray-700">
            {dateObj.toLocaleDateString()}
          </span>
          <span className="text-xs text-gray-500">
            {dateObj.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        </div>
      );
    } catch (error) {
      console.error("Date parsing error:", error);
      return <span className="text-gray-500">Invalid Date</span>;
    }
  };

  const tierTemplate = (rowData) => {
    return (
      <Tag
        value={rowData.tier || "N/A"}
        style={{ backgroundColor: "#443575", color: "white" }}
        className="text-xs"
      />
    );
  };

  const effortTemplate = (rowData) => {
    const months = rowData.total_months;
    return (
      <span className="font-medium text-gray-700">
        {months ? `${months.toFixed(1)} months` : "N/A"}
      </span>
    );
  };

  const statusTemplate = (rowData) => {
    const status = rowData.status || "Completed";
    return (
      <Tag
        value={status}
        style={{ backgroundColor: "#443575", color: "white" }}
        className="text-xs"
        rounded
      />
    );
  };

  const actionTemplate = (rowData) => {
    return (
      <div className="flex gap-3 justify-center items-center w-full">
        <Button
          icon="pi pi-eye"
          className="p-button-rounded p-button-text p-button-secondary p-button-sm hover:bg-[#443575]/10 hover:text-[#443575]"
          onClick={() => router.push(`/scoping-history/${rowData.id}`)}
          tooltip="View Details"
          tooltipPosition="top"
        />
        <Button
          icon="pi pi-download"
          className="p-button-rounded p-button-text p-button-success p-button-sm hover:text-green-600"
          onClick={() => downloadReport(rowData.id)}
          tooltip="Download Report"
          tooltipPosition="top"
        />
      </div>
    );
  };

  const userName = session?.user?.name || "User";

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <Toast ref={toast} />

      <div className="mb-4">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">
          {greeting}, {userName}!
        </h1>
        <p className="text-sm text-gray-600">
          Senior FCCS Consultant • FCCS Scoping Tool
        </p>
        <p className="text-xs text-gray-500 mt-0.5">{currentDate}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4 mb-4">
        <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 p-4 border border-gray-200">
          <div className="flex items-start gap-3">
            <div className="bg-[#443575] p-2.5 rounded-lg flex-shrink-0">
              <CalculateOutlinedIcon
                className="text-white"
                style={{ fontSize: 28 }}
              />
            </div>
            <div className="flex-1">
              <h2 className="text-lg font-bold text-gray-900 mb-1">
                New FCCS Scoping
              </h2>
              <p className="text-gray-600 text-xs mb-3 leading-relaxed">
                Start a new scoping calculation with our comprehensive 8-section
                form
              </p>
              <button
                onClick={() => router.push("/fccs-scoping")}
                className="inline-flex items-center gap-2 bg-[#443575] hover:bg-[#5a2d7a] text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 text-xs shadow-sm hover:shadow"
              >
                Get Started
                <ArrowForwardIcon fontSize="small" />
              </button>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 p-4 border border-gray-200">
          <div className="flex items-start gap-3">
            <div className="bg-blue-600 p-2.5 rounded-lg flex-shrink-0">
              <HistoryOutlinedIcon
                className="text-white"
                style={{ fontSize: 28 }}
              />
            </div>
            <div className="flex-1">
              <h2 className="text-lg font-bold text-gray-900 mb-1">
                View Scoping History
              </h2>
              <p className="text-gray-600 text-xs mb-3 leading-relaxed">
                Access all previous scoping projects with advanced search and
                filters
              </p>
              <button
                onClick={() => router.push("/scoping-history")}
                className="inline-flex items-center gap-2 bg-white hover:bg-gray-50 text-gray-900 px-4 py-2 rounded-lg font-medium transition-colors duration-200 border-2 border-gray-300 hover:border-gray-400 text-xs"
              >
                Get Started
                <ArrowForwardIcon fontSize="small" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-md border border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-gray-900">
                Your Scoping Submissions
              </h2>
              <p className="text-xs text-gray-600 mt-0.5">
                View and manage all your scoping projects
              </p>
            </div>
            <button
              onClick={() => router.push("/scoping-history")}
              className="text-[#443575] hover:text-[#5a2d7a] font-medium text-xs flex items-center gap-1 transition-colors"
            >
              View All Details
              <ArrowForwardIcon fontSize="small" />
            </button>
          </div>
        </div>

        <div className="p-4">
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#443575]"></div>
            </div>
          ) : submissions.length > 0 ? (
            <DataTable
              value={submissions}
              paginator
              rows={10}
              rowsPerPageOptions={[5, 10, 25, 50]}
              className="p-datatable-sm"
              stripedRows
              sortMode="multiple"
              emptyMessage="No submissions found"
              paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
              currentPageReportTemplate="Showing {first} to {last} of {totalRecords} submissions"
            >
              <Column
                field="user_name"
                header="Submitted By"
                sortable
                filter
                filterPlaceholder="Search by user"
                style={{ minWidth: "150px" }}
                body={(rowData) => (
                  <span className="text-gray-700 text-xs">
                    {rowData.user_name}
                  </span>
                )}
              />
              <Column
                field="tier"
                header="Tier"
                sortable
                body={tierTemplate}
                style={{ minWidth: "100px" }}
              />
              <Column
                field="total_months"
                header="Estimated Effort"
                sortable
                body={effortTemplate}
                style={{ minWidth: "130px" }}
              />
              <Column
                field="status"
                header="Status"
                body={statusTemplate}
                sortable
                style={{ minWidth: "120px" }}
              />
              <Column
                field="submitted_at"
                header="Submitted"
                sortable
                body={dateTemplate}
                style={{ minWidth: "150px" }}
              />
              <Column
                header="Actions"
                body={actionTemplate}
                style={{ minWidth: "150px" }}
              />
            </DataTable>
          ) : (
            <div className="text-center py-12">
              <HistoryOutlinedIcon
                className="text-gray-300 mx-auto mb-3"
                style={{ fontSize: 64 }}
              />
              <p className="text-gray-600 text-lg mb-2">No submissions yet</p>
              <p className="text-gray-400 text-sm mb-6">
                Start your first scoping project to see it here
              </p>
              <button
                onClick={() => router.push("/fccs-scoping")}
                className="inline-flex items-center gap-2 bg-[#443575] hover:bg-[#5a2d7a] text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
              >
                Create New Scoping
                <ArrowForwardIcon fontSize="small" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
