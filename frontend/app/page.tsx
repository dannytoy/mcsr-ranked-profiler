'use client';

import { useState } from 'react';
import PlayerForm from './components/PlayerForm';
import ResultsDisplay from './components/ResultsDisplay';
import { PlayerProfile } from './types';

export default function Home() {
  const [profile, setProfile] = useState<PlayerProfile | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (username: string) => {
    setIsLoading(true);
    setError(null);
    setProfile(null);

    try {
      const response = await fetch(`http://localhost:8000/profile/${username}`);
      if (!response.ok) {
        throw new Error('Player not found or not enough data.');
      }
      const data: PlayerProfile = await response.json();
      setProfile(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching the profile.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center gap-8 text-center">
      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400 sm:text-5xl md:text-6xl">
          MCSR Ranked Profiler
        </h1>
        <p className="max-w-[600px] text-slate-400 md:text-xl">
          Enter a username to analyze their playstyle, predict their true Elo, and discover their archetype.
        </p>
      </div>

      <PlayerForm onSubmit={handleSearch} isLoading={isLoading} />

      {error && (
        <div className="w-full max-w-md rounded-lg bg-red-500/10 px-6 py-4 text-center text-red-400 border border-red-500/50">
          {error}
        </div>
      )}

      {profile && !isLoading && <ResultsDisplay profile={profile} />}
    </div>
  );
}