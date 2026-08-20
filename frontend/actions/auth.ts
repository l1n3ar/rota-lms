'use server'

import { api } from "@/lib/api"
import { ENDPOINTS } from "@/lib/api/endpoints"
import { COOKIE_KEYS } from "@/types/auth"
import { cookies } from "next/headers"

export const getCookie = async (key: COOKIE_KEYS) => {
    const cookieStore = await cookies()
    return cookieStore.get(key)?.value || null
}

export const requestOTP = async (email: string) => {
    if (!email) return

    return await api.call(ENDPOINTS.AUTH.REQUEST_OTP, {
        body: {
            email
        }
    })
}
