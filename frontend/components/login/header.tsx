import React from 'react'

interface LoginHeaderProps{
    title : string
    desc : string
}

const LoginHeader = ({
    title,
    desc
} : LoginHeaderProps) => {
    return (
        <div className='flex flex-col items-center '>
            <span className='text-2xl'>{title}</span>
            <span className='text-muted-foreground'>{desc}</span>
        </div>
    )
}

export default LoginHeader