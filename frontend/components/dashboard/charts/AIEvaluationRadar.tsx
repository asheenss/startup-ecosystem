"use client";

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from "recharts";

interface AIEvaluationRadarProps {
  data: {
    problem_clarity: number;
    market_size: number;
    traction: number;
    team_strength: number;
    financial_potential: number;
  };
}

export function AIEvaluationRadar({ data }: AIEvaluationRadarProps) {
  // Transform standard 1-10 scores into radar points
  const chartData = [
    { subject: "Problem", A: data.problem_clarity, fullMark: 10 },
    { subject: "Market", A: data.market_size, fullMark: 10 },
    { subject: "Traction", A: data.traction, fullMark: 10 },
    { subject: "Team", A: data.team_strength, fullMark: 10 },
    { subject: "Financials", A: data.financial_potential, fullMark: 10 },
  ];

  return (
    <div style={{ width: "100%", height: 350 }}>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={chartData}>
          <PolarGrid stroke="rgba(255,255,255,0.1)" />
          <PolarAngleAxis 
            dataKey="subject" 
            tick={{ fill: "#94a3b8", fontSize: 12, fontWeight: 500 }} 
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 10]} 
            tick={{ fill: "#475569", fontSize: 10 }}
            axisLine={false}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: "#0f172a", 
              border: "1px solid #1e293b",
              borderRadius: "8px",
              color: "#f8fafc",
            }}
            itemStyle={{ color: "#38bdf8" }}
          />
          <Radar
            name="AI Score"
            dataKey="A"
            stroke="#38bdf8"
            fill="#38bdf8"
            fillOpacity={0.4}
            dot={{ r: 3, fill: "#0ea5e9" }}
            activeDot={{ r: 5, fill: "#bae6fd" }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
