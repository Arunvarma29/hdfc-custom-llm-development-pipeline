import api from "./api";

export async function getDatasets(params = {}) {
  const response = await api.get("/api/v1/datasets", {
    params,
  });

  return response.data;
}

export async function createDataset(formData) {
  const response = await api.post(
    "/api/v1/datasets",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export async function deleteDataset(datasetId) {
  await api.delete(`/api/v1/datasets/${datasetId}`);
}

// -----------------------------------------
// Dataset Governance APIs
// -----------------------------------------

export async function prepareDataset(datasetId) {
  const response = await api.post(
    `/api/v1/datasets/${datasetId}/prepare`
  );

  return response.data;
}

export async function getPreparationStatus(datasetId) {
  const response = await api.get(
    `/api/v1/datasets/${datasetId}/preparation`
  );

  return response.data;
}



export async function approveDataset(
  datasetId,
  review = {}
) {
  const response = await api.post(
    `/api/v1/datasets/${datasetId}/approve`,
    review
  );

  return response.data;
}


export async function rejectDataset(
  datasetId,
  review = {}
) {
  const response = await api.post(
    `/api/v1/datasets/${datasetId}/reject`,
    review
  );

  return response.data;
}



export async function getQualityReport(datasetId) {
  const response = await api.get(
    `/api/v1/datasets/${datasetId}/quality`
  );

  return response.data;
}



export async function getPreparedArtifact(datasetId) {
  const response = await api.get(
    `/api/v1/datasets/${datasetId}/artifact`
  );

  return response.data;
}



export async function runPreparation(datasetId) {
  const response = await api.post(
    `/api/v1/datasets/${datasetId}/preparation/run`
  );

  return response.data;
}


export async function runQualityCheck(datasetId) {
  const response = await api.post(
    `/api/v1/datasets/${datasetId}/quality/run`
  );

  return response.data;
}