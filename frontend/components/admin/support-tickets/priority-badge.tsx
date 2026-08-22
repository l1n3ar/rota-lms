import { Badge } from '@/components/ui/badge'


interface PriorityBadgeProps {
    priority?: 'low' | 'moderate' | 'high'
}

const PriorityBadge = ({ priority }: PriorityBadgeProps) => {


    return (

        <Badge>Yo</Badge>
    )
}

export default PriorityBadge