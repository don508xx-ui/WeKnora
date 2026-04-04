import axios from "axios";

const generateID = (len: number) => {
  const chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678";
  let str = "";
  for (let i = 0; i < len; i++) str += chars.charAt(Math.floor(Math.random() * chars.length));
  return str;
};

const BASE_URL = "";

const instance = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
    "X-Request-ID": `${generateID(12)}`,
  },
});

instance.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  }
);

export function get(url: string) {
  return instance.get(url);
}

export async function getDown(url: string) {
  let res = await instance.get(url, {
    responseType: "blob",
  });
  return res
}

export function postUpload(url: string, data = {}, onUploadProgress?: (progressEvent: any) => void) {
  return instance.post(url, data, {
    headers: {
      "Content-Type": "multipart/form-data",
      "X-Request-ID": `${generateID(12)}`,
    },
    onUploadProgress,
  });
}

export function postChat(url: string, data = {}) {
  return instance.post(url, data, {
    headers: {
      "Content-Type": "text/event-stream;charset=utf-8",
      "X-Request-ID": `${generateID(12)}`,
    },
  });
}

export function post(url: string, data = {}, config?: any) {
  return instance.post(url, data, config);
}

export function put(url: string, data = {}) {
  return instance.put(url, data);
}

export function del(url: string, data?: any) {
  return instance.delete(url, { data });
}

export default instance;
