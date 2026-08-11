import axios from "axios";

const API = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
});

// ✅ LOGIN
export const loginUser = async(data) => {
    const res = await API.post("/user_login", data);
    return res.data;
};

// ✅ SIGNUP
export const registerUser = async(data) => {
    const res = await API.post("/register", data);
    return res.data;
};

// ✅ DASHBOARD APIs (fix your current error)
export const getDashboard = async() => {
    const res = await API.get("/dashboard");
    return res.data;
};

export const getExpenses = async() => {
    const res = await API.get("/expenses");
    return res.data;
};

export const getCategories = async() => {
    const res = await API.get("/categories");
    return res.data;
};

export default API;