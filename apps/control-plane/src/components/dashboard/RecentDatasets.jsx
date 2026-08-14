"use client";

import Link from "next/link";

function getStatusStyle(status) {
  switch (status) {
    case "APPROVED":
      return "bg-emerald-50 text-emerald-700";

    case "READY":
      return "bg-blue-50 text-blue-700";

    case "PREPARING":
      return "bg-amber-50 text-amber-700";

    case "REJECTED":
      return "bg-red-50 text-red-700";

    default:
      return "bg-slate-100 text-slate-600";
  }
}

export default function RecentDatasets({
  datasets = [],
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="mb-5 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Recent Dataset Uploads
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Latest registered datasets.
          </p>
        </div>

        <Link
          href="/datasets"
          className="text-sm font-semibold text-blue-600 hover:text-blue-700"
        >
          View all
        </Link>
      </div>

      {datasets.length === 0 ? (
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center">
          <p className="text-sm font-medium text-slate-700">
            No datasets yet
          </p>

          <p className="mt-1 text-sm text-slate-500">
            Upload your first dataset from the Dataset Registry.
          </p>
        </div>
      ) : (
        <>
          {/* Desktop */}
          <div className="hidden overflow-x-auto md:block">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Name
                  </th>

                  <th className="py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Type
                  </th>

                  <th className="py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Version
                  </th>

                  <th className="py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Status
                  </th>

                  <th className="py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Created
                  </th>
                </tr>
              </thead>

              <tbody>
                {datasets.map((dataset) => (
                  <tr
                    key={dataset.id}
                    className="border-b border-slate-100 last:border-0"
                  >
                    <td className="py-4 font-medium text-slate-900">
                      {dataset.name}
                    </td>

                    <td className="py-4 text-sm text-slate-600">
                      {dataset.dataset_type}
                    </td>

                    <td className="py-4 text-sm text-slate-600">
                      {dataset.version}
                    </td>

                    <td className="py-4">
                      <span
                        className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${getStatusStyle(
                          dataset.status
                        )}`}
                      >
                        {dataset.status}
                      </span>
                    </td>

                    <td className="py-4 text-sm text-slate-500">
                      {new Date(
                        dataset.created_at
                      ).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile */}
          <div className="space-y-3 md:hidden">
            {datasets.map((dataset) => (
              <div
                key={dataset.id}
                className="rounded-xl border border-slate-200 p-4"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate font-semibold text-slate-900">
                      {dataset.name}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {dataset.dataset_type} · v
                      {dataset.version}
                    </p>
                  </div>

                  <span
                    className={`shrink-0 rounded-full px-2.5 py-1 text-xs font-semibold ${getStatusStyle(
                      dataset.status
                    )}`}
                  >
                    {dataset.status}
                  </span>
                </div>

                <p className="mt-3 text-xs text-slate-500">
                  {new Date(
                    dataset.created_at
                  ).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}