"use client";

import { useState } from 'react';
import Chat from '@/components/Chat';
import Ingest from '@/components/Ingest';
import Dashboard from '@/components/Dashboard';
import { 
  Activity, 
  Settings, 
  LogOut,
  ChevronRight,
  ShieldCheck,
  BrainCircuit,
  LayoutDashboard,
  Sun,
  Moon
} from 'lucide-react';

export default function Home() {
  const [activeView, setActiveView] = useState<'dashboard' | 'training'>('dashboard');
  const [isDark, setIsDark] = useState(true);

  const toggleTheme = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle('light');
  };

  return (
    <main className={`flex h-[100vh] overflow-hidden ${isDark ? 'bg-[#0A0C10] text-gray-100' : 'bg-white text-gray-900'} transition-colors duration-300`}>
      {/* Sidebar Navigation */}
      <aside className={`w-72 border-r ${isDark ? 'border-white/5 bg-[#0D0F14]' : 'border-gray-200 bg-gray-50'} flex flex-col p-8 transition-colors duration-300`}>
        <div className="flex items-center gap-3 mb-12">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
            <ShieldCheck className="text-white" size={24} />
          </div>
          <div>
            <h1 className="font-black text-xl tracking-tight">Curriculo</h1>
            <p className="text-[10px] text-primary font-bold uppercase tracking-[0.2em]">Platform AI</p>
          </div>
        </div>

        <nav className="flex-1 space-y-2">
          <button 
            onClick={() => setActiveView('dashboard')}
            className={`w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all ${
              activeView === 'dashboard' ? 'bg-primary/10 text-primary border border-primary/20' : 'text-secondary hover:bg-white/5'
            }`}
          >
            <div className="flex items-center gap-3">
              <LayoutDashboard size={20} />
              <span className="font-semibold text-sm">Dashboard</span>
            </div>
          </button>

          <button 
            onClick={() => setActiveView('training')}
            className={`w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all ${
              activeView === 'training' ? 'bg-primary/10 text-primary border border-primary/20' : 'text-secondary hover:bg-white/5'
            }`}
          >
            <div className="flex items-center gap-3">
              <BrainCircuit size={20} />
              <span className="font-semibold text-sm">Training AI</span>
            </div>
            <span className="text-[10px] bg-amber-500/20 text-amber-500 px-2 py-0.5 rounded-full font-bold">Beta</span>
          </button>
        </nav>

        <div className="pt-8 border-t border-white/5 space-y-4">
          <button 
            onClick={toggleTheme}
            className="flex items-center gap-3 text-secondary text-sm hover:text-primary transition-colors w-full px-4"
          >
            {isDark ? <Sun size={18} /> : <Moon size={18} />}
            <span>{isDark ? 'Light' : 'Dark'} Mode</span>
          </button>
          <button className="flex items-center gap-3 text-secondary text-sm hover:text-white transition-colors w-full px-4">
            <Settings size={18} />
            <span>Settings</span>
          </button>
          <button className="flex items-center gap-3 text-rose-500 text-sm hover:text-rose-400 transition-colors w-full px-4">
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Navbar */}
        <header className={`h-20 border-b ${isDark ? 'border-white/5 bg-[#0A0C10]/80' : 'border-gray-200 bg-white/80'} backdrop-blur-xl flex items-center justify-between px-10 z-10 transition-colors duration-300`}>
          <div className="flex items-center gap-2 text-sm text-secondary">
            <span>Admin</span>
            <ChevronRight size={14} />
            <span className={`${isDark ? 'text-white' : 'text-gray-900'} font-medium capitalize`}>{activeView}</span>
          </div>

          <div className="flex items-center gap-6">
             <div className="flex items-center gap-2 bg-emerald-500/10 px-3 py-1.5 rounded-full border border-emerald-500/20">
               <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
               <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">System Live</span>
             </div>
             <div className="w-10 h-10 bg-white/5 border border-white/10 rounded-full flex items-center justify-center font-bold text-sm">
                MK
             </div>
          </div>
        </header>

        {/* Content View */}
        <div className="flex-1 p-10 overflow-y-auto overflow-x-hidden custom-scrollbar">
          <div className="max-w-6xl mx-auto h-full flex flex-col gap-10">
            {activeView === 'dashboard' ? (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 h-full">
                <div className="lg:col-span-12 h-fit">
                   <Dashboard />
                </div>
                <div className="lg:col-span-12 h-[500px]">
                   <Chat />
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 h-full">
                <div className="lg:col-span-6">
                  <Ingest />
                </div>
                <div className="lg:col-span-6">
                  <Chat />
                </div>
              </div>
            )}
            
            <footer className="text-center py-8 text-[10px] text-secondary/20 font-medium uppercase tracking-[0.2em] mt-auto">
              Curriculo Care Management Platform &copy; 2026 Admin Portal
            </footer>
          </div>
        </div>
      </div>
    </main>
  );
}
