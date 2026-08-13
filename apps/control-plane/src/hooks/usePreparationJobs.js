"use client";

import { useQuery } from "@tanstack/react-query";
import { getPreparationStatus } from "@/services/dataset.service";

export function usePreparationJobs(datasetId) {
  return useQuery({
    queryKey: ["preparation-status", datasetId],
    queryFn: () => getPreparationStatus(datasetId),
    enabled: Boolean(datasetId),
  });
}