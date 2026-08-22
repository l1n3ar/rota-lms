import { SupportTicketsTable } from '@/components/support-tickets/admin/datatable/table'
import { Button } from '@/components/ui/button'
import { InputGroup, InputGroupInput, InputGroupAddon } from '@/components/ui/input-group'
import { ListFilter, Search } from 'lucide-react'
import { mockSupportTickets } from '@/data/mock/support-ticket'


const AdminSupportTicketsPage = () => {


  return (
    <div className='h-full w-full flex flex-col gap-4'>

      <div id='section-heading' className='flex items-center justify-between'>
        <span className='text-lg font-medium'>Support Tickets</span>

        <div className='flex items-center gap-2'>

          <InputGroup className='bg-white p-4 flex w-[15rem]'>
            <InputGroupInput
              id="inline-end-input"
              placeholder="Ticket Search"
            />
            <InputGroupAddon align="inline-end">
              <Search />
            </InputGroupAddon>
          </InputGroup>

          <Button className='rounded-full p-4x shrink-0' size='icon-lg' variant='outline'><ListFilter /></Button>

        </div>
      </div>

      <div id='content'>
        <SupportTicketsTable data={mockSupportTickets} />
      </div>

    </div>
  )
}

export default AdminSupportTicketsPage