import { User } from "./user";

export type SUPPORT_TICKET_PRIORITY = 'low' | 'medium' | 'high'
export type SUPPORT_TICKET_STATUS = 'answered' | 'in_progress' | 'closed'

export type SupportTicketComment = {
    id: string,
    author: User,
    message: string,
    created_at: Date,
}

export type SupportTicket = {
    id: string,
    created_by: User,
    category: string,
    subject: string,
    priority? : SUPPORT_TICKET_PRIORITY
    status?: SUPPORT_TICKET_STATUS
    assignee?: User,
    comments?: SupportTicketComment[],

    created_at: Date,
    updated_at: Date,
}


export enum MapDBPriorityToUserFacingPriority {
    low = 'Low',
    medium = 'Medium',
    high = 'High'
}

export enum MapDBStatusToUserFacingStatus {
    answered = 'Answered',
    in_progress = 'In Progress',
    closed = 'Closed'
}
