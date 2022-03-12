import axios, { AxiosInstance } from "axios";

const apiClient: AxiosInstance = axios.create({
    baseURL: location.href + 'json/',
    headers: {
        'Content-type': 'application/json',
    },
});
export default apiClient;
