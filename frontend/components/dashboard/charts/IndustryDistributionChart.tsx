"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";

export function IndustryDistributionChart({ data }: { data: Record<string, number> }) {
  const chartData = Object.entries(data)
    .map(([industry, count]) => ({ industry, count }))
    .sort((a, b) => b.count - a.count);

  // A sleek gradient color scale from primary to a lighter hue
  const colors = ["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe"];

  return (
    <div style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
          <XAxis 
            dataKey="industry" 
            tick={{ fill: "#64748b", fontSize: 12 }} 
            axisLine={false} 
            tickLine={false} 
          />
          <YAxis 
            tick={{ fill: "#64748b", fontSize: 12 }} 
            axisLine={false} 
            tickLine={false} 
            allowDecimals={false}
          />
          <Tooltip 
            cursor={{ fill: "rgba(255,255,255,0.02)" }}
            contentStyle={{ 
              backgroundColor: "#0f172a", 
              border: "1px solid #1e293b",
              borderRadius: "8px",
              boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.5)"
            }}
            itemStyle={{ color: "#e2e8f0" }}
          />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
