import type { Reading } from "../types";

interface Props {
  anomalies: Reading[];
}

const severityColors: Record<string, string> = {
  high: "#ef4444",
  medium: "#f59e0b",
  low: "#eab308",
};

export function AnomalyTable({ anomalies }: Props) {
  return (
    <div
      style={{
        background: "#1e293b",
        borderRadius: "12px",
        padding: "20px",
        border: "1px solid #334155",
      }}
    >
      <h3 style={{ color: "#f1f5f9", marginTop: 0 }}>
        Recent Anomalies ({anomalies.length})
      </h3>
      <div style={{ maxHeight: "300px", overflowY: "auto" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            color: "#cbd5e1",
            fontSize: "13px",
          }}
        >
          <thead>
            <tr style={{ textAlign: "left", color: "#94a3b8" }}>
              <th style={{ padding: "8px" }}>Time</th>
              <th style={{ padding: "8px" }}>Device</th>
              <th style={{ padding: "8px" }}>Temp</th>
              <th style={{ padding: "8px" }}>Vibration</th>
              <th style={{ padding: "8px" }}>Pressure</th>
              <th style={{ padding: "8px" }}>Score</th>
              <th style={{ padding: "8px" }}>Severity</th>
            </tr>
          </thead>
          <tbody>
            {anomalies.map((a, i) => (
              <tr key={i} style={{ borderTop: "1px solid #334155" }}>
                <td style={{ padding: "8px" }}>
                  {new Date(a.timestamp * 1000).toLocaleTimeString()}
                </td>
                <td style={{ padding: "8px" }}>{a.device_id}</td>
                <td style={{ padding: "8px" }}>{a.temperature}</td>
                <td style={{ padding: "8px" }}>{a.vibration}</td>
                <td style={{ padding: "8px" }}>{a.pressure}</td>
                <td style={{ padding: "8px" }}>{a.anomaly_score}</td>
                <td style={{ padding: "8px" }}>
                  <span
                    style={{
                      background: severityColors[a.severity],
                      color: "#0f172a",
                      padding: "2px 10px",
                      borderRadius: "12px",
                      fontWeight: 600,
                      fontSize: "11px",
                    }}
                  >
                    {a.severity.toUpperCase()}
                  </span>
                </td>
              </tr>
            ))}
            {anomalies.length === 0 && (
              <tr>
                <td
                  colSpan={7}
                  style={{ padding: "20px", textAlign: "center", color: "#64748b" }}
                >
                  No anomalies detected yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}