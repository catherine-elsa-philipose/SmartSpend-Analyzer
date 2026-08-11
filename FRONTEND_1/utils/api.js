import axios from "axios";

const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:5000/api",
});

// ✅ Attach Authorization: Bearer <token> from localStorage
API.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ✅ LOGIN (POST /api/user_login)
export const loginUser = async (data) => {
  const res = await API.post("/user_login", data);
  return res.data;
};

// ✅ SIGNUP (POST /api/register)
export const registerUser = async (data) => {
  const res = await API.post("/register", data);
  return res.data;
};

// ✅ UPLOAD RECEIPT (POST /api/ocr)
export const uploadReceipt = async (file) => {
  const formData = new FormData();
  formData.append("image", file);
  const res = await API.post("/ocr", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return res.data;
};

// ✅ DASHBOARD DATA SCIENCE SUMMARY (GET /api/ds/summary)
export const getSpendingSummary = async () => {
  const res = await API.get("/ds/summary");
  return res.data;
};

// ✅ DASHBOARD DATA SCIENCE FORECAST (POST /api/ds/forecast)
export const getForecast = async (horizon = 6) => {
  const res = await API.post("/ds/forecast", { horizon });
  return res.data;
};

export default API;