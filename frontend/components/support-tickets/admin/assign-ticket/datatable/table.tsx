"use client"

import { DataTable } from "@/components/ui/datatable"
import { AssignableAdmin } from "@/types/user"
import { columns } from "./columns"
import { features } from "./features"

export function AssignTicketAdminTable({ data }: { data: AssignableAdmin[] }) {
  return <DataTable features={features} columns={columns} data={data} />
}
