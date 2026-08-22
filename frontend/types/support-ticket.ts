import { User } from "./user";

export type SupportTicket = {
    id: string,
    created_by: User,
    category: string,
    subject: string,
    priority? : 'low' | 'moderate' | 'high'
    assignee: User,
    created_at: Date,
    updated_at: Date,
}