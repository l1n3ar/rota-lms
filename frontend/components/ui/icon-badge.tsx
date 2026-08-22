import { type LucideIcon } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface IconBadgeProps {
  label: string
  icon: LucideIcon
  className?: string
}

export function IconBadge({ label, icon: Icon, className }: IconBadgeProps) {
  return (
    <Badge className={cn("gap-1", className)}>
      <Icon />
      {label}
    </Badge>
  )
}
