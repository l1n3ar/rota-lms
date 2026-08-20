import { ApiEndpoint } from "@/types/api"

const AUTH_ROUTE_PREFIX = '/auth'

export const AUTH_ENDPOINTS = {

    GET_CURRENT_USER_PROFILE: { method: 'GET', path: `${AUTH_ROUTE_PREFIX}/me`, requiresAuth: true },

    UPDATE_PROFILE_FULL: { method: 'PUT', path: `${AUTH_ROUTE_PREFIX}/me`, requiresAuth: true },

    UPDATE_PROFILE_PARTIAL: { method: 'PATCH', path: `${AUTH_ROUTE_PREFIX}/me`, requiresAuth: true },  //complete onboardingg

    REQUEST_OTP: { method: 'POST', path: `${AUTH_ROUTE_PREFIX}/otp/request`, requiresAuth: false },

    VERIFY_OTP: { method: 'POST', path: `${AUTH_ROUTE_PREFIX}/otp/verify`, requiresAuth: false },

    REFRESH_TOKEN: { method: 'POST', path: `${AUTH_ROUTE_PREFIX}/token/refresh`, requiresAuth: false },
}




