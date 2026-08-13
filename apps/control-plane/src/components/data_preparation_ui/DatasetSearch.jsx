"use client";

import { FaFilter, FaSearch } from "react-icons/fa";

export default function DatasetSearch({
  datasets,
  totalResults,
  search,
  typeFilter,
  statusFilter,
  datasetTypes,
  datasetStatuses,
  isLoading,
  selectedDatasetId,
  onSearchChange,
  onTypeChange,
  onStatusChange,
  onSelect,
}) {
  return (
    <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5">
      <div className="flex items-center gap-2">
        <FaFilter className="text-slate-400" />
        <div>
          <h2 className="text-sm font-semibold text-slate-900">
            Find Dataset
          </h2>
          <p className="text-xs text-slate-500">
            Search or filter to open a preparation workspace.
          </p>
        </div>
      </div>

      <div className="mt-4 grid gap-3 lg:grid-cols-[minmax(260px,1.7fr)_180px_180px]">
        <div className="relative">
          <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search by name, type, domain or version..."
            className="w-full rounded-xl border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <select
          value={typeFilter}
          onChange={(event) => onTypeChange(event.target.value)}
          className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        >
          <option value="">All Types</option>
          {datasetTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>

        <select
          value={statusFilter}
          onChange={(event) => onStatusChange(event.target.value)}
          className="w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        >
          <option value="">All Status</option>
          {datasetStatuses.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </div>

      <div className="mt-4">
        <div className="mb-2 flex items-center justify-between">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Matching Datasets
          </p>
          <p className="text-xs text-slate-400">
            {totalResults} result{totalResults === 1 ? "" : "s"}
          </p>
        </div>

        <div className="max-h-64 overflow-y-auto rounded-xl border border-slate-200 bg-slate-50">
          {isLoading ? (
            <div className="p-5 text-sm text-slate-500">
              Loading datasets...
            </div>
          ) : datasets.length === 0 ? (
            <div className="p-5 text-center">
              <p className="text-sm font-medium text-slate-700">
                No matching datasets
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Try another search term or clear the filters.
              </p>
            </div>
          ) : (
            <div className="divide-y divide-slate-200">
              {datasets.map((dataset) => {
                const selected = dataset.id === selectedDatasetId;

                return (
                  <button
                    key={dataset.id}
                    type="button"
                    onClick={() => onSelect(dataset.id)}
                    className={`flex w-full items-center justify-between gap-4 px-4 py-3 text-left transition ${
                      selected
                        ? "bg-blue-50"
                        : "bg-white hover:bg-slate-50"
                    }`}
                  >
                    <div className="min-w-0">
                      <p className="truncate text-sm font-semibold text-slate-900">
                        {dataset.name}
                      </p>
                      <p className="mt-1 truncate text-xs text-slate-500">
                        {dataset.dataset_type} · {dataset.domain} · v{dataset.version}
                      </p>
                    </div>
                    <span className="shrink-0 rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-semibold text-slate-600">
                      {dataset.status}
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
