"use client";

import { FaCheckCircle, FaPlay } from "react-icons/fa";

export default function SelectedDatasetCard({
  dataset,
  preparation,
  runningPreparation,
  qualityRunning,
  runMessage,
  qualityMessage,
  onRunPreparation,
  onRunQualityCheck,
}) {
  return (
    <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Selected Dataset
          </p>
          <h2 className="mt-1 truncate text-lg font-bold text-slate-900">
            {dataset.name}
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            {dataset.dataset_type} · {dataset.domain} · Version {dataset.version}
          </p>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div className="rounded-full bg-slate-100 px-3 py-1 text-center text-xs font-semibold text-slate-600">
            {dataset.status}
          </div>

          {preparation?.status === "QUEUED" && (
            <button
              type="button"
              onClick={onRunPreparation}
              disabled={runningPreparation}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <FaPlay size={12} />
              {runningPreparation ? "Running..." : "Run Preparation"}
            </button>
          )}

          {preparation?.status === "RUNNING" && (
            <span className="rounded-xl bg-amber-50 px-4 py-2.5 text-sm font-semibold text-amber-700 ring-1 ring-inset ring-amber-200">
              Preparation Running
            </span>
          )}

          {preparation?.status === "COMPLETED" && (
            <button
              type="button"
              onClick={onRunQualityCheck}
              disabled={qualityRunning}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {qualityRunning ? "Checking..." : "Run Quality Check"}
            </button>
          )}

          {preparation?.status === "FAILED" && (
            <button
              type="button"
              onClick={onRunPreparation}
              disabled={runningPreparation}
              className="rounded-xl bg-red-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-red-700 disabled:opacity-50"
            >
              {runningPreparation ? "Retrying..." : "Retry Preparation"}
            </button>
          )}
        </div>
      </div>

      {(runMessage || qualityMessage) && (
        <div className="mt-4 grid gap-3">
          {runMessage && (
            <Message text={runMessage} />
          )}
          {qualityMessage && (
            <Message text={qualityMessage} />
          )}
        </div>
      )}
    </div>
  );
}

function Message({ text }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">
      {text}
    </div>
  );
}
