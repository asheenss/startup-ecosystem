"use client";

import { useState } from "react";
import { FileUp, Loader2, CheckCircle2, AlertCircle, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function AnalyzerUI() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "analyzing" | "completed" | "error">("idle");
  const [progress, setProgress] = useState(0);

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    
    // Simulating progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setStatus("analyzing");
          return 100;
        }
        return prev + 10;
      });
    }, 200);

    // Actual upload logic would go here
  };

  return (
    <div className="glass-panel p-8 max-w-2xl mx-auto w-full">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-primary/20 rounded-lg">
          <Sparkles className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h2 className="text-xl font-bold">AI Pitch Deck Analyzer</h2>
          <p className="text-sm text-muted">Upload your deck for instant AI-powered scoring & insights</p>
        </div>
      </div>

      <AnimatePresence mode="wait">
        {status === "idle" && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="border-2 border-dashed border-white/10 rounded-3xl p-12 text-center hover:border-primary/50 transition-colors cursor-pointer"
            onClick={() => document.getElementById("file-upload")?.click()}
          >
            <input 
              id="file-upload" 
              type="file" 
              className="hidden" 
              accept=".pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            <div className="bg-primary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <FileUp className="w-8 h-8 text-primary" />
            </div>
            <h3 className="font-semibold mb-1">
              {file ? file.name : "Click to upload pitch deck"}
            </h3>
            <p className="text-xs text-muted">PDF files only (Max 10MB)</p>
            {file && (
              <button 
                onClick={(e) => { e.stopPropagation(); handleUpload(); }}
                className="btn-primary mt-6 w-full"
              >
                Analyze Deck
              </button>
            )}
          </motion.div>
        )}

        {(status === "uploading" || status === "analyzing") && (
          <motion.div 
            key="processing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-12 text-center"
          >
            <div className="relative w-20 h-20 mx-auto mb-6">
              <Loader2 className="w-20 h-20 text-primary animate-spin" />
              <div className="absolute inset-0 flex items-center justify-center text-xs font-bold">
                {status === "uploading" ? `${progress}%` : "AI..."}
              </div>
            </div>
            <h3 className="text-lg font-semibold mb-2">
              {status === "uploading" ? "Uploading Document..." : "Agents Collaborating..."}
            </h3>
            <p className="text-sm text-muted max-w-xs mx-auto">
              Our Multi-Agent system is extracting text, scoring metrics, and matching investors.
            </p>
          </motion.div>
        )}

        {status === "completed" && (
          <motion.div 
            key="done"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-8 text-center"
          >
            <div className="bg-green-500/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle2 className="w-8 h-8 text-green-500" />
            </div>
            <h3 className="text-xl font-bold mb-2">Analysis Complete!</h3>
            <p className="text-sm text-muted mb-6">Your dashboard insights have been updated.</p>
            <button 
              onClick={() => setStatus("idle")}
              className="px-6 py-2 border border-white/10 rounded-xl hover:bg-white/5"
            >
              Analyze Another
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
