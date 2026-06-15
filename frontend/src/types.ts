export interface Reading {
  device_id: string;
  timestamp: number;
  temperature: number;
  vibration: number;
  pressure: number;
  is_anomaly: boolean;
  anomaly_score: number;
  rolling_anomaly_rate: number;
  severity: "low" | "medium" | "high";
  _injected_anomaly?: number;
}

export interface Stats {
  processed: number;
  anomalies: number;
}

export interface WSMessage {
  type: "reading";
  data: Reading;
  stats: Stats;
}