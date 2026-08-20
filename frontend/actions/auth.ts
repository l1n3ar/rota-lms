'use server'

import { api } from "@/lib/api"
import { ENDPOINTS } from "@/lib/api/endpoints"

export const requestOTP = async (email: string) => {
    if (!email) return

    return await api.call(ENDPOINTS.AUTH.REQUEST_OTP, {
        body: {
            email
        }
    })
}
