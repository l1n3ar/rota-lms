import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Separator } from '@/components/ui/separator'
import { SupportTicket } from '@/types/support-ticket'
import { AssignTicketAdminTable } from './datatable/table'
import { mockAssignableAdmins } from '@/data/mock/user'

interface AssignTicketDialogProps {
  ticket: SupportTicket
  open: boolean
  onOpenChange: (open: boolean) => void
}

const AssignTicketDialog = ({ ticket, open, onOpenChange }: AssignTicketDialogProps) => {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader >
          <DialogTitle>Assign ticket</DialogTitle>
          <Separator />
        </DialogHeader>

          <AssignTicketAdminTable data={mockAssignableAdmins}/>
      </DialogContent>
    </Dialog>
  )
}

export default AssignTicketDialog