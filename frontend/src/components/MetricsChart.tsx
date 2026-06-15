import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Scatter,
  ComposedChart,
} from "recharts";
import type { Reading } from "../types";

interface Props {
  data: Reading[];
}

export function MetricsChart({ data }: Props) {
  // map for chart: x = index, plus anomaly markers
  const chartData = data.map((d, i) => ({
    idx: i,
    temperature: d.temperature,
    vibration: d.vibration * 50, // scale up for visibility
    pressure: d.pressure,
    anomaly: d.is_anomaly ? d.temperature : null,
  }));

  return (
    <div
      style={{
        background: "#1e293b",
        borderRadius: "12px",
        padding: "20px",
        border: "1px solid #334155",
        marginBottom: "24px",
      }}
    >
      <h3 style={{ color: "#f1f5f9", marginTop: 0 }}>
        Real-time Sensor Metrics
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="idx" stroke="#94a3b8" tick={{ fontSize: 11 }} />
          <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
          <Tooltip
            contentStyle={{
              background: "#0f172a",
              border: "1px solid #334155",
              borderRadius: "8px",
              color: "#f1f5f9",
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="temperature"
            stroke="#38bdf8"
            dot={false}
            strokeWidth={2}
            name="Temperature"
            isAnimationActive={false}
          />
          <Line
            type="monotone"
            dataKey="pressure"
            stroke="#a78bfa"
            dot={false}
            strokeWidth={2}
            name="Pressure"
            isAnimationActive={false}
          />
          <Line
            type="monotone"
            dataKey="vibration"
            stroke="#34d399"
            dot={false}
            strokeWidth={1.5}
            name="Vibration (x50)"
            isAnimationActive={false}
          />
          <Scatter
            dataKey="anomaly"
            fill="#ef4444"
            name="Anomaly"
            isAnimationActive={false}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}