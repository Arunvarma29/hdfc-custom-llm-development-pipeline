"use client";

import { useQuery } from "@tanstack/react-query";
import { getDashboardSummary } from "@/services/dashboard.service";

export default function useDashboardSummary() {
  return useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: getDashboardSummary,
    refetchInterval: 15000,
    refetchOnWindowFocus: true,
  });
}