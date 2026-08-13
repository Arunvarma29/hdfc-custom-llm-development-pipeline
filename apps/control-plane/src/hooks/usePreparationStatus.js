"use client";

import { useState } from "react";
import { getPreparationStatus } from "@/services/dataset.service";

export default function usePreparationStatus() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getStatus = async (datasetId) => {
    setLoading(true);
    setError(null);

    try {
      return await getPreparationStatus(datasetId);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Failed to get preparation status"
      );

      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    getStatus,
    loading,
    error,
  };
}