import axios from "axios";

export type ApiResponse<T> = {
  message?: string;
  data: T;
  success: boolean;
};

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  timeout: 60000,
});

service.interceptors.response.use((response) => {
  return response.data;
});

export default service;
