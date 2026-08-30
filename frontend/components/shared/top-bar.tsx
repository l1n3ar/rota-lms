import React from 'react'
import { Button } from '../ui/button'
import { Bell, Search, Settings, TextAlignStart } from 'lucide-react'

import {
    InputGroup,
    InputGroupAddon,
    InputGroupInput,
} from "@/components/ui/input-group"
import SearchInput from './search-input'

const TopBar = () => {
    return (
        <div className='w-full flex items-center justify-between'>

            <div className='flex items-center gap-4'>
                <Button className='rounded-full p-4x shrink-0' size='icon-xl' variant='outline'><TextAlignStart /></Button>
                <div className='flex flex-col'>
                    <span className='text-2xl leading-none'>Hello Mehul 👋</span>
                    <span className='text-xs text-muted-foreground'>Let&apos;s learn something new today!</span>

                </div>
            </div>

            <div className='flex items-center gap-2'>
                <SearchInput placeholderText='Search from courses...' className='rounded-full'/>

                <Button className='rounded-full p-4x shrink-0' size='icon-xl' variant='outline'><Bell /></Button>
                <Button className='rounded-full p-4x shrink-0' size='icon-xl' variant='outline'><Settings /></Button>

            </div>

        </div>
    )
}

export default TopBar

