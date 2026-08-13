"use client";

export default function DatasetTableSkeleton() {
  return (
    <div className="overflow-hidden rounded-xl border bg-white">

      <div className="animate-pulse">

        {[...Array(8)].map((_, row) => (
          <div
            key={row}
            className="flex border-b p-4"
          >
            {[...Array(7)].map((_, col) => (
              <div
                key={col}
                className="mx-2 h-4 flex-1 rounded bg-slate-200"
              />
            ))}
          </div>
        ))}

      </div>

    </div>
  );
}