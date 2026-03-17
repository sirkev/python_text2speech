"use client";

import { useState, useEffect, useRef } from 'react';
import { Send, ShieldCheck, User, Loader2 } from 'lucide-react';
import axios from 'axios';

const API_BASE = "http://localhost:8010/api/v1";

export default function Chat() {
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant', content: string }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/chat`, {
        message: userMsg,
        history: messages.map(m => ({ role: m.role, content: m.content }))
      });

      setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error connecting to the brain." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full glass rounded-3xl overflow-hidden animate-fade-in">
      {/* Header */}
      <div className="p-6 border-b border-glass-border flex items-center gap-3">
        <div className="p-2 bg-primary/20 rounded-xl">
          <ShieldCheck className="text-primary" size={24} />
        </div>
        <div>
          <h2 className="font-bold text-lg">Care AI Assistant</h2>
          <p className="text-xs text-secondary">Operational Support & RAG Retrieval</p>
        </div>
      </div>

      {/* Messages */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar"
      >
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center space-y-8 animate-fade-in">
            <div className="space-y-4 opacity-50 flex flex-col items-center">
              <ShieldCheck size={48} />
              <p className="max-w-[240px]">I can help with Rota, Compliance, or Training documents.</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-md">
              {[
                "Who is on shift today?",
                "Report medication discrepancy",
                "London branch compliance status",
                "Calculate training hours needed"
              ].map((query, i) => (
                <button
                  key={i}
                  onClick={() => {
                    setInput(query);
                    // Trigger send handled by the button click logic
                  }}
                  className="text-left p-4 rounded-xl border border-white/10 hover:border-primary/50 hover:bg-primary/5 transition-all text-xs font-medium"
                >
                  {query}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((msg, i) => (
          <div 
            key={i} 
            className={`flex items-start gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div className={`p-2 rounded-lg ${msg.role === 'user' ? 'bg-accent/20' : 'bg-primary/20'}`}>
              {msg.role === 'user' ? <User size={16} /> : <ShieldCheck size={16} />}
            </div>
            <div className={`max-w-[80%] p-4 rounded-2xl ${
              msg.role === 'user' 
                ? 'bg-accent/10 rounded-tr-none' 
                : 'bg-card-bg rounded-tl-none border border-glass-border'
            }`}>
              <p className="text-sm leading-relaxed">{msg.content}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 opacity-50 italic text-sm">
            <Loader2 className="animate-spin" size={16} />
            Brain is thinking...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-6 border-t border-glass-border">
        <div className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your question..."
            className="w-full bg-card-bg border border-glass-border rounded-2xl py-4 pl-6 pr-14 focus:outline-none focus:border-primary/50 transition-colors"
          />
          <button 
            onClick={handleSend}
            disabled={!input.trim() || loading}
            aria-label="Send message"
            title="Send message"
            className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-primary hover:bg-primary/80 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
