import { SupportTicket } from '@/types/support-ticket'
import { IconBadge } from '@/components/ui/icon-badge'
import { PRIORITY_CONFIG, TICKET_STATUS_CONFIG } from './config'
import SupportTicketHeaderCard from './support-ticket-header-card'

interface SupportTicketHeaderProps {
    ticket: SupportTicket
}

const SupportTicketHeader = ({ ticket }: SupportTicketHeaderProps) => {
    return (
        <div className='flex flex-col gap-4'>
            <div id='header'>
                <span className='text-lg'>Support Tickets</span>
            </div>

            <div id='ticket-details' className='grid grid-cols-3 grid-rows-2 gap-4 bg-muted p-4 rounded-xl'>
                <SupportTicketHeaderCard title='Ticket ID' content={ticket.id} />
                <SupportTicketHeaderCard title='Category' content={ticket.category} />
                <SupportTicketHeaderCard
                    title='Priority'
                    content={ticket.priority ? <IconBadge {...PRIORITY_CONFIG[ticket.priority]} /> : null}
                />
                <SupportTicketHeaderCard title='Subject' content={ticket.subject} className='col-span-2' />
                <SupportTicketHeaderCard
                    title='Status'
                    content={ticket.status ? <IconBadge {...TICKET_STATUS_CONFIG[ticket.status]} /> : null}
                />
            </div>

        </div>
    )
}

export default SupportTicketHeader
