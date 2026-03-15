"use client";

import { motion } from "framer-motion";

export function EntityCard({
  title,
  subtitle,
  tags
}: {
  title: string;
  subtitle: string;
  tags?: string[];
}) {
  return (
    <motion.div 
      className="card"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02, backgroundColor: "rgba(255, 255, 255, 0.05)" }}
      transition={{ duration: 0.2 }}
    >
      <h3>{title}</h3>
      <p className="muted">{subtitle}</p>
      <div className="flex flex-wrap gap-2" style={{ marginTop: 12 }}>
        {tags?.map((tag) => (
          <span className="tag" key={tag}>{tag}</span>
        ))}
      </div>
    </motion.div>
  );
}
