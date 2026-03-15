'use client';

import { useQuery } from '@tanstack/react-query';
import { DashboardShell } from './DashboardShell';
import { MetricCard } from './MetricCard';
import { IndustryDistributionChart } from './charts/IndustryDistributionChart';
import { FundingStageChart } from './charts/FundingStageChart';
import { Users, Rocket, Calendar, Brain, Share2, ClipboardList } from "lucide-react";
import { fetchJson } from '../../lib/api';

interface AdminData {
  metrics: {
    total_startups: number;
    total_investors: number;
    events_hosted: number;
    evaluations_generated: number;
    connections_requested: number;
    event_registrations: number;
  };
  industry_distribution: Record<string, number>;
  stage_distribution: Record<string, number>;
}

export function AdminDashboardContent({ initialData }: { initialData: AdminData }) {
  const { data } = useQuery({
    queryKey: ['dashboard', 'admin'],
    queryFn: () => fetchJson('/dashboard/admin', initialData),
    initialData
  });

  return (
    <DashboardShell
      title="Admin dashboard"
      subtitle="Overview of the startup ecosystem, platform metrics, and active member participation."
    >
      <div className="stats-grid">
        <MetricCard label="Total Startups" value={data.metrics.total_startups} icon={<Rocket className="w-5 h-5" />} />
        <MetricCard label="Total Investors" value={data.metrics.total_investors} icon={<Users className="w-5 h-5" />} />
        <MetricCard label="Events Hosted" value={data.metrics.events_hosted} icon={<Calendar className="w-5 h-5" />} />
        <MetricCard label="AI Evaluations" value={data.metrics.evaluations_generated} icon={<Brain className="w-5 h-5" />} />
        <MetricCard label="Connections" value={data.metrics.connections_requested} icon={<Share2 className="w-5 h-5" />} />
        <MetricCard label="Event Regs" value={data.metrics.event_registrations} icon={<ClipboardList className="w-5 h-5" />} />
      </div>

      <div className="grid-2">
        <section className="panel min-h-[450px]">
          <h2 className="text-xl font-bold mb-6">Industry Distribution</h2>
          <div style={{ height: 320, minHeight: 320 }}>
            <IndustryDistributionChart data={data.industry_distribution} />
          </div>
        </section>

        <section className="panel min-h-[450px]">
          <h2 className="text-xl font-bold mb-6">Funding Stage Distribution</h2>
          <div style={{ height: 320, minHeight: 320 }}>
            <FundingStageChart data={data.stage_distribution} />
          </div>
        </section>
      </div>
    </DashboardShell>
  );
}
