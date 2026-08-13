"use client";

import { FaSearch } from "react-icons/fa";
import {
  DATASET_TYPES,
  DATASET_STATUSES,
} from "@/constants/datasetOptions";

export default function DatasetToolbar({
  filters,
  onFilterChange,
  isFetching,
  onUploadClick,
  registryMode,
  onRegistryModeChange,
}) {
  return (
    <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5">
      {/* Registry partitions */}
      <div className="mb-5 border-b border-slate-200 pb-4">
        <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500">
          Dataset Workspace
        </p>

        <div className="flex flex-wrap gap-2">
          <ModeButton
            active={registryMode === "all"}
            onClick={() => onRegistryModeChange("all")}
          >
            All Data
          </ModeButton>

          <ModeButton
            active={registryMode === "structured"}
            onClick={() =>
              onRegistryModeChange("structured")
            }
          >
            Structured Data
          </ModeButton>

          <ModeButton
            active={registryMode === "knowledge"}
            onClick={() =>
              onRegistryModeChange("knowledge")
            }
          >
            Knowledge Documents
          </ModeButton>
        </div>
      </div>

      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        {/* Filters */}
        <div className="grid flex-1 gap-3 sm:grid-cols-2 lg:grid-cols-[minmax(240px,1.6fr)_minmax(160px,1fr)_minmax(160px,1fr)]">
          {/* Search */}
          <div className="relative">
            <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />

            <input
              type="text"
              placeholder={
                registryMode === "knowledge"
                  ? "Search documents..."
                  : "Search datasets..."
              }
              value={filters.search}
              onChange={(e) =>
                onFilterChange(
                  "search",
                  e.target.value
                )
              }
              className="w-full rounded-xl border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            />

            {isFetching && (
              <div className="mt-2 flex items-center gap-2 text-xs text-blue-600">
                <div className="h-3 w-3 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
                <span>Searching...</span>
              </div>
            )}
          </div>

          {/* Dataset Type */}
          <select
            value={filters.dataset_type}
            onChange={(e) =>
              onFilterChange(
                "dataset_type",
                e.target.value
              )
            }
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          >
            <option value="">All Types</option>

            {DATASET_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>

          {/* Status */}
          <select
            value={filters.status}
            onChange={(e) =>
              onFilterChange(
                "status",
                e.target.value
              )
            }
            className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          >
            <option value="">All Status</option>

            {DATASET_STATUSES.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
        </div>

        {/* Upload */}
        <button
          onClick={onUploadClick}
          className="w-full shrink-0 rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-300 sm:w-auto"
        >
          + Upload Dataset
        </button>
      </div>
    </div>
  );
}

function ModeButton({
  active,
  onClick,
  children,
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
        active
          ? "bg-slate-900 text-white shadow-sm"
          : "bg-slate-100 text-slate-600 hover:bg-slate-200"
      }`}
    >
      {children}
    </button>
  );
}