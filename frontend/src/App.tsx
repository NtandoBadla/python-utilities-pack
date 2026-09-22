import { useEffect, useState } from "react";
import {
  Activity,
  Cpu,
  HardDrive,
  LayoutDashboard,
  MemoryStick,
  RefreshCw,
  Server,
  Settings,
  Terminal,
} from "lucide-react";

interface Metric {
  usage: number;
  status: string;
}

interface HealthData {
  hostname: string;
  operating_system: string;
  os_version: string;
  cpu: Metric;
  memory: Metric;
  disk: Metric;
}

function statusClass(status: string) {
  switch (status) {
    case "CRITICAL":
      return "text-red-400 bg-red-400/10 border-red-400/20";
    case "WARNING":
      return "text-yellow-400 bg-yellow-400/10 border-yellow-400/20";
    default:
      return "text-green-400 bg-green-400/10 border-green-400/20";
  }
}

function MetricCard({
  title,
  value,
  status,
  icon: Icon,
}: {
  title: string;
  value: number;
  status: string;
  icon: React.ElementType;
}) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800/70 p-5 shadow-lg">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-slate-700 p-2">
            <Icon size={20} />
          </div>
          <span className="text-sm text-slate-400">{title}</span>
        </div>

        <span
          className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${statusClass(
            status
          )}`}
        >
          {status}
        </span>
      </div>

      <div className="mt-5">
        <span className="text-4xl font-bold">{value.toFixed(1)}%</span>
      </div>

      <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-700">
        <div
          className="h-full rounded-full bg-current"
          style={{ width: `${Math.min(value, 100)}%` }}
        />
      </div>
    </div>
  );
}

function App() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchHealth = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch("http://127.0.0.1:8000/api/health/");

      if (!response.ok) {
        throw new Error("Failed to retrieve system health.");
      }

      const data = await response.json();
      setHealth(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();

    const interval = setInterval(fetchHealth, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="hidden w-64 border-r border-slate-800 bg-slate-900 p-5 md:block">
          <div className="mb-8 flex items-center gap-3">
            <div className="rounded-xl bg-indigo-500 p-2">
              <Terminal size={22} />
            </div>

            <div>
              <h1 className="font-bold">IT Ops</h1>
              <p className="text-xs text-slate-500">Automation Platform</p>
            </div>
          </div>

          <nav className="space-y-2">
            <button className="flex w-full items-center gap-3 rounded-xl bg-indigo-500/10 px-4 py-3 text-left text-indigo-400">
              <LayoutDashboard size={18} />
              Dashboard
            </button>

            <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-slate-400 hover:bg-slate-800">
              <Activity size={18} />
              System Health
            </button>

            <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-slate-400 hover:bg-slate-800">
              <Cpu size={18} />
              Performance
            </button>

            <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-slate-400 hover:bg-slate-800">
              <Server size={18} />
              File Tools
            </button>

            <button className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-slate-400 hover:bg-slate-800">
              <Settings size={18} />
              Settings
            </button>
          </nav>
        </aside>

        {/* Main */}
        <main className="flex-1 p-6 md:p-8">
          <header className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-center">
            <div>
              <p className="text-sm text-indigo-400">IT OPERATIONS</p>
              <h2 className="mt-1 text-3xl font-bold">
                System Dashboard
              </h2>
              <p className="mt-2 text-slate-400">
                Monitor and automate your IT environment.
              </p>
            </div>

            <button
              onClick={fetchHealth}
              className="flex items-center justify-center gap-2 rounded-xl border border-slate-700 bg-slate-800 px-4 py-2.5 text-sm hover:bg-slate-700"
            >
              <RefreshCw size={16} />
              Refresh
            </button>
          </header>

          {loading && !health && (
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-slate-400">
              Checking system health...
            </div>
          )}

          {error && (
            <div className="mb-6 rounded-2xl border border-red-500/20 bg-red-500/10 p-5 text-red-400">
              {error}
            </div>
          )}

          {health && (
            <>
              {/* System info */}
              <section className="mb-6 grid gap-4 md:grid-cols-3">
                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
                  <p className="text-sm text-slate-500">Hostname</p>
                  <p className="mt-2 font-semibold">{health.hostname}</p>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
                  <p className="text-sm text-slate-500">Operating System</p>
                  <p className="mt-2 font-semibold">
                    {health.operating_system}
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
                  <p className="text-sm text-slate-500">OS Version</p>
                  <p className="mt-2 font-semibold">{health.os_version}</p>
                </div>
              </section>

              {/* Metrics */}
              <section className="grid gap-5 md:grid-cols-3">
                <MetricCard
                  title="CPU Usage"
                  value={health.cpu.usage}
                  status={health.cpu.status}
                  icon={Cpu}
                />

                <MetricCard
                  title="Memory Usage"
                  value={health.memory.usage}
                  status={health.memory.status}
                  icon={MemoryStick}
                />

                <MetricCard
                  title="Disk Usage"
                  value={health.disk.usage}
                  status={health.disk.status}
                  icon={HardDrive}
                />
              </section>

              {/* Status */}
              <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold">Monitoring Status</h3>
                    <p className="mt-1 text-sm text-slate-500">
                      Health information refreshes automatically every 10
                      seconds.
                    </p>
                  </div>

                  <div className="flex items-center gap-2 text-sm text-green-400">
                    <span className="h-2 w-2 rounded-full bg-green-400" />
                    API Connected
                  </div>
                </div>
              </section>
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;