import { CircleAlert, OctagonAlert, ShieldAlert,CircleCheck, Clock, Check  } from "lucide-react"

export const PRIORITY_CONFIG = {
  low: { label: "Low", icon: OctagonAlert, className: "bg-blue/10 text-blue" },
  medium: { label: "Medium", icon: ShieldAlert, className: "bg-warning/10 text-warning" },
  high: { label: "High", icon: CircleAlert, className: "bg-error/10 text-error" },
}

export const TICKET_STATUS_CONFIG = {
  answered: { label: "Answered", icon: Check, className: "bg-success/10 text-success" },
  in_progress: { label: "In Progress", icon: Clock, className: "bg-warning/10 text-warning" },
  closed: { label: "Closed", icon: CircleCheck, className: "bg-success/10 text-success" },
}
