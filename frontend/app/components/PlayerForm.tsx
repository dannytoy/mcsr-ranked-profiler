'use client';

import { useState, FormEvent } from 'react';

interface Props {
  onSubmit: (username: string) => void;
  isLoading: boolean;
}

export default function PlayerForm({ onSubmit, isLoading }: Props) {
  const [username, setUsername] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (username.trim()) {
      onSubmit(username.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex w-full max-w-md flex-col gap-4 sm:flex-row">
      <input
        type="text"
        placeholder="Enter MCSR Username..."
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        disabled={isLoading}
        className="flex-1 rounded-xl border border-slate-700 bg-slate-900/50 px-4 py-3.5 text-white placeholder-slate-400 shadow-inner backdrop-blur-sm transition-all focus:border-emerald-500 focus:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={isLoading || !username.trim()}
        className="flex min-w-[140px] items-center justify-center rounded-xl bg-emerald-600 px-6 py-3.5 font-bold text-white shadow-lg shadow-emerald-900/20 transition-all hover:-translate-y-0.5 hover:bg-emerald-500 hover:shadow-emerald-900/40 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0 disabled:hover:bg-emerald-600"
      >
        {isLoading ? (
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-white/20 border-t-white" />
        ) : (
          'Analyze'
        )}
      </button>
    </form>
  );
}