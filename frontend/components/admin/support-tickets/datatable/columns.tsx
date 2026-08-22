"use client"

import { createColumnHelper } from "@tanstack/react-table"
import dateFormat from 'dateformat'

import { type DataTableFeatures } from './features'
import { SupportTicket } from "@/types/support-ticket"
import { TicketActionsCell } from "./actions"



const columnHelper = createColumnHelper<DataTableFeatures, SupportTicket>()

export const columns = columnHelper.columns([
  columnHelper.accessor("id", {
    header: "Ticket ID",
    cell: (info) => {
      return (
        <div className="flex flex-col">
          <span>{info.getValue()}</span>
          <span className="text-xs text-muted-foreground">{info.row.original.created_by.first_name} {info.row.original.created_by.last_name}</span>
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
          <span className="text-xs text-muted-foreground">{dateFormat(new Date(info.row.original.created_at),'mmmm d, yyyy')} </span>
        </div>
      )
    }
  }),
  columnHelper.accessor("subject", {
    header: "Subject",
  }),
  columnHelper.accessor(
    (row) => `${row.assignee.first_name} ${row.assignee.last_name}`,
    { id: "assignee", header: "Assignee" }
  ),
  columnHelper.accessor('updated_at', {
    header: "Last Update",
    cell: (info) => {
      return (
        <div className="flex flex-col">
          <span>{dateFormat(new Date(info.getValue()),'mmmm d, yyyy')}</span>
          <span className="text-xs text-muted-foreground">{dateFormat(new Date(info.getValue()),'hh:mm')}</span>
        </div>
      )
    },
  }),
  columnHelper.display({
    id: "actions",
    header: "Actions",
    cell: (info) => <TicketActionsCell ticket={info.row.original} />,
  }),
])
