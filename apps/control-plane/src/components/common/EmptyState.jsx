"use client";

export default function EmptyState({
  title,
  description,
  actionLabel,
  onAction,
}) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white py-20">

      <div className="mb-4 text-5xl">
        📂
      </div>

      <h2 className="text-xl font-semibold">
        {title}
      </h2>

      <p className="mt-2 text-center text-slate-500">
        {description}
      </p>

      {actionLabel && (
        <button
          onClick={onAction}
          className="mt-6 rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-700"
        >
          {actionLabel}
        </button>
      )}

    </div>
  );
}