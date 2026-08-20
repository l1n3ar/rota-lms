import { AxiosRequestConfig } from "axios";
import { ENDPOINTS } from "./endpoints";

export const logRequest = (endpoint: keyof typeof ENDPOINTS, config: AxiosRequestConfig) => {
    console.log(`[API REQUEST] ${endpoint}`, {
        method: config.method,
        url: config.url,
        params: config.params,
        headers: config.headers,
        body: config.data,
    });
}

export const logResponse = (endpoint: keyof typeof ENDPOINTS, response: any) => {
    console.log(`[API RESPONSE] ${endpoint}`, {
        status: response.status,
        data: response.data
    });
}