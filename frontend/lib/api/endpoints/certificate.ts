const CERTIFICATE_ROUTE_PREFIX = '/certificate'

export const CERTIFICATE_ENDPOINTS = {

    GET_ALL_CERTIFICATES: { method: 'GET', path: `${CERTIFICATE_ROUTE_PREFIX}/certificates/`, requiresAuth: true },

    CREATE_CERTIFICATE: { method: 'POST', path: `${CERTIFICATE_ROUTE_PREFIX}/certificates/`, requiresAuth: true },

    GET_CERTIFICATE_BY_ID: {
        method: 'GET',
        path: (params: { id: number }) => `${CERTIFICATE_ROUTE_PREFIX}/certificates/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_CERTIFICATE_FULL: {
        method: 'PUT',
        path: (params: { id: number }) => `${CERTIFICATE_ROUTE_PREFIX}/certificates/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_CERTIFICATE_PARTIAL: {
        method: 'PATCH',
        path: (params: { id: number }) => `${CERTIFICATE_ROUTE_PREFIX}/certificates/${params.id}/`,
        requiresAuth: true,
    },

    DELETE_CERTIFICATE: {
        method: 'DELETE',
        path: (params: { id: number }) => `${CERTIFICATE_ROUTE_PREFIX}/certificates/${params.id}/`,
        requiresAuth: true,
    },

    GET_ALL_ISSUED_CERTIFICATES: { method: 'GET', path: `${CERTIFICATE_ROUTE_PREFIX}/issued/`, requiresAuth: true },

    ISSUE_CERTIFICATE: { method: 'POST', path: `${CERTIFICATE_ROUTE_PREFIX}/issued/`, requiresAuth: true },

    GET_ISSUED_CERTIFICATE_BY_ID: {
        method: 'GET',
        path: (params: { id: string }) => `${CERTIFICATE_ROUTE_PREFIX}/issued/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_ISSUED_CERTIFICATE_FULL: {
        method: 'PUT',
        path: (params: { id: string }) => `${CERTIFICATE_ROUTE_PREFIX}/issued/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_ISSUED_CERTIFICATE_PARTIAL: {
        method: 'PATCH',
        path: (params: { id: string }) => `${CERTIFICATE_ROUTE_PREFIX}/issued/${params.id}/`,
        requiresAuth: true,
    },

    REVOKE_ISSUED_CERTIFICATE: {
        method: 'DELETE',
        path: (params: { id: string }) => `${CERTIFICATE_ROUTE_PREFIX}/issued/${params.id}/`,
        requiresAuth: true,
    },

    DOWNLOAD_ISSUED_CERTIFICATE_PDF: {
        method: 'GET',
        path: (params: { id: string }) => `${CERTIFICATE_ROUTE_PREFIX}/issued/${params.id}/pdf/`,
        requiresAuth: true,
    },

    GET_MY_ISSUED_CERTIFICATES: { method: 'GET', path: `${CERTIFICATE_ROUTE_PREFIX}/issued/my/`, requiresAuth: true },

} as const
