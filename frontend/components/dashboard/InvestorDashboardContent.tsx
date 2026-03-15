'use client';

import { useQuery } from '@tanstack/react-query';
import { DashboardShell } from './DashboardShell';
import { MetricCard } from './MetricCard';
import { EntityCard } from './EntityCard';
import { KanbanBoard } from './KanbanBoard';
import { Search, PlusCircle, TrendingUp, Filter } from "lucide-react";
import { fetchJson } from '../../lib/api';

interface InvestorData {
  metrics: {
    total_startups_discovered: number;
    new_startups_this_week: number;
    top_rated_startups: number;
    startups_seeking_funding: number;
  };
  recommended_startups: any[];
  pipeline: any;
}

export function InvestorDashboardContent({ initialData }: { initialData: InvestorData }) {
  const { data } = useQuery({
    queryKey: ['dashboard', 'investor'],
    queryFn: () => fetchJson('/dashboard/investor', initialData),
    initialData
  });

  return (
    <DashboardShell
      title="Investor dashboard"
      subtitle="Discover high-potential startups, manage your investment pipeline, and track deal flow."
    >
      <div className="stats-grid">
        <MetricCard label="Discovered" value={data.metrics.total_startups_discovered} icon={<Search className="w-5 h-5" />} />
        <MetricCard label="New This Week" value={data.metrics.new_startups_this_week} icon={<PlusCircle className="w-5 h-5" />} />
        <MetricCard label="Top Rated" value={data.metrics.top_rated_startups} icon={<TrendingUp className="w-5 h-5" />} />
        <MetricCard label="Seeking Funding" value={data.metrics.startups_seeking_funding} icon={<Filter className="w-5 h-5" />} />
      </div>

      <div className="grid-2">
        <section className="panel">
          <h2 className="text-xl font-bold mb-6">Recommended Startups</h2>
          <div className="space-y-4">
            {data.recommended_startups.map((startup: any) => (
              <EntityCard
                key={startup.id}
                title={startup.startup_name}
                subtitle={`${startup.industry} | ${startup.stage}`}
                tags={[`$${startup.funding_needed.toLocaleString()} needed`]}
              />
            ))}
          </div>
        </section>

        <section className="panel">
          <h2 className="text-xl font-bold mb-6">Investment Pipeline</h2>
          <KanbanBoard pipeline={data.pipeline} />
        </section>
      </div>
    </DashboardShell>
  );
}
