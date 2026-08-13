"use client";

export default function PreparationJobCard({
  preparation,
  loading,
}) {
  return (
    <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">
        Preparation Job
      </h2>
      <p className="mt-1 text-sm text-slate-500">
        Track the preparation lifecycle for the selected dataset.
      </p>

      {loading ? (
        <LoadingPanel text="Loading preparation status..." />
      ) : preparation ? (
        <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <Info label="Job ID" value={preparation.id} />
          <Info label="Status" value={preparation.status} />
          <Info label="Attempts" value={preparation.attempts} />
          <Info label="Created" value={formatDate(preparation.created_at)} />
          <Info label="Started" value={formatDate(preparation.started_at)} />
          <Info label="Completed" value={formatDate(preparation.completed_at)} />
          <Info label="Error" value={preparation.error_message || "—"} />
        </div>
      ) : (
        <EmptyPanel text="No preparation job found for this dataset." />
      )}
    </div>
  );
}

function formatDate(value) {
  return value ? new Date(value).toLocaleString() : "—";
}

function Info({ label, value }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      <p className="mt-1 break-all text-sm font-semibold text-slate-900">
        {value ?? "—"}
      </p>
    </div>
  );
}

function LoadingPanel({ text }) {
  return (
    <div className="mt-6 rounded-xl bg-slate-50 p-6">
      <p className="text-sm text-slate-500">{text}</p>
    </div>
  );
}

function EmptyPanel({ text }) {
  return (
    <div className="mt-6 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center">
      <p className="text-sm text-slate-500">{text}</p>
    </div>
  );
}
