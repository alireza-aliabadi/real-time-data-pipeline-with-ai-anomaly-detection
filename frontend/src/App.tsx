import { useCallback, useState } from "react";
import { useWebSocket } from "./hooks/useWebSocket";
import { StatsCards } from "./components/StatsCard";
import { MetricsChart } from "./components/MetricsChart";
import { AnomalyTable } from "./components/AnomalyTable";
import type { Reading, Stats, WSMessage } from "./types";

const MAX_CHART_POINTS = 60;
const MAX_ANOMALIES = 50;

export default function App() {
  const [readings, setReadings] = useState<Reading[]>([]);
  const [anomalies, setAnomalies] = useState<Reading[]>([]);
  const [stats, setStats] = useState<Stats>({ processed: 0, anomalies: 0 });

  const handleMessage = useCallback((msg: WSMessage) => {
    if (msg.type !== "reading") return;
    const r = msg.data;

    setStats(msg.stats);

    setReadings((prev) => {
      const next = [...prev, r];
      return next.length > MAX_CHART_POINTS
        ? next.slice(next.length - MAX_CHART_POINTS)
        : next;
    });

    if (r.is_anomaly) {
      setAnomalies((prev) => [r, ...prev].slice(0, MAX_ANOMALIES));
    }
  }, []);

  const { connected } = useWebSocket(handleMessage);

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        padding: "32px",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}
    >
      <h1 style={{ color: "#f1f5f9", marginBottom: "24px" }}>
        🔍 Real-time Anomaly Detection Pipeline
      </h1>
      <StatsCards stats={stats} connected={connected} />
      <MetricsChart data={readings} />
      <AnomalyTable anomalies={anomalies} />
    </div>
  );
}