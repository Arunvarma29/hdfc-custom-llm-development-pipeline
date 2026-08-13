"use client";

import { useState } from "react";
import { runPreparation } from "@/services/dataset.service";

export default function useRunPreparation() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const run = async (datasetId) => {
    setLoading(true);
    setError(null);

    try {
      return await runPreparation(datasetId);
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    run,
    loading,
    error,
  };
}