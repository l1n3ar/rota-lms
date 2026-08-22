"use client"

import { useRouter } from "next/navigation"

import { Button } from "@/components/ui/button"
import { SupportTicket } from "@/types/support-ticket"

export function TicketActionsCell({ ticket }: { ticket: SupportTicket }) {
  const router = useRouter()

  return (
    <Button size="sm" variant="outline" onClick={() => router.push(`/admin/support/${ticket.id}`)}>
      View
    </Button>
  )
}
