"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

export function FundingStageChart({ data }: { data: Record<string, number> }) {
  const chartData = Object.entries(data)
    .map(([stage, count]) => ({ name: stage, value: count }))
    .sort((a, b) => b.value - a.value);

  // Modern vibrant palette for pie slices
  const COLORS = ["#8b5cf6", "#6366f1", "#ec4899", "#f43f5e", "#f59e0b"];

  return (
    <div style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer>
        <PieChart margin={{ top: 0, right: 0, bottom: 0, left: 0 }}>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={2}
            dataKey="value"
            stroke="none"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{ 
              backgroundColor: "#0f172a", 
              border: "1px solid #1e293b",
              borderRadius: "8px",
              color: "#f8fafc",
              boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.5)"
            }}
            itemStyle={{ color: "#f8fafc" }}
          />
          <Legend 
            verticalAlign="bottom" 
            height={36} 
            iconType="circle"
            wrapperStyle={{ fontSize: "12px", color: "#94a3b8" }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
