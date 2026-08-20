export interface ApiEndpoint<
    TPathParams extends Record<string, string | number> = Record<string, never>,
    TQueryParams extends Record<string, any> = Record<string, never>
> {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
    path: string | ((params: TPathParams) => string);
    requiresAuth?: boolean; //mostly will be true all the time
}

export interface ApiResponse {
    success: boolean;
    data: any
    client_msg?: string // might not need to show all the time 
    dev_msg?: string // prolly use it only for dev
    status? : number

}