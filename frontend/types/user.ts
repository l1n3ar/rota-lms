export type User = {
    first_name: string,
    last_name: string,
    created_at: Date,
    updated_at: Date,
    role: USER_ROLE
}

export type USER_ROLE = 'user' | 'lecturer' | 'superuser'

export enum MapDBRoleToUserFacingRole {
    user = 'User',
    lecturer = 'Lecturer',
    superuser = 'Admin'
}