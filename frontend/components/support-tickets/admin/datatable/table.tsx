"use client"

import { DataTable } from "@/components/ui/datatable"
import { SupportTicket } from "@/types/support-ticket"
import { columns } from "./columns"
import { features } from "./features"

export function SupportTicketsTable({ data }: { data: SupportTicket[] }) {
  return <DataTable features={features} columns={columns} data={data} />
}
