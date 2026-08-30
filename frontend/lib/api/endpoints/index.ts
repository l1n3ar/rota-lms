import { AUTH_ENDPOINTS } from "./auth";
import { TICKET_ENDPOINTS } from "./tickets";
import { COURSE_ENDPOINTS } from "./course";
import { QUIZ_ENDPOINTS } from "./quiz";
import { CERTIFICATE_ENDPOINTS } from "./certificate";

export const ENDPOINTS  = {
    AUTH : {...AUTH_ENDPOINTS},
    TICKET : {...TICKET_ENDPOINTS},
    COURSE : {...COURSE_ENDPOINTS},
    QUIZ : {...QUIZ_ENDPOINTS},
    CERTIFICATE : {...CERTIFICATE_ENDPOINTS}
}