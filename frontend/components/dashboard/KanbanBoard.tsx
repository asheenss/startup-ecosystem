"use client";

import { motion } from "framer-motion";

type KanbanItem = { id: number; startup_name: string; stage: string };

export function KanbanBoard({
  pipeline
}: {
  pipeline: Record<"interested" | "reviewing" | "meeting" | "invested", KanbanItem[]>;
}) {
  const labels = {
    interested: "Interested",
    reviewing: "Reviewing",
    meeting: "Meeting",
    invested: "Invested"
  } as const;

  return (
    <div className="kanban">
      {Object.entries(labels).map(([key, label], colIndex) => (
        <motion.div 
          className="kanban-column" 
          key={key}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: colIndex * 0.1, duration: 0.3 }}
        >
          <strong>{label}</strong>
          <div className="list" style={{ marginTop: 12 }}>
            {pipeline[key as keyof typeof pipeline].map((item, itemIndex) => (
              <motion.div 
                className="card" 
                key={item.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: (colIndex * 0.1) + (itemIndex * 0.05) }}
                whileHover={{ scale: 1.02, backgroundColor: "rgba(255, 255, 255, 0.06)" }}
                style={{ cursor: "pointer" }}
              >
                <div>{item.startup_name}</div>
                <div className="muted">{item.stage}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      ))}
    </div>
  );
}
