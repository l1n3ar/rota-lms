import { cn } from '@/lib/utils'
import React from 'react'

interface SupportTicketHeaderCardProps {
    title: string
    content: React.ReactNode | string
    className? : string
}

const SupportTicketHeaderCard = ({ title, content,className }: SupportTicketHeaderCardProps) => {
    return (
        <div className={cn('p-4 rounded-xl flex flex-col bg-white ',className)}>
            <span className='text-xs text-muted-foreground'>{title}</span>
            {typeof content === 'string' ? <span>{content}</span> : content}
        </div>
    )
}

export default SupportTicketHeaderCard