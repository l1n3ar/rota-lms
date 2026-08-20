'use server'

import { COOKIE_KEYS } from "@/types/auth"
import { cookies } from "next/headers"


export const getCookie = async (key : COOKIE_KEYS) => {
    const cookieStore = await cookies()
    return cookieStore.get(key)?.value || null
}
