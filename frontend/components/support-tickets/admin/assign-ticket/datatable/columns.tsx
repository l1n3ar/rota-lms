"use client"

import { createColumnHelper } from "@tanstack/react-table"

import { type DataTableFeatures } from './features'
import { AssignableAdmin, MapDBRoleToUserFacingRole } from "@/types/user"
import { AdminActionsCell } from "./actions"
import { IconBadge } from "@/components/ui/icon-badge"
import { USER_STATUS_CONFIG } from "@/components/user/config"

const columnHelper = createColumnHelper<DataTableFeatures, AssignableAdmin>()

export const columns = columnHelper.columns([
    columnHelper.accessor(
        (row) => `${row.first_name} ${row.last_name}`,
        {
            id: "admin_name",
            header: "Admin Name",
            cell: (info) => {

                const adminName = `${info.row.original.first_name} ${info.row.original.last_name }`

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
                <IconBadge {...USER_STATUS_CONFIG[info.getValue()]} />
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
