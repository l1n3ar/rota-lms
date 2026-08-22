import { Check,DotIcon,CircleAlert } from "lucide-react"

import { cn } from "@/lib/utils"
import { User } from "@/types/user";


type Status = NonNullable<User["status"]>

const STATUS_CONFIG: Record<Status, { label: string; icon: typeof Check; className: string }> = {
    
  online: { label: "Online", icon: Check, className: "bg-success/10 text-success" },
  away: { label: "Away", icon:CircleAlert, className: "bg-warning/10 text-warning" },
  offline: { label: "Offline", icon: DotIcon, className: "bg-muted text-muted-foreground" },
}

export default function UserStatusBadge({ status }: { status?: Status }) {
  if (!status) return null

  const { label, icon: Icon, className } = STATUS_CONFIG[status]

  return (
    <span className={cn("inline-flex w-fit items-center gap-1 rounded-full px-2 text-xs font-medium", className)}>
      <Icon className="size-3" />
      {label}
    </span>
  )
}
