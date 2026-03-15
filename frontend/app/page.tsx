import Link from "next/link";
import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { Rocket, Users, Calendar, Activity, Zap, TrendingUp } from "lucide-react";

export default function HomePage() {
  return (
    <DashboardShell
      title="Ecosystem Intelligence"
      subtitle="The ultimate hub for founders, investors, and platform administrators. Powered by real-time AI analysis."
    >
      {/* Featured Metric Row */}
      <div className="stats-grid">
        <MetricCard 
          label="Total Volume" 
          value="$14.2M" 
          icon={<TrendingUp className="text-primary" />} 
        />
        <MetricCard 
          label="AI throughput" 
          value="1,240/hr" 
          icon={<Zap className="text-primary" />} 
        />
        <MetricCard 
          label="Active Founders" 
          value="842" 
          icon={<Rocket className="text-primary" />} 
        />
        <MetricCard 
          label="Top Matches" 
          value="53" 
          icon={<Activity className="text-primary" />} 
        />
      </div>

      <div className="grid-3 mt-10">
        <Link href="/dashboard/founder?user=1" className="glass-panel-hover p-8 group">
          <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Rocket className="text-primary w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold mb-3">Founders</h2>
          <p className="text-muted leading-relaxed">
            Analyze your pitch deck, track performance, and discover matching investors using our vector-search matching engine.
          </p>
          <div className="mt-6 flex items-center text-primary text-sm font-bold gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            Launch Dashboard →
          </div>
        </Link>

        <Link href="/dashboard/investor?user=2" className="glass-panel-hover p-8 group">
          <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Users className="text-primary w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold mb-3">Investors</h2>
          <p className="text-muted leading-relaxed">
            Monitor deal flow, discover similar startups via pgvector, and move opportunities through a sleek investment pipeline.
          </p>
          <div className="mt-6 flex items-center text-primary text-sm font-bold gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            Review Pipeline →
          </div>
        </Link>
        
        <Link href="/dashboard/admin" className="glass-panel-hover p-8 group">
          <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <Activity className="text-primary w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold mb-3">Administrators</h2>
          <p className="text-muted leading-relaxed">
            Gain platform-wide visibility into adoption metrics, event activity, and AI-driven success predictions.
          </p>
          <div className="mt-6 flex items-center text-primary text-sm font-bold gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            Admin Console →
          </div>
        </Link>
      </div>

      <div className="mt-12 glass-panel p-10 flex flex-col lg:flex-row items-center justify-between gap-8">
        <div className="space-y-4">
          <h3 className="text-3xl font-black">Ready to scale your ecosystem?</h3>
          <p className="text-muted text-lg">Integrated networking, semantic search, and AI evaluations in one unified shell.</p>
        </div>
        <div className="flex gap-4">
          <Link href="/dashboard/events" className="btn-primary">Explore Events</Link>
          <Link href="/dashboard/startups" className="px-6 py-2.5 rounded-xl border border-white/10 hover:bg-white/5 transition-all">Browse Startups</Link>
        </div>
      </div>
    </DashboardShell>
  );
}
