import React from 'react'
import { Button } from '../ui/button'
import { TextAlignStart } from 'lucide-react'

const AdminTopBar = () => {
    return (
        <div className='w-full flex items-center justify-between'>

            <div className='flex items-center gap-4'>
                <Button className='rounded-full p-4x shrink-0' size='icon-lg' variant='outline'><TextAlignStart /></Button>
                <div className='flex flex-col'>
                    <span className='text-2xl'>Hello Hossein</span>
                    <span className='text-xs text-neutral-500'>Let's learn something new today!</span>

                </div>
            </div>

            <div className='flex items-center gap-2'>

            </div>

        </div>
    )
}

export default AdminTopBar

