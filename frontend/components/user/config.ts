import { Check, CircleAlert, DotIcon } from "lucide-react"

export const USER_STATUS_CONFIG = {
    online: { label: "Online", icon: Check, className: "bg-success/10 text-success" },
    away: { label: "Away", icon: CircleAlert, className: "bg-warning/10 text-warning" },
    offline: { label: "Offline", icon: DotIcon, className: "bg-muted text-muted-foreground" },
}