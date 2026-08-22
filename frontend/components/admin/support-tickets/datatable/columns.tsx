"use client"

import { createColumnHelper } from "@tanstack/react-table"

import { type DataTableFeatures } from './features'
import { SupportTicket } from "@/types/support-ticket"
import { TicketActionsCell } from "./actions"

const columnHelper = createColumnHelper<DataTableFeatures, SupportTicket>()

export const columns = columnHelper.columns([
  columnHelper.accessor("id", {
    header: "Ticket ID",
  }),
  columnHelper.accessor("category", {
    header: "Category",
  }),
  columnHelper.accessor("subject", {
    header: "Subject",
  }),
  columnHelper.accessor(
    (row) => `${row.created_by.first_name} ${row.created_by.last_name}`,
    { id: "created_by", header: "Created By" }
  ),
  columnHelper.accessor(
    (row) => `${row.assignee.first_name} ${row.assignee.last_name}`,
    { id: "assignee", header: "Assignee" }
  ),
  columnHelper.accessor("created_at", {
    header: "Created At",
    cell: (info) => new Date(info.getValue()).toLocaleDateString(),
  }),
  columnHelper.display({
    id: "actions",
    header: "Actions",
    cell: (info) => <TicketActionsCell ticket={info.row.original} />,
  }),
])
