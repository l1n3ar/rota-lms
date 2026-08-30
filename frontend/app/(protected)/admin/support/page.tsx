import { SupportTicketsTable } from '@/components/support-tickets/admin/datatable/table'
import { mockSupportTickets } from '@/data/mock/support-ticket'
import TicketTopBar from '@/components/support-tickets/tickets-top-bar'


const AdminSupportTicketsPage = () => {


  return (
    <div className='h-full w-full flex flex-col gap-4'>

      <div id='section-heading' className='flex items-center justify-between'>
        <TicketTopBar isAdmin/>
      </div>

      <div id='content'>
        <SupportTicketsTable data={mockSupportTickets} />
      </div>

    </div>
  )
}

export default AdminSupportTicketsPage