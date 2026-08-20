import { AxiosRequestConfig } from "axios";
import { ApiEndpoint } from "@/types/api";

export const logRequest = (endpoint: ApiEndpoint, config: AxiosRequestConfig) => {
    console.log(`[API REQUEST] ${endpoint}`, {
        method: config.method,
        url: config.url,
        params: config.params,
        headers: config.headers,
        body: config.data,
    });
}

export const logResponse = (endpoint: ApiEndpoint, response: any) => {
    console.log(`[API RESPONSE] ${endpoint}`, {
        status: response.status,
        data: response.data
    });
}

export const logError = (endpoint: ApiEndpoint, error: any) =>  {
    console.log(`[API ERROR] ${endpoint}`, {
      status : error.status,
      message: error.message,
      stack: error.stack,
      response: error.response?.data,
    });
  }