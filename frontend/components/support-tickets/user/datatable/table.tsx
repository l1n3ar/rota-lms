import { DataTable } from "@/components/ui/datatable";

import { features } from "../../admin/datatable/features";
import { columns } from './columns'
import { SupportTicket } from "@/types/support-ticket";

import empty from '@/public/empty.png'
import Image from "next/image";


export function UserSupportTicketsTable({ data }: { data: SupportTicket[] }) {

  if (data.length === 0) {
    return <div className="w-full h-full bg-neutral-50 p-8x flex flex-col items-center justify-center rounded-2xl">
      <Image src={empty} alt='empty' />
      <div className="flex flex-col gap-2x items-center">
        <span className="text-xl">There are no tickets available for display.</span>
        <span className="text-muted-foreground">If you need support, you can create a new ticket and chat with the support team.</span>
      </div>
    </div>
  }

  return <DataTable features={features} columns={columns} data={data} />
}