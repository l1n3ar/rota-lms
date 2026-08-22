"use client"

import { createColumnHelper } from "@tanstack/react-table"

import { type DataTableFeatures } from './features'
import { AssignableAdmin, MapDBRoleToUserFacingRole, MapDBStatusToUserFacingStatus } from "@/types/user"
import { AdminActionsCell } from "./actions"

const columnHelper = createColumnHelper<DataTableFeatures, AssignableAdmin>()

export const columns = columnHelper.columns([
    columnHelper.accessor(
        (row) => `${row.first_name} ${row.last_name}`,
        {
            id: "admin_name",
            header: "Admin Name",
            cell: (info) => {

                const adminName = `${info.row.original.first_name} ${info.row.original.last_name}`

                return (
                    <div className="flex flex-col">
                        <span>{adminName}</span>
                        <span className="text-xs text-muted-foreground tracking-tight">{MapDBRoleToUserFacingRole[info.row.original.role]}</span>

                    </div>
                )
            }
        }

    ),
    columnHelper.accessor("status", {
        header: "Status",
        cell: (info) => {
            return (
                <span>{MapDBStatusToUserFacingStatus[info.getValue()]}</span>
            )
        }
    }),
    columnHelper.accessor("open_tickets", {
        header: "Open Tickets",
    }),
    columnHelper.display({
        id: "actions",
        header: "Action",
        cell: (info) => <AdminActionsCell admin={info.row.original} />,
    }),
])
