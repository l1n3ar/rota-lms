import axios, { AxiosRequestConfig } from "axios";
import { ENDPOINTS } from "./endpoints";

class ApiClient {

    private baseURL: string;

    constructor() {
        this.baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || ''
    }

    private logRequest(endpoint: keyof typeof ENDPOINTS, config: AxiosRequestConfig) {
        console.log(`[API REQUEST] ${endpoint}`, {
            method: config.method,
            url: config.url,
            params: config.params,
            headers: config.headers,
            body: config.data,
        });
    }
}