'use client';

import { useQuery } from '@tanstack/react-query';
import { DashboardShell } from './DashboardShell';
import { StatCard } from './StatCard';
import { EntityCard } from './EntityCard';
import { AIEvaluationRadar } from './charts/AIEvaluationRadar';
import { Rocket, Briefcase, CircleDollarSign, Brain, Target, Calendar } from "lucide-react";
import { fetchJson } from '../../lib/api';
import { AnalyzerUI } from '../ai/AnalyzerUI';
import { SimilarityGallery } from './SimilarityGallery';

interface FounderData {
  startup_overview: {
    id: number;
    startup_name: string;
    industry: string;
    stage: string;
    funding_needed: number;
  };
  latest_analysis: any;
  investor_matches: any[];
  event_recommendations: any[];
}

export function FounderDashboardContent({ initialData, userId }: { initialData: FounderData, userId: string }) {
  const { data } = useQuery({
    queryKey: ['dashboard', 'founder', userId],
    queryFn: () => fetchJson(`/dashboard/founder/${userId}`, initialData),
    initialData,
    refetchInterval: (query: any) => {
      const status = query.state.data?.latest_analysis?.status;
      return status === 'pending' ? 5000 : false;
    }
  });

  const analysis = data?.latest_analysis;

  return (
    <DashboardShell
      title={`Welcome back, ${data.startup_overview?.startup_name ?? "Founder"}`}
      subtitle="Your AI-powered ecosystem status and investment readiness scorecard."
    >
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <StatCard 
          label="Industry Focus" 
          value={data.startup_overview?.industry ?? "N/A"} 
          icon={Target} 
        />
        <StatCard 
          label="Current Stage" 
          value={data.startup_overview?.stage ?? "Seed"} 
          icon={Rocket} 
        />
        <StatCard 
          label="Funding Goal" 
          value={`$${(data.startup_overview?.funding_needed / 1000).toFixed(0)}k`} 
          icon={CircleDollarSign} 
        />
        <StatCard 
          label="AI Readiness" 
          value={analysis?.score ?? "--"} 
          icon={Brain}
          trend={{ value: 12, isUp: true }}
          description="Based on latest deck"
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        <div className="xl:col-span-2 space-y-8">
          <AnalyzerUI />
          
          <section className="glass-panel p-8">
            <h2 className="text-xl font-bold mb-4">AI Evaluation Insights</h2>
            <div className="grid md:grid-cols-2 gap-8">
              {analysis && analysis.status === 'completed' ? (
                <AIEvaluationRadar data={analysis} />
              ) : (
                <div className="flex items-center justify-center p-12 bg-white/5 rounded-3xl text-muted text-sm text-center">
                  Upload your pitch deck to generate <br/> a 360° AI evaluation.
                </div>
              )}
              
              <div className="space-y-4">
                <h3 className="text-sm font-semibold uppercase tracking-wider text-primary">Strategic Suggestions</h3>
                <div className="space-y-3">
                  {(analysis?.improvement_suggestions?.split("\n") ?? ["No suggestions yet."]).slice(0, 5).map((item: string, i: number) => (
                    <div key={i} className="flex gap-3 text-sm p-3 bg-white/5 rounded-xl border border-white/5">
                      <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 shrink-0" />
                      <p>{item}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
          <section className="glass-panel p-8">
            <h2 className="text-xl font-bold mb-4">Competitor & Lookalike Discovery</h2>
            <p className="text-sm text-muted mb-6">AI models searching for startups with overlapping technologies and business goals.</p>
            <SimilarityGallery startupId={data.startup_overview.id} />
          </section>
        </div>

        <div className="space-y-8 text-white">
          <section className="glass-panel p-8">
            <h2 className="text-xl font-bold mb-6">Top Investor Matches</h2>
            <div className="space-y-4">
              {data.investor_matches?.slice(0, 3).map((investor: any) => (
                <div key={investor.investor_name} className="p-4 bg-white/5 rounded-2xl border border-white/5 hover:border-primary/30 transition-colors">
                  <div className="flex justify-between items-center mb-1">
                    <h4 className="font-bold">{investor.investor_name}</h4>
                    <span className="text-primary font-mono text-xs">{investor.match_score}% Match</span>
                  </div>
                  <p className="text-xs text-muted mb-3">Focus: {investor.preferred_industries}</p>
                  <button className="w-full py-2 bg-primary/10 text-primary text-xs font-bold rounded-lg hover:bg-primary hover:text-canvas transition-colors">
                    Request Connection
                  </button>
                </div>
              ))}
            </div>
          </section>

          <section className="glass-panel p-8">
            <h2 className="text-xl font-bold mb-6">Recommended Events</h2>
            <div className="space-y-4">
              {data.event_recommendations?.slice(0, 2).map((event: any) => (
                <div key={event.id} className="flex gap-4">
                  <div className="bg-primary/20 p-3 rounded-2xl flex flex-col items-center justify-center min-w-[60px] h-[60px]">
                    <span className="text-xs uppercase font-bold text-primary">Mar</span>
                    <span className="text-lg font-black text-white">24</span>
                  </div>
                  <div>
                    <h4 className="font-bold text-sm leading-tight mb-1">{event.title}</h4>
                    <p className="text-xs text-muted flex items-center gap-1">
                      <Calendar size={12} /> {event.location}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </DashboardShell>
  );
}
