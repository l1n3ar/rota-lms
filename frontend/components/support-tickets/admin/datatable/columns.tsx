"use client"

import { createColumnHelper } from "@tanstack/react-table"
import dateFormat from 'dateformat'

import { type DataTableFeatures } from './features'
import { SupportTicket } from "@/types/support-ticket"
import { TicketActionsCell } from "./actions"
import { IconBadge } from "@/components/ui/icon-badge"
import { PRIORITY_CONFIG } from "../../config"
import { MapDBRoleToUserFacingRole } from "@/types/user"

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
          <span className="text-xs text-muted-foreground">{dateFormat(new Date(info.row.original.created_at), 'mmmm d, yyyy')} </span>
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
          {info.row.original.priority && <IconBadge {...PRIORITY_CONFIG[info.row.original.priority]} />}
        </div>

      )
    }
  }),
  columnHelper.accessor(
    (row) => `${row.assignee?.first_name} ${row.assignee?.last_name}`,
    {
      id: "assignee",
      header: "Assignee",
      cell: (info) => {

        const assigneeName = info.row.original.assignee ? `${info.row.original.assignee?.first_name} ${info.row.original.assignee?.last_name}` : 'None'
        const assigneeRole = info.row.original.assignee ? `${MapDBRoleToUserFacingRole[info.row.original.assignee.role]}` : ''

        return (
          <div className="flex flex-col">
            <span>{assigneeName}</span>
            <span className="text-xs text-muted-foreground">{assigneeRole}</span>
          </div>

        )
      }
    }

  ),
  columnHelper.accessor('updated_at', {
    header: "Last Update",
    cell: (info) => {
      return (
        <div className="flex flex-col">
          <span>{dateFormat(new Date(info.getValue()), 'mmmm d, yyyy')}</span>
          <span className="text-xs text-muted-foreground">{dateFormat(new Date(info.getValue()), 'hh:mm')}</span>
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
