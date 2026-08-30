'use client'

import { useState } from 'react'

import CreateTicketDialog from '@/components/support-tickets/user/create-ticket-dialog'
import { Button } from '@/components/ui/button'
import { ArrowRight } from 'lucide-react'

import { mockSupportTickets } from '@/data/mock/support-ticket'
import TicketTopBar from '@/components/support-tickets/tickets-top-bar'
import { UserSupportTicketsTable } from '@/components/support-tickets/user/datatable/table'
import { SupportTicket } from '@/types/support-ticket'


const UserSupportPage = () => {
    const [isCreateTicketOpen, setIsCreateTicketOpen] = useState(false)
    const data : SupportTicket[] = mockSupportTickets //set to empty array to see empty state
 
    return (
        <>
            <div className='flex w-full gap-4 h-full'>

                <div id='text-section' className='w-1/3 flex flex-col gap-4 justify-between' >

                    {/* <span className='text-xs'>How can we help?</span> */}
                    <div className='max-w-[20rem] flex flex-col leading-0'>
                        <span className='text-3xl'>Have a question? </span>
                        <span className='text-3xl text-muted-foreground'>We’ve probably answered it here. If not, our support team is just a </span>
                        <span className='text-3xl'>ticket away.</span>

                    </div>

                    <Button className='rounded-full w-fit' onClick={() => setIsCreateTicketOpen(true)}>
                        Create Support Ticket
                        <ArrowRight />
                    </Button>
                </div>

                <div id='table-section' className='w-2/3 flex flex-col gap-4 p-4 rounded-2xl border'>
                    <TicketTopBar onClick={() => setIsCreateTicketOpen(true)} />

                    <UserSupportTicketsTable data={data} />

                </div>
            </div>

            <CreateTicketDialog open={isCreateTicketOpen} onOpenChange={setIsCreateTicketOpen} />
        </>

    )
}

export default UserSupportPage