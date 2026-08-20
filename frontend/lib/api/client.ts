

import { ApiEndpoint } from "@/types/api";
import { getCookie } from "@/actions/auth";

export class ApiClient {

    private baseURL: string;

    constructor() {
        this.baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || ''
    }


    async call(
        endpoint: ApiEndpoint,
        pathParams?: Record<string, any>,
        queryParams?: Record<string, any>,
        body?: any
    ) {

        const token = await getCookie('access_token') //assuming we are gonna be storing it in cookies

        if (endpoint.requiresAuth && !token){
            //raise err here
        }

        
    }
}

