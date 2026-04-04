import axios from "axios";
import { generateRandomString } from "./index";
import i18n from '@/i18n'

const t = (key: string) => i18n.global.t(key)

// API基础URL - 生产环境使用相对路径，开发环境使用localhost
const BASE_URL = import.meta.env.DEV ? "http://localhost:8080" : "";

const instance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
    "X-Request-ID": `${generateRandomString(12)}`,
  },
});

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('weknora_token');
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    config.headers["X-Request-ID"] = `${generateRandomString(12)}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default instance;
