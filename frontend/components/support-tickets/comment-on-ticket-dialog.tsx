"use client"



import { Dialog, DialogContent, DialogHeader } from "@/components/ui/dialog"
import { SupportTicket } from "@/types/support-ticket"
import SupportTicketHeader from "./support-ticket-header"
import SupportTicketContent from "./support-ticket-content"
import SupportTicketCommentBox from "./support-ticket-comment-box"


interface CommentOnTicketDialogProps {
  ticket: SupportTicket
  open: boolean
  onOpenChange: (open: boolean) => void
}

const CommentOnTicketDialog = ({ ticket, open, onOpenChange }: CommentOnTicketDialogProps) => {


  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent size="3xl">
        <DialogHeader className="mb-8x">
          <SupportTicketHeader ticket={ticket} />
          {/* <Separator className="mt-2" /> */}
        </DialogHeader>
        
        <SupportTicketContent ticket={ticket} />
        <SupportTicketCommentBox ticket={ticket} />
      </DialogContent>
    </Dialog>
  )
}

export default CommentOnTicketDialog
