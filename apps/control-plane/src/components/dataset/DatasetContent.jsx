"use client";

import { useMemo, useState } from "react";

import DatasetToolbar from "./DatasetToolbar";
import DatasetTable from "./DatasetTable";
import Pagination from "./Pagination";
import UploadDialog from "./UploadDialog";
import DatasetDetailsDialog from "./DatasetDetailsDialog";
import DatasetTableSkeleton from "./DatasetTableSkeleton";

import EmptyState from "@/components/common/EmptyState";
import ConfirmationDialog from "../common/ConfirmationDialog";
import { useDeleteDataset } from "@/hooks/useDeleteDataset";

export default function DatasetContent({
  filters,
  onFilterChange,
  data,
  isLoading,
  isFetching,
  isError,
  onPageChange,
}) {
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [selectedDataset, setSelectedDataset] =
    useState(null);
  const [isDetailsOpen, setIsDetailsOpen] =
    useState(false);

  const [registryMode, setRegistryMode] =
    useState("all");

  const { mutate, isPending } =
    useDeleteDataset();

  const datasets = data?.items ?? [];

  const isKnowledgeDataset = (dataset) => {
    const type =
      dataset.dataset_type?.toLowerCase() || "";

    const contentType =
      dataset.content_type?.toLowerCase() || "";

    return (
      type === "documents" ||
      type === "document" ||
      contentType.includes("pdf") ||
      contentType.includes("word") ||
      contentType.includes("text/plain")
    );
  };

  const registryDatasets = useMemo(() => {
    if (registryMode === "all") {
      return datasets;
    }

    if (registryMode === "knowledge") {
      return datasets.filter(isKnowledgeDataset);
    }

    return datasets.filter(
      (dataset) => !isKnowledgeDataset(dataset)
    );
  }, [datasets, registryMode]);

  const summary = useMemo(() => {
    const source = registryDatasets;

    return {
      total: source.length,

      uploaded: source.filter(
        (item) => item.status === "UPLOADED"
      ).length,

      preparing: source.filter(
        (item) => item.status === "PREPARING"
      ).length,

      ready: source.filter(
        (item) => item.status === "READY"
      ).length,

      approved: source.filter(
        (item) => item.status === "APPROVED"
      ).length,

      knowledge: source.filter(
        isKnowledgeDataset
      ).length,
    };
  }, [registryDatasets]);

  if (isLoading) {
    return <DatasetTableSkeleton />;
  }

  if (isError) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 p-5">
        <p className="text-sm font-semibold text-red-700">
          Failed to load datasets.
        </p>

        <p className="mt-1 text-sm text-red-600">
          Please refresh the page and try again.
        </p>
      </div>
    );
  }

  const handleRegistryModeChange = (mode) => {
    setRegistryMode(mode);

    // Reset normal filters when switching workspace.
    onFilterChange("dataset_type", "");
    onFilterChange("status", "");
  };

  const handleDelete = () => {
    if (!selectedDataset) return;

    mutate(selectedDataset.id, {
      onSuccess: () => {
        setSelectedDataset(null);
      },
    });
  };

  const handleView = (dataset) => {
    setSelectedDataset(dataset);
    setIsDetailsOpen(true);
  };

  return (
    <>
      {/* Registry header */}
      <div className="mb-6 grid gap-4 lg:grid-cols-2">
        <div
          className={`rounded-2xl border p-5 transition ${
            registryMode === "structured"
              ? "border-blue-200 bg-blue-50"
              : "border-slate-200 bg-white"
          }`}
        >
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Structured Data
          </p>

          <h2 className="mt-1 text-lg font-bold text-slate-900">
            Data Preparation Pipeline
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            Tabular datasets used for preparation,
            quality validation and model development.
          </p>
        </div>

        <div
          className={`rounded-2xl border p-5 transition ${
            registryMode === "knowledge"
              ? "border-violet-200 bg-violet-50"
              : "border-slate-200 bg-white"
          }`}
        >
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Knowledge Documents
          </p>

          <h2 className="mt-1 text-lg font-bold text-slate-900">
            RAG / Knowledge Store
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            PDFs, documents and text sources stored
            for future retrieval-based AI workflows.
          </p>
        </div>
      </div>

      {/* Summary */}
      <div className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        <SummaryCard
          label={
            registryMode === "knowledge"
              ? "Documents"
              : "Total"
          }
          value={summary.total}
        />

        <SummaryCard
          label="Uploaded"
          value={summary.uploaded}
        />

        <SummaryCard
          label={
            registryMode === "knowledge"
              ? "Stored"
              : "Preparing"
          }
          value={
            registryMode === "knowledge"
              ? summary.total - summary.approved
              : summary.preparing
          }
        />

        <SummaryCard
          label="Ready"
          value={summary.ready}
        />

        <SummaryCard
          label={
            registryMode === "knowledge"
              ? "RAG Ready"
              : "Approved"
          }
          value={
            registryMode === "knowledge"
              ? 0
              : summary.approved
          }
        />
      </div>

      {/* Toolbar */}
      <DatasetToolbar
        filters={filters}
        onFilterChange={onFilterChange}
        isFetching={isFetching}
        onUploadClick={() =>
          setIsUploadOpen(true)
        }
        registryMode={registryMode}
        onRegistryModeChange={
          handleRegistryModeChange
        }
      />

      {/* Workspace description */}
      <div className="mb-4 flex flex-col gap-1">
        <h3 className="text-base font-semibold text-slate-900">
          {registryMode === "knowledge"
            ? "Knowledge Documents"
            : registryMode === "structured"
              ? "Structured Datasets"
              : "All Registered Data"}
        </h3>

        <p className="text-sm text-slate-500">
          {registryMode === "knowledge"
            ? "Documents are stored separately from the structured preparation pipeline."
            : registryMode === "structured"
              ? "Structured datasets follow the preparation and quality lifecycle."
              : "All registered data sources in the platform."}
        </p>
      </div>

      {/* Dataset table */}
      <div className="mt-4">
        {registryDatasets.length === 0 ? (
          <EmptyState
            title={
              registryMode === "knowledge"
                ? "No knowledge documents found"
                : "No datasets found"
            }
            description="Try changing your filters or upload a new source."
            actionLabel="Upload Dataset"
            onAction={() =>
              setIsUploadOpen(true)
            }
          />
        ) : (
          <>
            <DatasetTable
              datasets={registryDatasets}
              onDelete={setSelectedDataset}
              onView={handleView}
            />

            {data?.pagination && (
              <Pagination
                pagination={data.pagination}
                onPageChange={onPageChange}
              />
            )}
          </>
        )}
      </div>

      {/* Upload */}
      <UploadDialog
        isOpen={isUploadOpen}
        onClose={() =>
          setIsUploadOpen(false)
        }
      />

      {/* Delete */}
      <ConfirmationDialog
        isOpen={
          !!selectedDataset && !isDetailsOpen
        }
        title="Delete Dataset"
        message={
          selectedDataset
            ? `You are about to permanently delete "${selectedDataset.name}".\n\nThis action cannot be undone.`
            : ""
        }
        confirmText="Delete"
        cancelText="Cancel"
        onConfirm={handleDelete}
        onCancel={() =>
          setSelectedDataset(null)
        }
        isLoading={isPending}
      />

      {/* Details */}
      <DatasetDetailsDialog
        dataset={selectedDataset}
        isOpen={isDetailsOpen}
        onClose={() => {
          setSelectedDataset(null);
          setIsDetailsOpen(false);
        }}
      />
    </>
  );
}

function SummaryCard({
  label,
  value,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-2xl font-bold text-slate-900">
        {value}
      </p>
    </div>
  );
}