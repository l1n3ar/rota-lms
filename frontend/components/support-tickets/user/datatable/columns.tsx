import { createColumnHelper } from "@tanstack/react-table";
import { DataTableFeatures } from "../../admin/datatable/features";
import { SupportTicket } from "@/types/support-ticket";
import dateFormat from "dateformat";
import { IconBadge } from "@/components/ui/icon-badge";
import { PRIORITY_CONFIG, TICKET_STATUS_CONFIG } from "../../config";
import { UserTicketActionsCell } from "./actions";

const columnHelper = createColumnHelper<DataTableFeatures, SupportTicket>()

export const columns = columnHelper.columns([
    columnHelper.accessor("id", {
        header: "Ticket ID",
        cell: (info) => {
            return (
                <div className="flex flex-col">
                    <span>{info.getValue()}</span>
                    <span className="text-xs text-muted-foreground">{dateFormat(new Date(info.row.original.created_at), 'mmmm d, yyyy')} </span>
                </div>
            )
        }
    }),
    columnHelper.accessor("category", {
        header: "Category",
        cell: (info) => {
            return (
                <div className="flex flex-col">
                    <span>{info.getValue()}</span>
                  
                    {info.row.original.priority && <IconBadge {...PRIORITY_CONFIG[info.row.original.priority]} />}
                </div>
            )
        }
    }),
    columnHelper.accessor("subject", {
        header: "Subject",
        cell: (info) => {
            return (
                <div className="flex flex-col gap-1">
                    <span>{info.getValue()}</span>
                    {info.row.original.priority && <IconBadge {...TICKET_STATUS_CONFIG[info.row.original.status]} />}
                </div>

            )
        }
    }),

    columnHelper.display({
        id: "actions",
        // header: "Actions",
        cell: (info) => <UserTicketActionsCell ticket={info.row.original} />,
    }),
])