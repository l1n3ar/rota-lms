const TICKET_ROUTE_PREFIX = '/ticket'

export const TICKET_ENDPOINTS = {

    GET_ALL_TICKETS: { method: 'GET', path: `${TICKET_ROUTE_PREFIX}/`, requiresAuth: true },

    GET_TICKET_BY_ID: {
        method: 'GET',
        path: (params: { ticket_id: string }) => `${TICKET_ROUTE_PREFIX}/${params.ticket_id}/`,
        requiresAuth: true,
    },

    ADD_COMMENT_TO_TICKET: {
        method: 'POST',
        path: (params: { ticket_id: string }) => `${TICKET_ROUTE_PREFIX}/${params.ticket_id}/comment/`,
        requiresAuth: true,
    },

    CREATE_TICKET: { method: 'POST', path: `${TICKET_ROUTE_PREFIX}/create/`, requiresAuth: true },

} as const
