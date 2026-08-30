
import { ArrowRight } from 'lucide-react'
import React from 'react'
import { Button } from '../ui/button'

interface LoginFooterProps {
    buttonText: string
    onClick: () => void

    extra?: React.ReactNode

}


const LoginFooter = ({
    buttonText,
    onClick,
    extra
}: LoginFooterProps) => {
    return (
        <div className='flex flex-col gap-2 w-full'>
            <div>{extra}</div>
            <Button className='rounded-full w-full p-6x' onClick={onClick}>
                {buttonText}
                <ArrowRight />
            </Button>
        </div>
    )
}

export default LoginFooter