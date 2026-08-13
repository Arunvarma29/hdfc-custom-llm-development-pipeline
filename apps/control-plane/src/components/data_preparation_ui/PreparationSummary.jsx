"use client";

export default function PreparationSummary({ summary }) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
      <SummaryCard title="Total Datasets" value={summary.total} />
      <SummaryCard title="Queued" value={summary.queued} />
      <SummaryCard title="Running" value={summary.running} />
      <SummaryCard title="Ready" value={summary.ready} />
      <SummaryCard title="Approved" value={summary.approved} />
    </div>
  );
}

function SummaryCard({ title, value }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {title}
      </p>
      <p className="mt-2 text-2xl font-bold text-slate-900">{value}</p>
    </div>
  );
}
