"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";

export function MetricCard({ label, value, hint, icon }: { label: string; value: string | number; hint?: string; icon?: ReactNode }) {
  return (
    <motion.div 
      className="panel hover:border-primary/30 transition-all duration-300"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ y: -4, boxShadow: "0 10px 40px -10px rgba(98, 212, 255, 0.2)" }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="text-muted text-xs font-bold uppercase tracking-wider">{label}</div>
        {icon && <div className="p-2 rounded-lg bg-white/5 text-primary">{icon}</div>}
      </div>
      <div className="text-4xl font-black tracking-tight text-white mb-1">{value}</div>
      {hint && <div className="text-xs text-primary/70 font-medium">{hint}</div>}
    </motion.div>
  );
}
