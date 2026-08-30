const COURSE_ROUTE_PREFIX = '/course'

export const COURSE_ENDPOINTS = {

    GET_ALL_COURSES: { method: 'GET', path: `${COURSE_ROUTE_PREFIX}/list/`, requiresAuth: false },

    GET_COURSES_BY_CATEGORY: {
        method: 'GET',
        path: (params: { category_id: number }) => `${COURSE_ROUTE_PREFIX}/list/${params.category_id}/`,
        requiresAuth: false,
    },

    GET_ALL_CATEGORIES: { method: 'GET', path: `${COURSE_ROUTE_PREFIX}/cat/`, requiresAuth: false },

    CREATE_CATEGORY: { method: 'POST', path: `${COURSE_ROUTE_PREFIX}/cat/`, requiresAuth: true },

    GET_CATEGORY_BY_ID: {
        method: 'GET',
        path: (params: { id: number }) => `${COURSE_ROUTE_PREFIX}/cat/${params.id}/`,
        requiresAuth: false,
    },

    UPDATE_CATEGORY_FULL: {
        method: 'PUT',
        path: (params: { id: number }) => `${COURSE_ROUTE_PREFIX}/cat/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_CATEGORY_PARTIAL: {
        method: 'PATCH',
        path: (params: { id: number }) => `${COURSE_ROUTE_PREFIX}/cat/${params.id}/`,
        requiresAuth: true,
    },

    DELETE_CATEGORY: {
        method: 'DELETE',
        path: (params: { id: number }) => `${COURSE_ROUTE_PREFIX}/cat/${params.id}/`,
        requiresAuth: true,
    },

} as const
