import './globals.css';
import { ReactNode } from 'react';
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata = {
  title: 'MCSR Ranked Profiler',
  description: 'Predict player archetypes and Elo in MCSR Ranked.',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable}`}>
      <body className="min-h-screen bg-[#0A0A0A] text-slate-100 font-sans selection:bg-emerald-500 selection:text-white relative">
        <div className="fixed top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_center,_rgba(20,83,45,0.4),_transparent_40%)] -z-10 pointer-events-none"></div>
        <main className="container mx-auto flex min-h-screen flex-col items-center justify-center p-8 relative z-10">
          {children}
        </main>
      </body>
    </html>
  );
}