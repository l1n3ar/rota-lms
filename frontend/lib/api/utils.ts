'use server'

import { COOKIE_KEYS } from "@/types/auth"
import { cookies } from "next/headers"
import { logger } from "@/lib/logger"
import axios, { AxiosRequestConfig, AxiosResponse } from "axios"

export const getCookie = async (key: COOKIE_KEYS) => {
    const cookieStore = await cookies()
    return cookieStore.get(key)?.value || null
}

export const logRequest = async (config: AxiosRequestConfig) => {
    logger.debug({
        method: config.method,
        url: config.url,
        headers: config.headers,
        queryParams: config.params,
        body: config.data,
    }, "API request")
}

export const logResponse = async (response: AxiosResponse) => {
    logger.debug({
        method: response.config?.method,
        url: response.config?.url,
        status: response.status,
        data: response.data,
    }, "API response")
}

export const logError = async (err: unknown) => {
    if (axios.isAxiosError(err)) {
        logger.error({
            method: err.config?.method,
            url: err.config?.url,
            status: err.response?.status,
            data: err.response?.data,
            message: err.message,
        }, "API error")
        return
    }

    logger.error({ message: err instanceof Error ? err.message : String(err) }, "API error")
}