import { LucideIcon } from "lucide-react";
import { motion } from "framer-motion";

interface StatCardProps {
  label: string;
  value: string | number;
  trend?: {
    value: number;
    isUp: boolean;
  };
  icon: LucideIcon;
  description?: string;
}

export function StatCard({ label, value, trend, icon: Icon, description }: StatCardProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="stat-card glass-panel-hover"
    >
      <div className="flex justify-between items-start mb-4">
        <div className="p-2.5 bg-primary/10 rounded-xl">
          <Icon className="w-5 h-5 text-primary" />
        </div>
        {trend && (
          <span className={`text-xs font-bold px-2 py-1 rounded-lg ${
            trend.isUp ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500"
          }`}>
            {trend.isUp ? "+" : "-"}{Math.abs(trend.value)}%
          </span>
        )}
      </div>
      
      <div>
        <p className="text-sm text-muted font-medium mb-1">{label}</p>
        <h3 className="text-2xl font-bold tracking-tight">{value}</h3>
        {description && <p className="text-xs text-muted mt-2">{description}</p>}
      </div>
    </motion.div>
  );
}
