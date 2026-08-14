import api from "./api";

export async function getDashboardSummary() {
  const response = await api.get(
    "/api/v1/dashboard/summary"
  );

  return response.data;
}