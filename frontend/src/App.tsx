
import { useEffect, useState, type ReactNode } from "react";
import {
  Activity,
  BarChart3,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Cpu,
  FileText,
  FolderOpen,
  Gauge,
  HeartPulse,
  LayoutDashboard,
  Menu,
  RefreshCw,
  Server,
  Settings,
  ShieldCheck,
  Terminal,
  X,
  AlertTriangle,
  HardDrive,
  MemoryStick,
  Upload,
  Play,
  Download,
  ScanSearch,
  FileCheck2,
  Files,
  XCircle,
} from "lucide-react";

import { api, getDownloadUrl } from "./api";

type Page =
  | "Dashboard"
  | "System Health"
  | "Performance"
  | "File Organizer"
  | "Log Analyzer"
  | "CSV Validator"
  | "Reports"
  | "Activity Log"
  | "Settings";

interface HealthData {
  hostname: string;
  operating_system: string;
  os_version: string;
  cpu: {
    usage: number;
    status: string;
  };
  memory: {
    usage: number;
    status: string;
  };
  disk: {
    usage: number;
    status: string;
  };
}

interface ProcessData {
  pid: number;
  name: string;
  cpu_percent: number;
  memory_percent: number;
}

interface LogResult {
  filename: string;
  total_entries: number;
  info: number;
  warning: number;
  error: number;
  errors: string[];
}

interface InvalidRecord {
  record: Record<string, string>;
  problems: string[];
}

interface CsvResult {
  filename?: string;
  clean_records?: number;
  invalid_records?: number;
  duplicate_records?: number;
  output_path?: string;
  download_url?: string;

  clean?: Record<string, string>[];

  invalid?: InvalidRecord[];

  duplicates?: Record<string, string>[];
}

interface MovedFile {
  file: string;
  category: string;
  destination: string;
}

interface SkippedFile {
  file: string;
  reason: string;
  destination?: string;
}

interface OrganizerError {
  file: string;
  reason: string;
  error_type?: string;
  operation?: string;
  destination?: string;
  suggestion?: string;
}

interface OrganizerResult {
  success: boolean;
  folder: string;
  moved: MovedFile[];
  skipped: SkippedFile[];
  errors: OrganizerError[];
  summary: {
    moved: number;
    skipped: number;
    errors: number;
  };
}

interface ReportResult {
  format: string;
  path: string;
  filename: string;
  download_url?: string;
}

function App() {
  const [activePage, setActivePage] =
    useState<Page>("Dashboard");

  const [sidebarOpen, setSidebarOpen] =
    useState(true);

  const [health, setHealth] =
    useState<HealthData | null>(null);

  const [apiConnected, setApiConnected] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const fetchHealth = async () => {
    try {
      setLoading(true);

      const data = await api.health();

      setHealth(data);
      setApiConnected(true);
    } catch (error) {
      console.error("Health API error:", error);
      setApiConnected(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();

    const interval = setInterval(
      fetchHealth,
      10000
    );

    return () => clearInterval(interval);
  }, []);

  const navigate = (page: Page) => {
    setActivePage(page);

    if (window.innerWidth < 900) {
      setSidebarOpen(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside
        className={`fixed left-0 top-0 z-40 flex h-screen w-72 flex-col border-r border-slate-800 bg-slate-900 transition-transform duration-300 ${
          sidebarOpen
            ? "translate-x-0"
            : "-translate-x-full"
        } lg:translate-x-0`}
      >
        <div className="flex h-20 items-center justify-between border-b border-slate-800 px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600">
              <ShieldCheck size={22} />
            </div>

            <div>
              <h1 className="text-sm font-bold text-white">
                IT Operations
              </h1>

              <p className="text-xs text-slate-400">
                Automation Platform
              </p>
            </div>
          </div>

          <button
            onClick={() => setSidebarOpen(false)}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white lg:hidden"
          >
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-4 py-6">
          <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Workspace
          </p>

          <NavItem
            icon={<LayoutDashboard size={18} />}
            label="Dashboard"
            active={activePage === "Dashboard"}
            onClick={() => navigate("Dashboard")}
          />

          <NavItem
            icon={<HeartPulse size={18} />}
            label="System Health"
            active={activePage === "System Health"}
            onClick={() => navigate("System Health")}
          />

          <NavItem
            icon={<Gauge size={18} />}
            label="Performance"
            active={activePage === "Performance"}
            onClick={() => navigate("Performance")}
          />

          <NavItem
            icon={<FolderOpen size={18} />}
            label="File Organizer"
            active={activePage === "File Organizer"}
            onClick={() => navigate("File Organizer")}
          />

          <NavItem
            icon={<FileText size={18} />}
            label="Log Analyzer"
            active={activePage === "Log Analyzer"}
            onClick={() => navigate("Log Analyzer")}
          />

          <NavItem
            icon={<ClipboardCheck size={18} />}
            label="CSV Validator"
            active={activePage === "CSV Validator"}
            onClick={() => navigate("CSV Validator")}
          />

          <div className="my-6 border-t border-slate-800" />

          <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Management
          </p>

          <NavItem
            icon={<BarChart3 size={18} />}
            label="Reports"
            active={activePage === "Reports"}
            onClick={() => navigate("Reports")}
          />

          <NavItem
            icon={<Activity size={18} />}
            label="Activity Log"
            active={activePage === "Activity Log"}
            onClick={() => navigate("Activity Log")}
          />

          <NavItem
            icon={<Settings size={18} />}
            label="Settings"
            active={activePage === "Settings"}
            onClick={() => navigate("Settings")}
          />
        </nav>

        <div className="border-t border-slate-800 p-4">
          <div className="rounded-xl bg-slate-950 p-4">
            <div className="flex items-center gap-2">
              <span
                className={`h-2.5 w-2.5 rounded-full ${
                  apiConnected
                    ? "bg-emerald-400"
                    : "bg-red-400"
                }`}
              />

              <span className="text-sm font-medium">
                {apiConnected
                  ? "API Connected"
                  : "API Offline"}
              </span>
            </div>

            <p className="mt-2 text-xs text-slate-500">
              FastAPI backend
            </p>
          </div>
        </div>
      </aside>

      <main className="min-h-screen lg:ml-72">
        <header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-slate-800 bg-slate-950/95 px-5 backdrop-blur lg:px-8">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white lg:hidden"
            >
              <Menu size={22} />
            </button>

            <div>
              <p className="text-xs text-slate-500">
                Workspace
              </p>

              <h2 className="text-xl font-semibold text-white">
                {activePage}
              </h2>
            </div>
          </div>

          <button
            onClick={fetchHealth}
            disabled={loading}
            className="flex items-center gap-2 rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-200 transition hover:bg-slate-800 disabled:opacity-50"
          >
            <RefreshCw
              size={16}
              className={
                loading ? "animate-spin" : ""
              }
            />

            <span className="hidden sm:inline">
              Refresh
            </span>
          </button>
        </header>

        <div className="p-5 lg:p-8">
          {activePage === "Dashboard" && (
            <Dashboard
              health={health}
              apiConnected={apiConnected}
              navigate={navigate}
            />
          )}

          {activePage === "System Health" && (
            <SystemHealth
              health={health}
              loading={loading}
              onRefresh={fetchHealth}
            />
          )}

          {activePage === "Performance" && (
            <Performance />
          )}

          {activePage === "File Organizer" && (
            <FileOrganizer />
          )}

          {activePage === "Log Analyzer" && (
            <LogAnalyzer />
          )}

          {activePage === "CSV Validator" && (
            <CSVValidator />
          )}

          {activePage === "Reports" && (
            <Reports />
          )}

          {activePage === "Activity Log" && (
            <PlaceholderPage
              icon={<Activity size={28} />}
              title="Activity Log"
              description="Review actions performed through the automation platform."
            />
          )}

          {activePage === "Settings" && (
            <PlaceholderPage
              icon={<Settings size={28} />}
              title="Settings"
              description="Configure the IT Operations Automation Platform."
            />
          )}
        </div>
      </main>
    </div>
  );
}

/* ---------------------------------- */
/* Dashboard                          */
/* ---------------------------------- */

function Dashboard({
  health,
  apiConnected,
  navigate,
}: {
  health: HealthData | null;
  apiConnected: boolean;
  navigate: (page: Page) => void;
}) {
  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <section>
        <p className="mb-2 text-sm text-blue-400">
          System Overview
        </p>

        <h3 className="text-3xl font-bold tracking-tight text-white">
          Welcome to your IT Operations Center
        </h3>

        <p className="mt-2 max-w-2xl text-slate-400">
          Monitor your computer, automate routine IT tasks
          and analyze system information from one place.
        </p>
      </section>

      <div
        className={`flex items-center justify-between rounded-2xl border p-5 ${
          apiConnected
            ? "border-emerald-500/20 bg-emerald-500/5"
            : "border-red-500/20 bg-red-500/5"
        }`}
      >
        <div className="flex items-center gap-4">
          <div
            className={`flex h-11 w-11 items-center justify-center rounded-xl ${
              apiConnected
                ? "bg-emerald-500/10 text-emerald-400"
                : "bg-red-500/10 text-red-400"
            }`}
          >
            {apiConnected ? (
              <CheckCircle2 size={22} />
            ) : (
              <AlertTriangle size={22} />
            )}
          </div>

          <div>
            <p className="font-semibold text-white">
              {apiConnected
                ? "System monitoring is online"
                : "Backend connection unavailable"}
            </p>

            <p className="text-sm text-slate-400">
              {apiConnected
                ? "Your FastAPI services are responding normally."
                : "Start the FastAPI server to enable live monitoring."}
            </p>
          </div>
        </div>
      </div>

      <section>
        <div className="mb-4 flex items-center justify-between">
          <h4 className="text-lg font-semibold text-white">
            System Status
          </h4>

          <button
            onClick={() =>
              navigate("System Health")
            }
            className="flex items-center gap-1 text-sm text-blue-400 hover:text-blue-300"
          >
            View details
            <ChevronRight size={16} />
          </button>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <MetricCard
            icon={<Cpu size={21} />}
            title="CPU Usage"
            value={
              health
                ? `${health.cpu.usage.toFixed(1)}%`
                : "--"
            }
            status={health?.cpu.status}
          />

          <MetricCard
            icon={<MemoryStick size={21} />}
            title="Memory Usage"
            value={
              health
                ? `${health.memory.usage.toFixed(1)}%`
                : "--"
            }
            status={health?.memory.status}
          />

          <MetricCard
            icon={<HardDrive size={21} />}
            title="Disk Usage"
            value={
              health
                ? `${health.disk.usage.toFixed(1)}%`
                : "--"
            }
            status={health?.disk.status}
          />
        </div>
      </section>

      <section>
        <h4 className="mb-4 text-lg font-semibold text-white">
          Quick Actions
        </h4>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <QuickAction
            icon={<HeartPulse size={22} />}
            title="System Health"
            description="Check your system"
            onClick={() =>
              navigate("System Health")
            }
          />

          <QuickAction
            icon={<Gauge size={22} />}
            title="Performance"
            description="Monitor resources"
            onClick={() =>
              navigate("Performance")
            }
          />

          <QuickAction
            icon={<FolderOpen size={22} />}
            title="File Organizer"
            description="Organize files"
            onClick={() =>
              navigate("File Organizer")
            }
          />

          <QuickAction
            icon={<FileText size={22} />}
            title="Log Analyzer"
            description="Analyze logs"
            onClick={() =>
              navigate("Log Analyzer")
            }
          />
        </div>
      </section>

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <div className="mb-5 flex items-center gap-3">
          <Server
            className="text-blue-400"
            size={21}
          />

          <div>
            <h4 className="font-semibold text-white">
              System Information
            </h4>

            <p className="text-sm text-slate-500">
              Current machine information
            </p>
          </div>
        </div>

        <div className="grid gap-5 sm:grid-cols-3">
          <InfoItem
            label="Hostname"
            value={health?.hostname || "--"}
          />

          <InfoItem
            label="Operating System"
            value={
              health?.operating_system || "--"
            }
          />

          <InfoItem
            label="OS Version"
            value={
              health?.os_version || "--"
            }
          />
        </div>
      </section>
    </div>
  );
}

/* ---------------------------------- */
/* System Health                      */
/* ---------------------------------- */

function SystemHealth({
  health,
  loading,
  onRefresh,
}: {
  health: HealthData | null;
  loading: boolean;
  onRefresh: () => void;
}) {
  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <section>
        <p className="mb-2 text-sm text-blue-400">
          Monitoring
        </p>

        <h3 className="text-3xl font-bold text-white">
          System Health
        </h3>

        <p className="mt-2 text-slate-400">
          Live health information from your Windows machine.
        </p>
      </section>

      <div className="grid gap-5 md:grid-cols-3">
        <HealthCard
          icon={<Cpu size={24} />}
          title="CPU"
          usage={health?.cpu.usage}
          status={health?.cpu.status}
        />

        <HealthCard
          icon={<MemoryStick size={24} />}
          title="Memory"
          usage={health?.memory.usage}
          status={health?.memory.status}
        />

        <HealthCard
          icon={<HardDrive size={24} />}
          title="Disk"
          usage={health?.disk.usage}
          status={health?.disk.status}
        />
      </div>

      <div className="flex justify-end">
        <button
          onClick={onRefresh}
          disabled={loading}
          className="flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50"
        >
          <RefreshCw
            size={17}
            className={
              loading ? "animate-spin" : ""
            }
          />
          Run Health Check
        </button>
      </div>

      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        <div className="mb-5 flex items-center gap-3">
          <Terminal
            size={20}
            className="text-blue-400"
          />

          <h4 className="font-semibold text-white">
            Machine Details
          </h4>
        </div>

        <div className="grid gap-5 md:grid-cols-3">
          <InfoItem
            label="Hostname"
            value={
              health?.hostname || "Unavailable"
            }
          />

          <InfoItem
            label="Operating System"
            value={
              health?.operating_system ||
              "Unavailable"
            }
          />

          <InfoItem
            label="Version"
            value={
              health?.os_version || "Unavailable"
            }
          />
        </div>
      </div>
    </div>
  );
}

/* ---------------------------------- */
/* Performance                        */
/* ---------------------------------- */

function Performance() {
  const [processes, setProcesses] =
    useState<ProcessData[]>([]);

  const [sortBy, setSortBy] =
    useState<"cpu" | "memory">("cpu");

  const [loading, setLoading] =
    useState(false);

  const loadPerformance = async () => {
    try {
      setLoading(true);

      const result =
        await api.performance(sortBy, 10);

      setProcesses(
        Array.isArray(result.processes)
          ? result.processes
          : []
      );
    } catch (error) {
      console.error(
        "Performance API error:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPerformance();
  }, [sortBy]);

  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <section>
        <p className="mb-2 text-sm text-blue-400">
          Resource Monitoring
        </p>

        <h3 className="text-3xl font-bold text-white">
          Performance
        </h3>

        <p className="mt-2 text-slate-400">
          Monitor the processes consuming the most system resources.
        </p>
      </section>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex rounded-xl border border-slate-800 bg-slate-900 p-1">
          <button
            onClick={() => setSortBy("cpu")}
            className={`rounded-lg px-4 py-2 text-sm ${
              sortBy === "cpu"
                ? "bg-blue-600 text-white"
                : "text-slate-400 hover:text-white"
            }`}
          >
            CPU
          </button>

          <button
            onClick={() =>
              setSortBy("memory")
            }
            className={`rounded-lg px-4 py-2 text-sm ${
              sortBy === "memory"
                ? "bg-blue-600 text-white"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Memory
          </button>
        </div>

        <button
          onClick={loadPerformance}
          disabled={loading}
          className="flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2 text-sm font-semibold hover:bg-blue-500 disabled:opacity-50"
        >
          <RefreshCw
            size={16}
            className={
              loading ? "animate-spin" : ""
            }
          />
          Refresh
        </button>
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-800 bg-slate-950">
              <tr>
                <th className="px-5 py-4 text-slate-400">
                  PID
                </th>

                <th className="px-5 py-4 text-slate-400">
                  Process
                </th>

                <th className="px-5 py-4 text-slate-400">
                  CPU
                </th>

                <th className="px-5 py-4 text-slate-400">
                  Memory
                </th>
              </tr>
            </thead>

            <tbody>
              {processes.map((process) => (
                <tr
                  key={process.pid}
                  className="border-b border-slate-800 last:border-0"
                >
                  <td className="px-5 py-4 text-slate-500">
                    {process.pid}
                  </td>

                  <td className="px-5 py-4 font-medium text-white">
                    {process.name}
                  </td>

                  <td className="px-5 py-4 text-blue-400">
                    {Number(
                      process.cpu_percent
                    ).toFixed(1)}
                    %
                  </td>

                  <td className="px-5 py-4 text-purple-400">
                    {Number(
                      process.memory_percent
                    ).toFixed(1)}
                    %
                  </td>
                </tr>
              ))}

              {!loading &&
                processes.length === 0 && (
                  <tr>
                    <td
                      colSpan={4}
                      className="px-5 py-10 text-center text-slate-500"
                    >
                      No process information available.
                    </td>
                  </tr>
                )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

/* ---------------------------------- */
/* File Organizer                     */
/* ---------------------------------- */

function FileOrganizer() {
  const [folderPath, setFolderPath] =
    useState("");

  const [result, setResult] =
    useState<OrganizerResult | null>(null);

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const organize = async () => {
    if (!folderPath.trim()) {
      setError(
        "Please enter a folder path."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data =
        await api.organizeFiles(
          folderPath
        );

      setResult(data as OrganizerResult);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to organize files."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ToolPage
      icon={<FolderOpen size={28} />}
      title="File Organizer"
      description="Organize files automatically into categorized folders."
    >
      <div className="space-y-5">
        <label className="block">
          <span className="mb-2 block text-sm font-medium text-slate-300">
            Folder path
          </span>

          <input
            value={folderPath}
            onChange={(e) =>
              setFolderPath(e.target.value)
            }
            placeholder="C:\Users\Ntando.Badla\Downloads"
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none focus:border-blue-500"
          />
        </label>

        {error && (
          <ErrorMessage message={error} />
        )}

        <button
          onClick={organize}
          disabled={
            loading || !folderPath.trim()
          }
          className="flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-500 disabled:opacity-50"
        >
          <Play size={17} />

          {loading
            ? "Organizing..."
            : "Organize Files"}
        </button>

        {result && (
          <OrganizerResultView
            result={result}
          />
        )}
      </div>
    </ToolPage>
  );
}

function OrganizerResultView({
  result,
}: {
  result: OrganizerResult;
}) {
  const moved = Array.isArray(result.moved)
    ? result.moved
    : [];

  const skipped = Array.isArray(
    result.skipped
  )
    ? result.skipped
    : [];

  const errors = Array.isArray(
    result.errors
  )
    ? result.errors
    : [];

  const summary = result.summary ?? {
    moved: moved.length,
    skipped: skipped.length,
    errors: errors.length,
  };

  return (
    <div className="mt-8 space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h4 className="text-lg font-semibold text-white">
            Organizer Result
          </h4>

          <p className="mt-1 break-all text-sm text-slate-500">
            {result.folder}
          </p>
        </div>

        {result.success ? (
          <StatusPill
            icon={
              <CheckCircle2 size={15} />
            }
            text="Completed"
            type="success"
          />
        ) : (
          <StatusPill
            icon={
              <AlertTriangle size={15} />
            }
            text="Completed with Errors"
            type="error"
          />
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <SummaryCard
          title="Files Moved"
          value={summary.moved}
          icon={
            <CheckCircle2 size={22} />
          }
          type="success"
        />

        <SummaryCard
          title="Files Skipped"
          value={summary.skipped}
          icon={
            <AlertTriangle size={22} />
          }
          type="warning"
        />

        <SummaryCard
          title="Errors"
          value={summary.errors}
          icon={<XCircle size={22} />}
          type="error"
        />
      </div>

      {moved.length > 0 && (
        <div className="overflow-hidden rounded-xl border border-emerald-700/30 bg-slate-950">
          <div className="border-b border-emerald-700/30 px-5 py-4">
            <div className="flex items-center gap-2">
              <CheckCircle2
                size={18}
                className="text-emerald-400"
              />

              <h4 className="font-semibold text-emerald-400">
                Moved Files
              </h4>
            </div>

            <p className="mt-1 text-sm text-slate-500">
              Files successfully organized into categories.
            </p>
          </div>

          <div className="divide-y divide-slate-800">
            {moved.map((item, index) => (
              <div
                key={`${item.file}-${index}`}
                className="flex flex-col gap-3 px-5 py-4 md:flex-row md:items-center md:justify-between"
              >
                <div className="flex min-w-0 items-center gap-3">
                  <Files
                    size={18}
                    className="shrink-0 text-emerald-400"
                  />

                  <div className="min-w-0">
                    <p className="font-medium text-white">
                      {item.file}
                    </p>

                    <p className="break-all text-xs text-slate-500">
                      {item.destination}
                    </p>
                  </div>
                </div>

                <span className="w-fit rounded-full bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-400">
                  {item.category}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {skipped.length > 0 && (
        <div className="overflow-hidden rounded-xl border border-amber-700/30 bg-slate-950">
          <div className="border-b border-amber-700/30 px-5 py-4">
            <div className="flex items-center gap-2">
              <AlertTriangle
                size={18}
                className="text-amber-400"
              />

              <h4 className="font-semibold text-amber-400">
                Skipped Files
              </h4>
            </div>

            <p className="mt-1 text-sm text-slate-500">
              These files were not moved.
            </p>
          </div>

          <div className="divide-y divide-slate-800">
            {skipped.map((item, index) => (
              <div
                key={`${item.file}-${index}`}
                className="px-5 py-4"
              >
                <p className="font-medium text-white">
                  {item.file}
                </p>

                <p className="mt-1 text-sm text-amber-300">
                  {item.reason}
                </p>

                {item.destination && (
                  <p className="mt-1 break-all text-xs text-slate-500">
                    Destination:{" "}
                    {item.destination}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {errors.length > 0 && (
        <div className="overflow-hidden rounded-xl border border-red-700/40 bg-red-950/10">
          <div className="border-b border-red-700/30 px-5 py-4">
            <div className="flex items-center gap-2">
              <XCircle
                size={18}
                className="text-red-400"
              />

              <h4 className="font-semibold text-red-400">
                Errors
              </h4>
            </div>

            <p className="mt-1 text-sm text-slate-500">
              Problems encountered while organizing files.
            </p>
          </div>

          <div className="divide-y divide-red-900/30">
            {errors.map((item, index) => (
              <div
                key={`${item.file}-${index}`}
                className="px-5 py-5"
              >
                <p className="font-semibold text-white">
                  {item.file}
                </p>

                {item.error_type && (
                  <p className="mt-1 text-xs font-semibold uppercase tracking-wide text-red-400">
                    {item.error_type}
                  </p>
                )}

                <p className="mt-2 text-sm text-red-300">
                  {item.reason}
                </p>

                {item.operation && (
                  <p className="mt-2 text-xs text-slate-500">
                    Operation:{" "}
                    {item.operation}
                  </p>
                )}

                {item.destination && (
                  <p className="mt-1 break-all text-xs text-slate-500">
                    Destination:{" "}
                    {item.destination}
                  </p>
                )}

                {item.suggestion && (
                  <div className="mt-3 rounded-lg border border-red-800/40 bg-red-950/30 p-3">
                    <p className="text-xs font-semibold text-red-400">
                      Suggested action
                    </p>

                    <p className="mt-1 text-sm text-slate-300">
                      {item.suggestion}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {summary.moved === 0 &&
        summary.skipped === 0 &&
        summary.errors === 0 && (
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-6 text-center">
            <FolderOpen
              size={30}
              className="mx-auto text-slate-600"
            />

            <p className="mt-3 font-medium text-white">
              No files were found to organize.
            </p>

            <p className="mt-1 text-sm text-slate-500">
              The selected folder may be empty or contain no supported files.
            </p>
          </div>
        )}
    </div>
  );
}

/* ---------------------------------- */
/* Log Analyzer                       */
/* ---------------------------------- */

function LogAnalyzer() {
  const [file, setFile] =
    useState<File | null>(null);

  const [result, setResult] =
    useState<LogResult | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const analyze = async () => {
    if (!file) {
      setError(
        "Please select a log file."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");

      const data =
        await api.analyzeLog(file);

      setResult(data as LogResult);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to analyze the log file."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ToolPage
      icon={<FileText size={28} />}
      title="Log Analyzer"
      description="Analyze application and system logs for errors and warnings."
    >
      <FileUpload
        accept=".log,.txt"
        file={file}
        onChange={setFile}
      />

      {error && (
        <div className="mt-5">
          <ErrorMessage
            message={error}
          />
        </div>
      )}

      <button
        onClick={analyze}
        disabled={!file || loading}
        className="mt-5 flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
      >
        <ScanSearch size={17} />

        {loading
          ? "Analyzing..."
          : "Analyze Log"}
      </button>

      {result && (
        <div className="mt-6 grid gap-4 md:grid-cols-4">
          <ResultMetric
            title="Total Entries"
            value={result.total_entries}
          />

          <ResultMetric
            title="INFO"
            value={result.info}
          />

          <ResultMetric
            title="WARNING"
            value={result.warning}
          />

          <ResultMetric
            title="ERROR"
            value={result.error}
          />
        </div>
      )}
    </ToolPage>
  );
}

/* ---------------------------------- */
/* CSV Validator                      */
/* ---------------------------------- */

function CSVValidator() {
  const [file, setFile] =
    useState<File | null>(null);

  const [result, setResult] =
    useState<CsvResult | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const validate = async () => {
    if (!file) {
      setError(
        "Please select a CSV file."
      );
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data =
        await api.validateCsv(file);

      setResult(data as CsvResult);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to validate the CSV file."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ToolPage
      icon={<ClipboardCheck size={28} />}
      title="CSV Validator"
      description="Validate CSV files and identify data quality issues."
    >
      <FileUpload
        accept=".csv"
        file={file}
        onChange={(selectedFile) => {
          setFile(selectedFile);
          setResult(null);
          setError("");
        }}
      />

      {error && (
        <div className="mt-5">
          <ErrorMessage
            message={error}
          />
        </div>
      )}

      <button
        onClick={validate}
        disabled={!file || loading}
        className="mt-5 flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
      >
        <ClipboardCheck size={17} />

        {loading
          ? "Validating..."
          : "Validate CSV"}
      </button>

      {result && (
        <CSVResultView
          result={result}
        />
      )}
    </ToolPage>
  );
}

function CSVResultView({
  result,
}: {
  result: CsvResult;
}) {
  /*
   * IMPORTANT:
   * The backend may omit invalid, duplicates or clean.
   * Always normalize them to arrays before using .length,
   * .map(), etc.
   */

  const invalidRecords =
    Array.isArray(result.invalid)
      ? result.invalid
      : [];

  const duplicates =
    Array.isArray(result.duplicates)
      ? result.duplicates
      : [];

  const cleanRecords =
    Array.isArray(result.clean)
      ? result.clean
      : [];

  const cleanCount =
    typeof result.clean_records ===
    "number"
      ? result.clean_records
      : cleanRecords.length;

  const invalidCount =
    typeof result.invalid_records ===
    "number"
      ? result.invalid_records
      : invalidRecords.length;

  const duplicateCount =
    typeof result.duplicate_records ===
    "number"
      ? result.duplicate_records
      : duplicates.length;

  return (
    <div className="mt-8 space-y-6">
      {/* Header */}
      <div>
        <h4 className="text-lg font-semibold text-white">
          Validation Results
        </h4>

        <p className="mt-1 break-all text-sm text-slate-500">
          {result.filename ||
            "CSV file"}
        </p>
      </div>

      {/* Summary */}
      <div className="grid gap-4 md:grid-cols-3">
        <SummaryCard
          title="Clean Records"
          value={cleanCount}
          icon={
            <FileCheck2 size={22} />
          }
          type="success"
        />

        <SummaryCard
          title="Invalid Records"
          value={invalidCount}
          icon={<XCircle size={22} />}
          type="error"
        />

        <SummaryCard
          title="Duplicates"
          value={duplicateCount}
          icon={<Files size={22} />}
          type="warning"
        />
      </div>

      {/* Clean records */}
      <div className="rounded-xl border border-emerald-700/30 bg-emerald-950/10 p-5">
        <div className="flex items-center gap-3">
          <CheckCircle2
            size={20}
            className="text-emerald-400"
          />

          <div>
            <h4 className="font-semibold text-emerald-400">
              Clean Records
            </h4>

            <p className="text-sm text-slate-500">
              {cleanCount} records passed
              validation.
            </p>
          </div>
        </div>
      </div>

      {/* Invalid records */}
      {invalidRecords.length > 0 ? (
        <div className="overflow-hidden rounded-xl border border-red-700/30 bg-slate-950">
          <div className="border-b border-red-700/30 px-5 py-4">
            <div className="flex items-center gap-2">
              <XCircle
                size={18}
                className="text-red-400"
              />

              <h4 className="font-semibold text-red-400">
                Invalid Records
              </h4>
            </div>

            <p className="mt-1 text-sm text-slate-500">
              Records containing missing or invalid data.
            </p>
          </div>

          <div className="divide-y divide-slate-800">
            {invalidRecords.map(
              (item, index) => {
                const record =
                  item?.record &&
                  typeof item.record ===
                    "object"
                    ? item.record
                    : {};

                const problems =
                  Array.isArray(
                    item?.problems
                  )
                    ? item.problems
                    : [];

                return (
                  <div
                    key={index}
                    className="px-5 py-5"
                  >
                    <div className="mb-3 flex items-center justify-between">
                      <span className="rounded-full bg-red-500/10 px-3 py-1 text-xs font-semibold text-red-400">
                        Record #
                        {index + 1}
                      </span>
                    </div>

                    <div className="grid gap-2 sm:grid-cols-2">
                      {Object.entries(
                        record
                      ).map(
                        ([key, value]) => (
                          <div
                            key={key}
                            className="rounded-lg bg-slate-900 p-3"
                          >
                            <p className="text-xs uppercase tracking-wide text-slate-500">
                              {key}
                            </p>

                            <p className="mt-1 break-all text-sm text-slate-200">
                              {String(
                                value ??
                                  "(empty)"
                              )}
                            </p>
                          </div>
                        )
                      )}
                    </div>

                    {problems.length >
                      0 && (
                      <div className="mt-4 rounded-lg border border-red-800/30 bg-red-950/20 p-4">
                        <p className="text-xs font-semibold uppercase tracking-wide text-red-400">
                          Problems
                        </p>

                        <ul className="mt-2 space-y-1">
                          {problems.map(
                            (
                              problem,
                              problemIndex
                            ) => (
                              <li
                                key={
                                  problemIndex
                                }
                                className="text-sm text-red-300"
                              >
                                • {problem}
                              </li>
                            )
                          )}
                        </ul>
                      </div>
                    )}
                  </div>
                );
              }
            )}
          </div>
        </div>
      ) : (
        <div className="rounded-xl border border-emerald-700/30 bg-emerald-950/10 p-5">
          <p className="font-medium text-emerald-400">
            No invalid records found.
          </p>
        </div>
      )}

      {/* Duplicates */}
      {duplicates.length > 0 ? (
        <div className="overflow-hidden rounded-xl border border-amber-700/30 bg-slate-950">
          <div className="border-b border-amber-700/30 px-5 py-4">
            <div className="flex items-center gap-2">
              <Files
                size={18}
                className="text-amber-400"
              />

              <h4 className="font-semibold text-amber-400">
                Duplicate Records
              </h4>
            </div>

            <p className="mt-1 text-sm text-slate-500">
              Records detected as duplicates.
            </p>
          </div>

          <div className="divide-y divide-slate-800">
            {duplicates.map(
              (record, index) => (
                <div
                  key={index}
                  className="grid gap-2 px-5 py-4 sm:grid-cols-2"
                >
                  {Object.entries(
                    record || {}
                  ).map(
                    ([key, value]) => (
                      <div
                        key={key}
                        className="rounded-lg bg-slate-900 p-3"
                      >
                        <p className="text-xs uppercase tracking-wide text-slate-500">
                          {key}
                        </p>

                        <p className="mt-1 break-all text-sm text-slate-200">
                          {String(
                            value ??
                              "(empty)"
                          )}
                        </p>
                      </div>
                    )
                  )}
                </div>
              )
            )}
          </div>
        </div>
      ) : (
        <div className="rounded-xl border border-emerald-700/30 bg-emerald-950/10 p-5">
          <p className="font-medium text-emerald-400">
            No duplicate records found.
          </p>
        </div>
      )}

      {/* Download cleaned CSV */}
      {result.output_path && (
        <div className="rounded-xl border border-blue-700/30 bg-blue-950/10 p-5">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="flex items-center gap-2">
                <FileCheck2
                  size={19}
                  className="text-blue-400"
                />

                <h4 className="font-semibold text-white">
                  Cleaned CSV
                </h4>
              </div>

              <p className="mt-1 text-sm text-slate-500">
                A cleaned version of the CSV was generated.
              </p>

              <p className="mt-2 break-all text-xs text-slate-600">
                {result.output_path}
              </p>
            </div>

            {result.download_url ? (
              <a
                href={getDownloadUrl(
                  result.download_url
                )}
                download
                className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-500"
              >
                <Download size={17} />
                Download Cleaned CSV
              </a>
            ) : (
              <div className="rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-slate-500">
                Download endpoint unavailable
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------------------------------- */
/* Reports                            */
/* ---------------------------------- */

function Reports() {
  const [format, setFormat] =
    useState<
      "json" | "csv" | "html" | "text"
    >("html");

  const [result, setResult] =
    useState<ReportResult | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const generate = async () => {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      const data =
        await api.generateReport(format);

      setResult(data as ReportResult);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to generate report."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ToolPage
      icon={<BarChart3 size={28} />}
      title="Reports"
      description="Generate system health reports using your existing report generator."
    >
      <div className="grid gap-4 sm:grid-cols-4">
        {(
          [
            "json",
            "csv",
            "html",
            "text",
          ] as const
        ).map((item) => (
          <button
            key={item}
            onClick={() =>
              setFormat(item)
            }
            className={`rounded-xl border px-4 py-4 text-sm font-semibold uppercase ${
              format === item
                ? "border-blue-500 bg-blue-500/10 text-blue-400"
                : "border-slate-800 bg-slate-950 text-slate-400 hover:border-slate-700 hover:text-white"
            }`}
          >
            {item}
          </button>
        ))}
      </div>

      {error && (
        <div className="mt-5">
          <ErrorMessage
            message={error}
          />
        </div>
      )}

      <button
        onClick={generate}
        disabled={loading}
        className="mt-6 flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-semibold hover:bg-blue-500 disabled:opacity-50"
      >
        <BarChart3 size={17} />

        {loading
          ? "Generating..."
          : `Generate ${format.toUpperCase()} Report`}
      </button>

      {result && (
        <div className="mt-6 rounded-xl border border-emerald-700/30 bg-emerald-950/10 p-5">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="flex items-center gap-2">
                <CheckCircle2
                  size={19}
                  className="text-emerald-400"
                />

                <p className="font-semibold text-white">
                  Report Generated
                </p>
              </div>

              <p className="mt-2 text-sm text-slate-400">
                {result.filename}
              </p>

              <p className="mt-1 break-all text-xs text-slate-600">
                {result.path}
              </p>
            </div>

            {result.download_url ? (
              <a
                href={getDownloadUrl(
                  result.download_url
                )}
                download
                className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-emerald-600 px-5 py-3 text-sm font-semibold text-white hover:bg-emerald-500"
              >
                <Download size={17} />
                Download Report
              </a>
            ) : (
              <div className="rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-slate-500">
                Download endpoint unavailable
              </div>
            )}
          </div>
        </div>
      )}
    </ToolPage>
  );
}

/* ---------------------------------- */
/* Reusable Components                */
/* ---------------------------------- */

function NavItem({
  icon,
  label,
  active,
  onClick,
}: {
  icon: ReactNode;
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`mb-1 flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium transition ${
        active
          ? "bg-blue-600 text-white shadow-lg shadow-blue-900/20"
          : "text-slate-400 hover:bg-slate-800 hover:text-white"
      }`}
    >
      {icon}
      <span>{label}</span>
    </button>
  );
}

function MetricCard({
  icon,
  title,
  value,
  status,
}: {
  icon: ReactNode;
  title: string;
  value: string;
  status?: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <div className="mb-5 flex items-center justify-between">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-800 text-blue-400">
          {icon}
        </div>

        {status && (
          <StatusBadge status={status} />
        )}
      </div>

      <p className="text-sm text-slate-500">
        {title}
      </p>

      <p className="mt-1 text-3xl font-bold text-white">
        {value}
      </p>
    </div>
  );
}

function HealthCard({
  icon,
  title,
  usage,
  status,
}: {
  icon: ReactNode;
  title: string;
  usage?: number;
  status?: string;
}) {
  const percentage = usage ?? 0;

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-800 text-blue-400">
            {icon}
          </div>

          <h4 className="font-semibold text-white">
            {title}
          </h4>
        </div>

        {status && (
          <StatusBadge status={status} />
        )}
      </div>

      <div className="mb-3 flex items-end justify-between">
        <span className="text-4xl font-bold text-white">
          {usage !== undefined
            ? `${percentage.toFixed(1)}%`
            : "--"}
        </span>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-blue-500 transition-all duration-500"
          style={{
            width: `${Math.min(
              percentage,
              100
            )}%`,
          }}
        />
      </div>
    </div>
  );
}

function StatusBadge({
  status,
}: {
  status: string;
}) {
  const normalized =
    status.toUpperCase();

  const classes =
    normalized === "CRITICAL"
      ? "bg-red-500/10 text-red-400"
      : normalized === "WARNING"
      ? "bg-amber-500/10 text-amber-400"
      : normalized === "UNKNOWN"
      ? "bg-slate-500/10 text-slate-400"
      : "bg-emerald-500/10 text-emerald-400";

  return (
    <span
      className={`rounded-full px-2.5 py-1 text-xs font-semibold ${classes}`}
    >
      {normalized}
    </span>
  );
}

function StatusPill({
  icon,
  text,
  type,
}: {
  icon: ReactNode;
  text: string;
  type:
    | "success"
    | "warning"
    | "error";
}) {
  const classes =
    type === "success"
      ? "bg-emerald-500/10 text-emerald-400"
      : type === "warning"
      ? "bg-amber-500/10 text-amber-400"
      : "bg-red-500/10 text-red-400";

  return (
    <span
      className={`inline-flex w-fit items-center gap-2 rounded-full px-3 py-1.5 text-sm font-medium ${classes}`}
    >
      {icon}
      {text}
    </span>
  );
}

function SummaryCard({
  title,
  value,
  icon,
  type,
}: {
  title: string;
  value: number;
  icon: ReactNode;
  type:
    | "success"
    | "warning"
    | "error";
}) {
  const styles =
    type === "success"
      ? {
          border:
            "border-emerald-700/30",
          bg: "bg-emerald-950/20",
          icon:
            "bg-emerald-500/10 text-emerald-400",
          value: "text-emerald-400",
        }
      : type === "warning"
      ? {
          border:
            "border-amber-700/30",
          bg: "bg-amber-950/20",
          icon:
            "bg-amber-500/10 text-amber-400",
          value: "text-amber-400",
        }
      : {
          border:
            "border-red-700/30",
          bg: "bg-red-950/20",
          icon:
            "bg-red-500/10 text-red-400",
          value: "text-red-400",
        };

  return (
    <div
      className={`rounded-xl border ${styles.border} ${styles.bg} p-5`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">
            {title}
          </p>

          <p
            className={`mt-2 text-3xl font-bold ${styles.value}`}
          >
            {value}
          </p>
        </div>

        <div
          className={`rounded-lg p-3 ${styles.icon}`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
}

function QuickAction({
  icon,
  title,
  description,
  onClick,
}: {
  icon: ReactNode;
  title: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="group rounded-2xl border border-slate-800 bg-slate-900 p-5 text-left transition hover:-translate-y-0.5 hover:border-slate-700 hover:bg-slate-800"
    >
      <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
        {icon}
      </div>

      <div className="flex items-center justify-between">
        <div>
          <h5 className="font-semibold text-white">
            {title}
          </h5>

          <p className="mt-1 text-sm text-slate-500">
            {description}
          </p>
        </div>

        <ChevronRight
          size={18}
          className="text-slate-600 transition group-hover:translate-x-1 group-hover:text-blue-400"
        />
      </div>
    </button>
  );
}

function InfoItem({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wider text-slate-500">
        {label}
      </p>

      <p className="mt-1 truncate font-medium text-slate-200">
        {value}
      </p>
    </div>
  );
}

function ToolPage({
  icon,
  title,
  description,
  children,
}: {
  icon: ReactNode;
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <section>
        <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-400">
          {icon}
        </div>

        <h3 className="text-3xl font-bold text-white">
          {title}
        </h3>

        <p className="mt-2 text-slate-400">
          {description}
        </p>
      </section>

      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
        {children}
      </section>
    </div>
  );
}

function FileUpload({
  accept,
  file,
  onChange,
}: {
  accept: string;
  file: File | null;
  onChange: (
    file: File | null
  ) => void;
}) {
  return (
    <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-950 p-10 text-center hover:border-blue-500">
      <Upload
        className="mb-3 text-blue-400"
        size={30}
      />

      <p className="font-medium text-white">
        {file
          ? file.name
          : "Choose a file"}
      </p>

      <p className="mt-1 text-sm text-slate-500">
        {file
          ? `${(
              file.size / 1024
            ).toFixed(1)} KB`
          : "Click to upload"}
      </p>

      <input
        type="file"
        accept={accept}
        className="hidden"
        onChange={(event) =>
          onChange(
            event.target.files?.[0] ??
              null
          )
        }
      />
    </label>
  );
}

function ResultMetric({
  title,
  value,
}: {
  title: string;
  value: number;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
      <p className="text-sm text-slate-500">
        {title}
      </p>

      <p className="mt-2 text-3xl font-bold text-white">
        {value}
      </p>
    </div>
  );
}

function ErrorMessage({
  message,
}: {
  message: string;
}) {
  return (
    <div className="rounded-xl border border-red-700/40 bg-red-950/20 p-4">
      <div className="flex items-start gap-3">
        <AlertTriangle
          size={19}
          className="mt-0.5 shrink-0 text-red-400"
        />

        <div>
          <p className="font-semibold text-red-400">
            Operation failed
          </p>

          <p className="mt-1 break-words text-sm text-red-300">
            {message}
          </p>
        </div>
      </div>
    </div>
  );
}

function PlaceholderPage({
  icon,
  title,
  description,
}: {
  icon: ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="mx-auto max-w-7xl">
      <div className="flex min-h-[500px] flex-col items-center justify-center rounded-2xl border border-dashed border-slate-800 bg-slate-900/50 p-8 text-center">
        <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-400">
          {icon}
        </div>

        <h3 className="text-2xl font-bold text-white">
          {title}
        </h3>

        <p className="mt-2 max-w-md text-slate-500">
          {description}
        </p>

        <div className="mt-6 rounded-lg bg-slate-800 px-4 py-2 text-sm text-slate-400">
          Backend module coming next
        </div>
      </div>
    </div>
  );
}

export default App;

