"use client";

import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import PageHeader from "@/components/common/PageHeader";
import { useDatasets } from "../../../hooks/useDatasets";
import { usePreparationJobs } from "../../../hooks/usePreparationJobs";
import useRunPreparation from "../../../hooks/useRunnerPreparation";
import useRunQualityCheck from "../../../hooks/useRunQualityCheck";
import {
  getPreparedArtifact,
  getQualityReport,
} from "@/services/dataset.service";

import PreparationSummary from "../../../components/data_preparation_ui/PreparationSummary";
import DatasetSearch from "../../../components/data_preparation_ui/DatasetSearch";
import SelectedDatasetCard from "../../../components/data_preparation_ui/SelectedDatasetCard";
import PreparationJobCard from "../../../components/data_preparation_ui/PreparationJobCard";
import QualityGateCard from "../../../components/data_preparation_ui/QualityGateCard";
import PreparedArtifactCard from "../../../components/data_preparation_ui/PreparedArtifactCard";

export default function DataPreparationPage() {
  const [selectedDatasetId, setSelectedDatasetId] = useState("");
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [runMessage, setRunMessage] = useState("");
  const [qualityMessage, setQualityMessage] = useState("");

  const { data, isLoading } = useDatasets({
    page: 1,
    limit: 100,
  });

  const {
    data: preparation,
    isLoading: preparationLoading,
    refetch: refetchPreparation,
  } = usePreparationJobs(selectedDatasetId);

  const { run: runPreparation, loading: runningPreparation } =
    useRunPreparation();

  const { run: runQualityCheck, loading: qualityRunning } =
    useRunQualityCheck();

  const {
    data: qualityReport,
    isLoading: qualityLoading,
    refetch: refetchQuality,
  } = useQuery({
    queryKey: ["quality-report", selectedDatasetId],
    queryFn: () => getQualityReport(selectedDatasetId),
    enabled: Boolean(selectedDatasetId),
  });

  const {
    data: artifact,
    isLoading: artifactLoading,
    refetch: refetchArtifact,
  } = useQuery({
    queryKey: ["prepared-artifact", selectedDatasetId],
    queryFn: () => getPreparedArtifact(selectedDatasetId),
    enabled: Boolean(selectedDatasetId),
  });

  const datasets = data?.items ?? [];

  const selectedDataset =
    datasets.find((dataset) => dataset.id === selectedDatasetId) ?? null;

  const filteredDatasets = useMemo(() => {
    const query = search.trim().toLowerCase();

    return datasets.filter((dataset) => {
      const matchesSearch =
        !query ||
        dataset.name?.toLowerCase().includes(query) ||
        dataset.dataset_type?.toLowerCase().includes(query) ||
        dataset.domain?.toLowerCase().includes(query) ||
        dataset.version?.toLowerCase().includes(query);

      const matchesType =
        !typeFilter ||
        dataset.dataset_type?.toLowerCase() === typeFilter.toLowerCase();

      const matchesStatus =
        !statusFilter ||
        dataset.status?.toUpperCase() === statusFilter.toUpperCase();

      return matchesSearch && matchesType && matchesStatus;
    });
  }, [datasets, search, typeFilter, statusFilter]);

  const datasetTypes = useMemo(
    () => [
      ...new Set(
        datasets.map((dataset) => dataset.dataset_type).filter(Boolean)
      ),
    ],
    [datasets]
  );

  const datasetStatuses = useMemo(
    () => [
      ...new Set(
        datasets.map((dataset) => dataset.status).filter(Boolean)
      ),
    ],
    [datasets]
  );

  const summary = useMemo(
    () => ({
      total: data?.pagination?.total ?? datasets.length,
      queued: datasets.filter((dataset) => dataset.status === "UPLOADED").length,
      running: datasets.filter((dataset) => dataset.status === "PREPARING").length,
      ready: datasets.filter((dataset) => dataset.status === "READY").length,
      approved: datasets.filter((dataset) => dataset.status === "APPROVED").length,
    }),
    [data, datasets]
  );

  const handleRunPreparation = async () => {
    if (!selectedDatasetId) return;

    setRunMessage("");

    try {
      const result = await runPreparation(selectedDatasetId);

      await Promise.all([
        refetchPreparation(),
        refetchQuality(),
        refetchArtifact(),
      ]);

      setRunMessage(
        result?.result === true
          ? "Preparation completed successfully."
          : "Preparation run finished."
      );
    } catch (error) {
      setRunMessage(
        error?.response?.data?.detail ||
          "Preparation could not be started."
      );
      await refetchPreparation();
    }
  };

  const handleRunQualityCheck = async () => {
    if (!selectedDatasetId) return;

    setQualityMessage("");

    try {
      const result = await runQualityCheck(selectedDatasetId);

      setQualityMessage(
        result?.status === "PASS"
          ? "Quality check passed."
          : "Quality check completed with failures."
      );

      await Promise.all([
        refetchQuality(),
        refetchArtifact(),
        refetchPreparation(),
      ]);
    } catch (error) {
      setQualityMessage(
        error?.response?.data?.detail ||
          "Quality check could not be completed."
      );
    }
  };

  return (
    <div>
      <PageHeader
        title="Data Preparation"
        description="Prepare, validate, and freeze datasets for model development."
      />

      <PreparationSummary summary={summary} />

      <DatasetSearch
        datasets={filteredDatasets}
        totalResults={filteredDatasets.length}
        search={search}
        typeFilter={typeFilter}
        statusFilter={statusFilter}
        datasetTypes={datasetTypes}
        datasetStatuses={datasetStatuses}
        isLoading={isLoading}
        selectedDatasetId={selectedDatasetId}
        onSearchChange={setSearch}
        onTypeChange={setTypeFilter}
        onStatusChange={setStatusFilter}
        onSelect={setSelectedDatasetId}
      />

      {selectedDataset ? (
        <>
          <SelectedDatasetCard
            dataset={selectedDataset}
            preparation={preparation}
            runningPreparation={runningPreparation}
            qualityRunning={qualityRunning}
            runMessage={runMessage}
            qualityMessage={qualityMessage}
            onRunPreparation={handleRunPreparation}
            onRunQualityCheck={handleRunQualityCheck}
          />

          <PreparationJobCard
            preparation={preparation}
            loading={preparationLoading}
          />

          <QualityGateCard
            qualityReport={qualityReport}
            loading={qualityLoading}
          />

          <PreparedArtifactCard
            artifact={artifact}
            loading={artifactLoading}
          />
        </>
      ) : (
        <div className="mt-6 rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-10 text-center">
          <p className="text-sm font-medium text-slate-700">
            Select a dataset to open its preparation workspace.
          </p>
          <p className="mt-1 text-sm text-slate-500">
            Search above to quickly find the dataset you need.
          </p>
        </div>
      )}
    </div>
  );
}
