import { Filter, Plus, Search } from 'lucide-react'

import { InputGroup, InputGroupInput, InputGroupAddon } from '../ui/input-group'
import SearchInput from '../shared/search-input'
import { Button } from '../ui/button'

interface TicketTopBarProps{
    onClick : () => void
}

const TicketTopBar = ({
    onClick
} : TicketTopBarProps) => {
    return (
        <div className='w-full flex items-center justify-between'>

            <div className='text-xl'>
                Support Ticket
            </div>

            <div className='flex items-center gap-2'>
                <SearchInput placeholderText='Search Tickets...' className='p-4' />
                <Button variant='outline' className='rounded-full' size='icon-sm'>
                    <Filter />
                </Button>
                <Button className='rounded-full p-4' onClick={onClick}>
                    <Plus />
                    <span>New Ticket</span>
                </Button>
            </div>

        </div>
    )
}

export default TicketTopBar