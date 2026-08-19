import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"

export default function Page() {
  return (
    <div>
      <Button className="mb-2">ROTA <ArrowRight /></Button>
      <div className="font-mono text-xs text-muted-foreground">
        (Press <kbd>d</kbd> to toggle dark mode)
      </div>
    </div>
  )
}
