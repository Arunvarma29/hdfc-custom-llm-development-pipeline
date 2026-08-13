"use client";

import { useState } from "react";
import { approveDataset } from "@/services/dataset.service";

export default function useApproveDataset() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const approve = async (datasetId, review = {}) => {
    setLoading(true);
    setError(null);

    try {
      return await approveDataset(datasetId, review);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Failed to approve dataset"
      );

      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    approve,
    loading,
    error,
  };
}