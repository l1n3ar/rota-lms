'use server'

import { COOKIE_KEYS } from "@/types/auth"
import { cookies } from "next/headers"
import { logger } from "@/lib/logger"

export const getCookie = async (key: COOKIE_KEYS) => {
    const cookieStore = await cookies()
    return cookieStore.get(key)?.value || null
}

export const logRequest = async (details: {
    method?: string
    url?: string
    headers?: Record<string, any>
    pathParams?: Record<string, any>
    queryParams?: Record<string, any>
    body?: any
}) => {
    logger.debug(details, "API request")
}

export const logResponse = async (details: {
    method?: string
    url?: string
    status?: number
    data?: any
}) => {
    logger.debug(details, "API response")
}

export const logError = async (details: {
    method?: string
    url?: string
    status?: number
    data?: any
    message?: string
}) => {
    logger.error(details, "API error")
}