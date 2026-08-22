'use client'

import { SupportTicket } from '@/types/support-ticket'
import React, { useState } from 'react'
import { InputGroup, InputGroupAddon, InputGroupButton, InputGroupInput } from '../ui/input-group'
import { Button } from '../ui/button'
import { ArrowUp, Paperclip, ReplyAll, Settings2, X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SupportTicketCommentBoxProps {
    ticket: SupportTicket
}

const SupportTicketCommentBox = ({ ticket }: SupportTicketCommentBoxProps) => {
    const [showSuggestion, setShowSuggestion] = useState(true)

    return (
        <div>

            <div
                className={cn(
                    'grid overflow-hidden transition-all duration-300 ease-in-out',
                    showSuggestion ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'
                )}
            >
                <div className='min-h-0 overflow-hidden'>
                    <div id='suggestions' className='w-full rounded-t-lg px-4 py-1 text-xs flex items-center justify-between gap-2 bg-foreground/5 hover:cursor-pointer hover:bg-foreground/10 transition-colors'>
                        <div className='flex items-center gap-2'>
                            <ReplyAll className='rotate-y-180 size-3' />
                           
                            <span className='text-xs'>//TODO</span>
                        </div>
                        <Button variant='ghost' size='icon-xs' onClick={() => setShowSuggestion(false)}>
                            <X />
                        </Button>
                    </div>
                </div>
            </div>

            <InputGroup className={cn('rounded-b-lg ', showSuggestion ? 'rounded-t-none border-t-0' : 'rounded-t-lg')}>
               <InputGroupInput placeholder="Add a comment..."  className='min-h-12 max-h-32'/>
                <InputGroupAddon align="block-end" className="pt-1">
                    <div className='flex items-center gap-2 justify-between w-full'>
                        <div className='flex items-center gap-2'>
                            <InputGroupButton size='icon-xs' variant='ghost' className='rounded-full'><Paperclip /></InputGroupButton>
                            <InputGroupButton size='icon-xs' variant='ghost' className='rounded-full'><Settings2 /></InputGroupButton>
                        </div>
                        <InputGroupButton size='icon-sm' variant='default' className='rounded-full'><ArrowUp /></InputGroupButton>
                        <span className="sr-only">Send</span>
                    </div>
                </InputGroupAddon>


            </InputGroup>
        </div>

    )
}

export default SupportTicketCommentBox
