"use client"

import { useState } from "react"

import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Separator } from "@/components/ui/separator"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { SupportTicket } from "@/types/support-ticket"
import SupportTicketHeader from "../support-ticket-header"

interface CommentOnTicketDialogProps {
  ticket: SupportTicket
  open: boolean
  onOpenChange: (open: boolean) => void
}

const CommentOnTicketDialog = ({ ticket, open, onOpenChange }: CommentOnTicketDialogProps) => {


  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent size="3xl">
        <DialogHeader>
          <SupportTicketHeader ticket={ticket} />
          <Separator className="mt-2" />
        </DialogHeader>


      </DialogContent>
    </Dialog>
  )
}

export default CommentOnTicketDialog
