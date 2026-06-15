import type { Stats } from "../types";

interface Props {
  stats: Stats;
  connected: boolean;
}

export function StatsCards({ stats, connected }: Props) {
  const rate =
    stats.processed > 0
      ? ((stats.anomalies / stats.processed) * 100).toFixed(2)
      : "0.00";

  const cards = [
    { label: "Status", value: connected ? "🟢 Live" : "🔴 Offline" },
    { label: "Processed", value: stats.processed.toLocaleString() },
    { label: "Anomalies", value: stats.anomalies.toLocaleString() },
    { label: "Anomaly Rate", value: `${rate}%` },
  ];

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(4, 1fr)",
        gap: "16px",
        marginBottom: "24px",
      }}
    >
      {cards.map((c) => (
        <div
          key={c.label}
          style={{
            background: "#1e293b",
            borderRadius: "12px",
            padding: "20px",
            textAlign: "center",
            border: "1px solid #334155",
          }}
        >
          <div style={{ color: "#94a3b8", fontSize: "13px" }}>{c.label}</div>
          <div
            style={{
              color: "#f1f5f9",
              fontSize: "28px",
              fontWeight: 700,
              marginTop: "8px",
            }}
          >
            {c.value}
          </div>
        </div>
      ))}
    </div>
  );
}