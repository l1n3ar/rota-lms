export interface ApiEndpoint {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
    path: string;
    requiresAuth?: boolean; //mostly will be true all the time
}

export interface ApiResponse {
    success: boolean;
    data: any
    client_msg?: string // might not need to show all the time 
    dev_msg?: string // prolly use it only for dev

}