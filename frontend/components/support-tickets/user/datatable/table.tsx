import { DataTable } from "@/components/ui/datatable";

import { features } from "../../admin/datatable/features";
import {columns} from './columns'
import { SupportTicket } from "@/types/support-ticket";

export function UserSupportTicketsTable({ data }: { data: SupportTicket[] }) {
  return <DataTable features={features} columns={columns} data={data} />
}