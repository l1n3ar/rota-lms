"use client"

import { Button } from "@/components/ui/button"
import { AssignableAdmin } from "@/types/user"
import { ArrowRight } from "lucide-react"

export function AdminActionsCell({ admin }: { admin: AssignableAdmin }) {

    const handleAssign = () => {

    }

    return (
        <Button size="sm" variant="outline" className='rounded-full flex items-center gap-1' onClick={handleAssign}>
            <span>Assign</span>
            <ArrowRight />
        </Button>
    )
}
