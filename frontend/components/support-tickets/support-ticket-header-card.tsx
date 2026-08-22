import { cn } from '@/lib/utils'
import { type LucideIcon } from 'lucide-react'
import React from 'react'

interface SupportTicketHeaderCardProps {
    title: string
    content: React.ReactNode | string
    icon?: LucideIcon
    className?: string
}

const SupportTicketHeaderCard = ({ title, content, className }: SupportTicketHeaderCardProps) => {

    
    return (
        <div className={cn('p-4 rounded-xl flex flex-col bg-card ', className)}>
            <span className='flex items-center gap-1 text-xs text-muted-foreground'>
                {/* <Icon className='size-3.5' /> */}
                {title}
            </span>
            {typeof content === 'string' ? <span>{content}</span> : content}
        </div>
    )
}

export default SupportTicketHeaderCard