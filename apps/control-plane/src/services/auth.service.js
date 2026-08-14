import api from "./api";
import { getAuthToken } from "./auth.storage";

export async function signupUser(payload) {
  const response = await api.post(
    "/api/v1/auth/signup",
    payload
  );

  return response.data;
}

export async function loginUser(payload) {
  const response = await api.post(
    "/api/v1/auth/login",
    payload
  );

  return response.data;
}

export async function getCurrentUser() {
  const token = getAuthToken();

  if (!token) {
    throw new Error("No authentication token found.");
  }

  const response = await api.get(
    "/api/v1/auth/me",
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
}