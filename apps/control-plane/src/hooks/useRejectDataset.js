"use client";

import { useState } from "react";
import { rejectDataset } from "@/services/dataset.service";

export default function useRejectDataset() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const reject = async (datasetId, review = {}) => {
    setLoading(true);
    setError(null);

    try {
      return await rejectDataset(datasetId, review);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Failed to reject dataset"
      );

      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    reject,
    loading,
    error,
  };
}