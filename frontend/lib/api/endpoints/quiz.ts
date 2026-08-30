const QUIZ_ROUTE_PREFIX = '/quiz'

export const QUIZ_ENDPOINTS = {

    GET_ALL_QUIZZES: { method: 'GET', path: `${QUIZ_ROUTE_PREFIX}/quizzes/`, requiresAuth: true },

    CREATE_QUIZ: { method: 'POST', path: `${QUIZ_ROUTE_PREFIX}/quizzes/`, requiresAuth: true },

    GET_QUIZ_BY_ID: {
        method: 'GET',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/quizzes/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_QUIZ_FULL: {
        method: 'PUT',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/quizzes/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_QUIZ_PARTIAL: {
        method: 'PATCH',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/quizzes/${params.id}/`,
        requiresAuth: true,
    },

    DELETE_QUIZ: {
        method: 'DELETE',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/quizzes/${params.id}/`,
        requiresAuth: true,
    },

    GET_ALL_QUESTIONS: { method: 'GET', path: `${QUIZ_ROUTE_PREFIX}/questions/`, requiresAuth: true },

    CREATE_QUESTION: { method: 'POST', path: `${QUIZ_ROUTE_PREFIX}/questions/`, requiresAuth: true },

    GET_QUESTION_BY_ID: {
        method: 'GET',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/questions/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_QUESTION_FULL: {
        method: 'PUT',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/questions/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_QUESTION_PARTIAL: {
        method: 'PATCH',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/questions/${params.id}/`,
        requiresAuth: true,
    },

    DELETE_QUESTION: {
        method: 'DELETE',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/questions/${params.id}/`,
        requiresAuth: true,
    },

    GET_ALL_ANSWERS: { method: 'GET', path: `${QUIZ_ROUTE_PREFIX}/answers/`, requiresAuth: true },

    CREATE_ANSWER: { method: 'POST', path: `${QUIZ_ROUTE_PREFIX}/answers/`, requiresAuth: true },

    GET_ANSWER_BY_ID: {
        method: 'GET',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/answers/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_ANSWER_FULL: {
        method: 'PUT',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/answers/${params.id}/`,
        requiresAuth: true,
    },

    UPDATE_ANSWER_PARTIAL: {
        method: 'PATCH',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/answers/${params.id}/`,
        requiresAuth: true,
    },

    DELETE_ANSWER: {
        method: 'DELETE',
        path: (params: { id: number }) => `${QUIZ_ROUTE_PREFIX}/answers/${params.id}/`,
        requiresAuth: true,
    },

} as const
