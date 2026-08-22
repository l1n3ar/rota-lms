export type USER_STATUS = 'online' | 'away' | 'offline'
export type USER_ROLE = 'user' | 'lecturer' | 'superuser'

export type User = {
    first_name: string,
    last_name: string,
    created_at: Date,
    updated_at: Date,
    role: USER_ROLE,
    status: USER_STATUS
}

export type AssignableAdmin = User & {
    open_tickets: number
}

export enum MapDBRoleToUserFacingRole {
    user = 'User',
    lecturer = 'Lecturer',
    superuser = 'Admin'
}

export enum MapDBStatusToUserFacingStatus {
    online = 'Online',
    away = 'Away',
    offline = 'Offline'
}