import { CircleAlert, OctagonAlert, ShieldAlert, SignalHigh, SignalLow, SignalMedium } from "lucide-react"

import { cn } from "@/lib/utils"
import { SupportTicket } from "@/types/support-ticket"

type Priority = NonNullable<SupportTicket["priority"]>

const PRIORITY_CONFIG: Record<Priority, { label: string; icon: typeof SignalLow; className: string }> = {
    
  low: { label: "Low", icon: OctagonAlert, className: "bg-blue/10 text-blue" },
  moderate: { label: "Moderate", icon:ShieldAlert, className: "bg-warning/10 text-warning" },
  high: { label: "High", icon: CircleAlert, className: "bg-error/10 text-error" },
}

export default function PriorityBadge({ priority }: { priority?: Priority }) {
  if (!priority) return null

  const { label, icon: Icon, className } = PRIORITY_CONFIG[priority]

  return (
    <span className={cn("inline-flex w-fit items-center gap-1 rounded-full px-2 text-xs font-medium", className)}>
      <Icon className="size-3" />
      {label}
    </span>
  )
}
