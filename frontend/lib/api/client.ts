

import axios, { AxiosRequestConfig } from "axios";
import { ApiEndpoint, ApiResponse } from "@/types/api";
import { getCookie, logError, logRequest, logResponse } from "./utils";
export class ApiClient {

    private baseURL: string;

    constructor() {
        this.baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || ''
    }


    async call<
        TPathParams extends Record<string, string | number>
    >(
        endpoint: ApiEndpoint<TPathParams>,
        options?: {
            pathParams?: TPathParams
            queryParams?: Record<string, unknown>
            body?: Record<string, unknown>
        }
    ): Promise<ApiResponse> {

        const accessToken = await getCookie('access_token') //assuming we are gonna be storing it in cookies

        if (endpoint.requiresAuth && !accessToken) {
            //need an err handler or reroute to login here
        }

        const path = typeof endpoint.path === 'function'
            ? endpoint.path(options?.pathParams as TPathParams)
            : endpoint.path

        const config: AxiosRequestConfig = {
            baseURL: this.baseURL,
            url: path,
            method: endpoint.method,
            params: options?.queryParams,
            data: options?.body,
            headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
        }

        try {

            logRequest(config)

            const response = await axios.request<ApiResponse>(config)

            logResponse(response)

            return { ...response.data, status: response.status }

        } catch (err) {
            logError(err)

            if (axios.isAxiosError(err) && err.response) {
                return { ...err.response.data, status: err.response.status }
            }
            throw err
        }
    }
}

