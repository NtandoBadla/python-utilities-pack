const API_URL = "http://127.0.0.1:8000";

async function request<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, options);

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || "API request failed");
  }

  return response.json();
}

export interface HealthData {
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

export interface ProcessData {
  pid: number;
  name: string;
  cpu_percent: number;
  memory_percent: number;
}

export interface PerformanceData {
  sort_by: string;
  limit: number;
  processes: ProcessData[];
}

export const api = {
  health: () =>
    request<HealthData>("/api/health/"),

  performance: (
    sortBy: "cpu" | "memory" = "cpu",
    limit = 10
  ) =>
    request<PerformanceData>(
      `/api/performance?sort_by=${sortBy}&limit=${limit}`
    ),

  organizeFiles: (folderPath: string) =>
    request("/api/file-organizer", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        folder_path: folderPath,
      }),
    }),

  analyzeLog: (file: File) => {
    const formData = new FormData();

    formData.append("file", file);

    return request("/api/log-analyzer", {
      method: "POST",
      body: formData,
    });
  },

  validateCsv: (file: File) => {
    const formData = new FormData();

    formData.append("file", file);

    return request("/api/csv-validator", {
      method: "POST",
      body: formData,
    });
  },

  generateReport: (
    format: "json" | "csv" | "html" | "text"
  ) =>
    request(
      `/api/reports/health?output_format=${format}`,
      {
        method: "POST",
      }
    ),

  publicIp: () =>
    request("/api/public-ip"),

  github: () =>
    request(
      "/api/github?owner=NtandoBadla&repo=python-utilities-pack"
    ),

  fullScan: () =>
    request("/api/full-scan"),
};

export function getDownloadUrl(path?: string): string {
  if (!path) return "";

  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  return `http://127.0.0.1:8000${normalizedPath}`;
}