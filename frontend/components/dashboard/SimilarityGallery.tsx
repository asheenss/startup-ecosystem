"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchJson } from "@/lib/api";
import { StatCard } from "./StatCard";
import { Rocket, Target, ArrowRight } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";

interface SimilarStartup {
  id: number;
  startup_name: string;
  industry: string;
  stage: string;
  match_score: number;
}

export function SimilarityGallery({ startupId }: { startupId: number }) {
  const { data: similar, isLoading } = useQuery<SimilarStartup[]>({
    queryKey: ["startups", startupId, "similar"],
    queryFn: () => fetchJson(`/api/startups/${startupId}/similar`, []),
    enabled: !!startupId,
  });

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 animate-pulse">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-32 rounded-3xl bg-white/5 border border-white/5" />
        ))}
      </div>
    );
  }

  if (!similar || similar.length === 0) {
    return (
      <div className="p-8 border-2 border-dashed border-white/5 rounded-3xl text-center text-muted text-sm">
        No similar startups found yet. <br/> AI needs more embeddings to find matches.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {similar.map((item, index) => (
        <motion.div
          key={item.id}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.1 }}
          className="glass-panel p-5 group cursor-pointer hover:border-primary/50"
        >
          <div className="flex justify-between items-start mb-4">
            <div className="bg-primary/10 p-2 rounded-xl group-hover:bg-primary group-hover:text-canvas transition-colors">
              <Rocket size={18} />
            </div>
            <span className="text-xs font-mono font-bold text-primary px-2 py-1 bg-primary/10 rounded-lg">
              {item.match_score}% Match
            </span>
          </div>
          
          <h4 className="font-bold text-lg mb-1">{item.startup_name}</h4>
          <p className="text-xs text-muted mb-4">{item.industry} • {item.stage}</p>
          
          <Link 
            href={`/dashboard/startups/${item.id}`}
            className="flex items-center gap-2 text-xs font-bold text-primary group-hover:translate-x-1 transition-transform"
          >
            View Profile <ArrowRight size={14} />
          </Link>
        </motion.div>
      ))}
    </div>
  );
}
