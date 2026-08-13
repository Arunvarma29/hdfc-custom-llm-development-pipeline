"use client";

import { useState } from "react";
import { prepareDataset } from "@/services/dataset.service";

export default function usePrepareDataset() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const prepare = async (datasetId) => {
    setLoading(true);
    setError(null);

    try {
      return await prepareDataset(datasetId);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Failed to prepare dataset"
      );

      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    prepare,
    loading,
    error,
  };
}