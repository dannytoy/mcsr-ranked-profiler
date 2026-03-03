'use client';

import { PlayerProfile } from '../types';
import StatCard from './StatCard';

interface Props {
  profile: PlayerProfile;
}

const formatTime = (ms: number) => {
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000);
  const milliseconds = ms % 1000;
  return `${minutes}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(3, '0')}`;
};

export default function ResultsDisplay({ profile }: Props) {
  return (
    <div className="w-full max-w-4xl animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="space-y-6">
        <div className="p-8 bg-slate-900/80 border border-emerald-500/30 rounded-2xl shadow-2xl backdrop-blur-md">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="text-center md:text-left">
              <h2 className="text-5xl font-bold text-white tracking-tight">{profile.username}</h2>
              <p className="mt-3 text-xl font-medium text-emerald-400">{profile.player_archetype}</p>
            </div>
            <div className="flex gap-4 p-4 bg-slate-950/70 border border-slate-800 rounded-xl">
              <div className="px-6 text-center">
                <p className="text-sm uppercase tracking-wider text-slate-400">Official</p>
                <p className="text-4xl font-bold text-white">{profile.official_elo}</p>
                <p className="text-base text-slate-500">{profile.official_rank}</p>
              </div>
              <div className="w-px bg-slate-800"></div>
              <div className="px-6 text-center">
                <p className="text-sm uppercase tracking-wider text-slate-400">Predicted</p>
                <p className="text-4xl font-bold text-cyan-400">{profile.predicted_elo}</p>
                <p className="text-base text-slate-500">{profile.predicted_rank}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard label="Personal Best" value={formatTime(profile.best_time)} />
          <StatCard label="Average Time" value={formatTime(profile.average_time)} />
          <StatCard label="Win Rate" value={`${((profile.win_rate ?? 0) * 100).toFixed(1)}%`} />
          <StatCard label="Consistency" value={(profile.consistency_ratio ?? 0).toFixed(2)} />
        </div>

        <div className="p-6 bg-slate-900/80 border border-slate-800 rounded-xl backdrop-blur-md">
          <h3 className="text-lg font-semibold text-white mb-4">Match History</h3>
          <div className="space-y-3 text-base">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Total Games</span>
              <span className="font-medium text-white">{profile.total_games}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Wins</span>
              <span className="font-medium text-emerald-400">{profile.total_wins}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Losses</span>
              <span className="font-medium text-red-400">{profile.total_losses}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}