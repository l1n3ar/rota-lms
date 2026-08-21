import React from 'react'
import { Button } from '../ui/button'
import { Bell, Search, Settings, TextAlignStart } from 'lucide-react'

import {
    InputGroup,
    InputGroupAddon,
    InputGroupInput,
} from "@/components/ui/input-group"

const AdminTopBar = () => {
    return (
        <div className='w-full flex items-center justify-between'>

            <div className='flex items-center gap-4'>
                <Button className='rounded-full p-4x shrink-0' size='icon-xl' variant='outline'><TextAlignStart /></Button>
                <div className='flex flex-col'>
                    <span className='text-2xl leading-none'>Hello Hossein</span>
                    <span className='text-xs text-neutral-500'>Let's learn something new today!</span>

                </div>
            </div>

            <div className='flex items-center gap-2'>
                <InputGroup className='bg-white p-6 flex w-[20rem]'>

                    <InputGroupInput
                        id="inline-end-input"
                        placeholder="Search from courses..."
                    />

                    <InputGroupAddon align="inline-end">
                        <Search />
                    </InputGroupAddon>

                </InputGroup>

                <Button className='rounded-full p-4x shrink-0' size='icon-xl' variant='outline'><Bell /></Button>
                <Button className='rounded-full p-4x shrink-0' size='icon-xl' variant='outline'><Settings /></Button>

            </div>

        </div>
    )
}

export default AdminTopBar

