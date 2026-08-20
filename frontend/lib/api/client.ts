

import axios, { AxiosRequestConfig } from "axios";
import { ApiEndpoint, ApiResponse } from "@/types/api";
import { getCookie } from "@/actions/auth";

export class ApiClient {

    private baseURL: string;

    constructor() {
        this.baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || ''
    }


    async call<
        TPathParams extends Record<string, string | number> = Record<string, never>,
        TQueryParams extends Record<string, any> = Record<string, never>
    >(
        endpoint: ApiEndpoint<TPathParams, TQueryParams>,
        options?: {
            pathParams?: TPathParams
            queryParams?: TQueryParams
            body?: any
        }
    ): Promise<ApiResponse> {

        const token = await getCookie('access_token') //assuming we are gonna be storing it in cookies

        if (endpoint.requiresAuth && !token) {
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
            headers: token ? { Authorization: `Bearer ${token}` } : undefined,
        }

        try {
            const response = await axios.request<ApiResponse>(config)
            return { ...response.data, status: response.status }
        } catch (err) {
            if (axios.isAxiosError(err) && err.response) {
                return { ...err.response.data, status: err.response.status }
            }
            throw err
        }
    }
}

