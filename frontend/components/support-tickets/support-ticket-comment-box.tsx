import { SupportTicket } from '@/types/support-ticket'
import React from 'react'
import { InputGroup } from '../ui/input-group'

interface SupportTicketCommentBoxProps {
    ticket: SupportTicket
}

const SupportTicketCommentBox = ({ ticket }: SupportTicketCommentBoxProps) => {
    return (
        <div>
            <div className='bg- rounded-t-lg rounded-b-none px-4 py-1'>Yo</div>
            <InputGroup className='rounded-t-none rounded-b-lg'>

            </InputGroup>
        </div>

    )
}

export default SupportTicketCommentBox