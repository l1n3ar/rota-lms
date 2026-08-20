import { ApiEndpoint } from "@/types/api";
import { AUTH_ENDPOINTS } from "./auth";

export const ENDPOINTS : Record<string, Record<string, ApiEndpoint>> = {
    AUTH : {...AUTH_ENDPOINTS}
}