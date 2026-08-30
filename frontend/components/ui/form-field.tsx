import * as React from "react"

import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"

interface FormFieldProps {
  label: React.ReactNode
  htmlFor?: string
  hint?: React.ReactNode
  error?: React.ReactNode
  className?: string
  children: React.ReactNode
}

function FormField({ label, htmlFor, hint, error, className, children }: FormFieldProps) {
  return (
    <div className={cn("flex flex-col gap-2x", className)}>
      <div className="flex items-center justify-between">
        <Label htmlFor={htmlFor}>{label}</Label>
        {hint && <span className="text-xs text-muted-foreground leading-0">{hint}</span>}
      </div>
      {children}
      {error && <span className="text-xs text-destructive">{error}</span>}
    </div>
  )
}

interface FormFieldIconProps {
  icon: React.ComponentType<{ className?: string }>
}

function FormFieldIcon({ icon: Icon }: FormFieldIconProps) {
  return (
    <>
      <Icon />
      <Separator orientation="vertical" />
    </>
  )
}

export { FormField, FormFieldIcon }
