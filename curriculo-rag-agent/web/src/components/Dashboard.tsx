"use client";

import { useEffect, useState } from 'react';
import { 
  Users, 
  Building2, 
  ShieldAlert, 
  ArrowRight, 
  Calendar, 
  ClipboardCheck,
  LayoutDashboard
} from 'lucide-react';
import axios from 'axios';

const API_BASE = "http://localhost:8010/api/v1";

interface Stats {
  companies: number;
  branches: number;
  employees: number;
  clients: number;
  active_incidents: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get(`${API_BASE}/stats`);
        setStats(response.data);
      } catch (error) {
        console.error("Error fetching stats:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const cards = [
    { label: 'Branches', value: stats?.branches || 0, icon: Building2, color: 'text-blue-400', bg: 'bg-blue-400/10' },
    { label: 'Employees', value: stats?.employees || 0, icon: Users, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
    { label: 'Clients', value: stats?.clients || 0, icon: ClipboardCheck, color: 'text-amber-400', bg: 'bg-amber-400/10' },
    { label: 'Active Incidents', value: stats?.active_incidents || 0, icon: ShieldAlert, color: 'text-rose-400', bg: 'bg-rose-400/10' },
  ];

  return (
    <div className="flex flex-col h-full space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-primary/20 rounded-2xl">
            <LayoutDashboard className="text-primary" size={28} />
          </div>
          <div>
            <h2 className="font-bold text-2xl">Care Dashboard</h2>
            <p className="text-sm text-secondary">Real-time oversight across all branches</p>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map((card, i) => (
          <div key={i} className="glass p-6 rounded-3xl space-y-4 border border-glass-border hover:border-primary/30 transition-all group">
            <div className={`w-12 h-12 ${card.bg} rounded-2xl flex items-center justify-center transition-transform group-hover:scale-110`}>
              <card.icon className={card.color} size={24} />
            </div>
            <div>
              <p className="text-secondary text-xs font-semibold uppercase tracking-wider">{card.label}</p>
              <h4 className="text-3xl font-black mt-1">
                {loading ? '...' : card.value}
              </h4>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-widest text-secondary/60">Operational Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button className="flex items-center justify-between p-6 glass rounded-2xl hover:bg-primary/5 transition-colors border border-glass-border group text-left">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-emerald-500/20 rounded-xl">
                <Calendar className="text-emerald-400" size={22} />
              </div>
              <div>
                <p className="font-bold">Generate Rota</p>
                <p className="text-xs text-secondary">AI-optimized scheduling for next week</p>
              </div>
            </div>
            <ArrowRight size={18} className="text-secondary opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all" />
          </button>

          <button className="flex items-center justify-between p-6 glass rounded-2xl hover:bg-primary/5 transition-colors border border-glass-border group text-left">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-rose-500/20 rounded-xl">
                <ShieldAlert className="text-rose-400" size={22} />
              </div>
              <div>
                <p className="font-bold">Quality Compliance</p>
                <p className="text-xs text-secondary">Review recent incidents & CQC levels</p>
              </div>
            </div>
            <ArrowRight size={18} className="text-secondary opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all" />
          </button>
        </div>
      </div>

      {/* Recent Activity Placeholder */}
      <div className="glass p-8 rounded-3xl flex-1 border border-glass-border">
        <h3 className="font-bold text-lg mb-6">Recent Activity Highlights</h3>
        <div className="space-y-6 opacity-40">
           <div className="flex gap-4 items-start">
             <div className="w-1 h-10 bg-emerald-500 rounded-full mt-1"></div>
             <div>
               <p className="text-sm font-semibold">Sarah Johnson updated the London Central Care Plan</p>
               <p className="text-xs">2 hours ago</p>
             </div>
           </div>
           <div className="flex gap-4 items-start">
             <div className="w-1 h-10 bg-amber-500 rounded-full mt-1"></div>
             <div>
               <p className="text-sm font-semibold">Incident #8439 (Medication) escalated to Under Investigation</p>
               <p className="text-xs">Yesterday at 4:12 PM</p>
             </div>
           </div>
        </div>
      </div>
    </div>
  );
}
