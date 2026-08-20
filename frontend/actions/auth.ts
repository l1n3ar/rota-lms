'use server'

import { cookies } from "next/headers"

export const getAuthTokenFromCookies = async () => {
    const cookieStore = await cookies()
    return cookieStore.get("access_token")?.value || null
}