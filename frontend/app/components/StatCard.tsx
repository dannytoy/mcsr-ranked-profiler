interface StatCardProps {
  label: string;
  value: string | number;
}

export default function StatCard({ label, value }: StatCardProps) {
  return (
    <div className="p-4 bg-slate-900/80 border border-slate-800 rounded-xl text-center backdrop-blur-md">
      <p className="text-sm text-slate-400 mb-1">{label}</p>
      <p className="text-2xl font-semibold text-white">{value}</p>
    </div>
  );
}