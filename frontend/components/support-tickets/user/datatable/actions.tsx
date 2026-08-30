"use client"

import { useState } from "react"

import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { Button } from "@/components/ui/button"

import { SupportTicket } from "@/types/support-ticket"
import CommentOnTicketDialog from "../../comment-on-ticket-dialog"
import { ArrowRight } from "lucide-react"


export function UserTicketActionsCell({ ticket }: { ticket: SupportTicket }) {


    const [commentDialogOpen, setCommentDialogOpen] = useState(false)



    const handleAddComment = () => {
        setCommentDialogOpen(true)
    }

    return (
        <>
            <div className="flex items-center text-muted-foreground">

                <Tooltip>
                    <TooltipTrigger render={
                        <Button variant="ghost" size='icon-sm' onClick={handleAddComment}>
                            <ArrowRight className="size-3.5" />
                        </Button>
                    }
                    />
                    <TooltipContent>
                        <p>Go to ticket</p>
                    </TooltipContent>
                </Tooltip>

            </div>

            <CommentOnTicketDialog
                ticket={ticket}
                open={commentDialogOpen}
                onOpenChange={setCommentDialogOpen}
            />

        </>
    )
}
