"use client"

import { useState } from "react"

import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { Button } from "@/components/ui/button"

import { SupportTicket } from "@/types/support-ticket"
import { MessagesSquare, UserPlus } from "lucide-react"
import AssignTicketDialog from "../assign-ticket/assign-ticket-dialog"



export function TicketActionsCell({ ticket }: { ticket: SupportTicket }) {

  const [assignDialogOpen, setAssignDialogOpen] = useState(false)

  const handleAssignment = () => {
    setAssignDialogOpen(true)
  }

  const handleAddComment = () => {

  }

  return (
    <>
      <div className="flex items-center text-muted-foreground">
        <Tooltip>
          <TooltipTrigger render={
            <Button variant="ghost" size='icon-sm' onClick={handleAssignment}>
              <UserPlus className="size-3.5" />
            </Button>
          }
          />
          <TooltipContent>
            <p>Assign</p>
          </TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger render={
            <Button variant="ghost" size='icon-sm' onClick={handleAddComment}>
              <MessagesSquare className="size-3.5" />
            </Button>
          }
          />
          <TooltipContent>
            <p>Add comment</p>
          </TooltipContent>
        </Tooltip>

      </div>

      <AssignTicketDialog
        ticket={ticket}
        open={assignDialogOpen}
        onOpenChange={setAssignDialogOpen}
      />
    </>
  )
}
