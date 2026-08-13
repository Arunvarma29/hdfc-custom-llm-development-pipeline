"use client";

import { FaCheckCircle } from "react-icons/fa";

export default function QualityGateCard({
  qualityReport,
  loading,
}) {
  const qualityChecks = qualityReport?.checks ?? [];
  const failedChecks = qualityReport?.failed_checks ?? [];
  const qualityPassed = qualityReport?.status === "PASS";

  return (
    <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Quality Gate
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Validation evidence produced by the preparation pipeline.
          </p>
        </div>

        <div
          className={`inline-flex items-center gap-2 self-start rounded-full px-3 py-1.5 text-xs font-semibold ${
            qualityPassed
              ? "bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-200"
              : qualityReport?.status === "FAIL"
                ? "bg-red-50 text-red-700 ring-1 ring-inset ring-red-200"
                : "bg-slate-50 text-slate-600 ring-1 ring-inset ring-slate-200"
          }`}
        >
          {qualityPassed && <FaCheckCircle />}
          {qualityReport?.status || "NOT AVAILABLE"}
        </div>
      </div>

      {loading ? (
        <div className="mt-6 rounded-xl bg-slate-50 p-6">
          <p className="text-sm text-slate-500">
            Loading quality report...
          </p>
        </div>
      ) : qualityReport ? (
        <>
          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            <MetricCard label="Checks" value={qualityChecks.length} />
            <MetricCard label="Failed Checks" value={failedChecks.length} />
            <MetricCard label="Gate Result" value={qualityReport.status} />
          </div>

          <div className="mt-5">
            <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500">
              Checks
            </p>
            <div className="grid gap-2">
              {qualityChecks.map((check, index) => (
                <div
                  key={`${check.name}-${index}`}
                  className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
                >
                  <span className="text-sm font-medium capitalize text-slate-700">
                    {check.name?.replaceAll("_", " ")}
                  </span>
                  <span
                    className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ${
                      check.status === "PASS"
                        ? "bg-emerald-50 text-emerald-700"
                        : "bg-red-50 text-red-700"
                    }`}
                  >
                    {check.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </>
      ) : (
        <div className="mt-6 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center">
          <p className="text-sm text-slate-500">
            No quality report available yet.
          </p>
        </div>
      )}
    </div>
  );
}

function MetricCard({ label, value }) {
  return (
    <div className="rounded-xl bg-slate-50 p-4">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      <p className="mt-1 text-2xl font-bold text-slate-900">{value}</p>
    </div>
  );
}
