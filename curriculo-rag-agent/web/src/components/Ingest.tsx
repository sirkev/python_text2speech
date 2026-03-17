"use client";

import { useState } from 'react';
import { BrainCircuit, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

const API_BASE = "http://localhost:8010/api/v1";

export default function Ingest() {
  const [text, setText] = useState('');
  const [source, setSource] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<{ type: 'success' | 'error', message: string } | null>(null);

  const handleIngest = async () => {
    if (!text.trim() || !source.trim() || loading) return;

    setLoading(true);
    setStatus(null);

    try {
      const response = await axios.post(`${API_BASE}/ingest`, {
        text,
        source
      });

      setStatus({ 
        type: 'success', 
        message: `Success! Created ${response.data.chunks_created} knowledge chunks.` 
      });
      setText('');
      setSource('');
    } catch (error: any) {
      console.error("Ingest error:", error);
      setStatus({ 
        type: 'error', 
        message: error.response?.data?.detail || "Failed to ingest content. Check agent logs." 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full glass rounded-3xl p-8 space-y-6 animate-fade-in shadow-2xl">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-primary/20 rounded-2xl">
          <BrainCircuit className="text-primary" size={28} />
        </div>
        <div>
          <h2 className="font-bold text-xl">AI Knowledge Training</h2>
          <p className="text-sm text-secondary">Enhance the Care AI with new materials</p>
        </div>
      </div>

      <div className="space-y-4 flex-1 flex flex-col">
        <div className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-wider text-secondary">Material Source</label>
          <input
            type="text"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="e.g. Care Quality Commission Guidelines"
            className="w-full bg-card-bg border border-glass-border rounded-xl py-3 px-4 focus:outline-none focus:border-primary/50 transition-colors"
          />
        </div>

        <div className="space-y-2 flex-1 flex flex-col">
          <label className="text-xs font-semibold uppercase tracking-wider text-secondary">Document Content</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste compliance documents or training text here..."
            className="w-full flex-1 bg-card-bg border border-glass-border rounded-xl py-3 px-4 focus:outline-none focus:border-primary/50 transition-colors resize-none custom-scrollbar"
          />
        </div>

        {status && (
          <div className={`p-4 rounded-xl flex items-center gap-3 text-sm ${
            status.type === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
          }`}>
            {status.type === 'success' ? <CheckCircle size={18} /> : <AlertCircle size={18} />}
            {status.message}
          </div>
        )}

        <button
          onClick={handleIngest}
          disabled={!text.trim() || !source.trim() || loading}
          className="w-full py-4 bg-primary hover:bg-primary/80 text-white font-bold rounded-2xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-primary/20"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              Processing Knowledge...
            </>
          ) : (
            <>
              <BrainCircuit size={20} />
              Update AI Knowledge
            </>
          )}
        </button>
      </div>
    </div>
  );
}
