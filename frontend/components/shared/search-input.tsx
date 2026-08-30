import { Search } from 'lucide-react'
import { InputGroup, InputGroupInput, InputGroupAddon } from '../ui/input-group'
import { cn } from '@/lib/utils'

interface SearchInputProps {
    placeholderText: string

    className?: string
}

const SearchInput = ({
    placeholderText,
    className
}: SearchInputProps) => {
    return (
        <InputGroup className={cn('bg-card p-6 flex w-[20rem]', className)}>

            <InputGroupInput
                id="inline-end-input"
                placeholder={placeholderText}
            />

            <InputGroupAddon align="inline-end">
                <Search />
            </InputGroupAddon>

        </InputGroup>
    )
}

export default SearchInput