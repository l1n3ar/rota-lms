'use client'
import pageBg from '@/public/login/gradient-bg.png'
import contentBg from '@/public/login/content-bg.png'
import logo from '@/public/logo-dark.png'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { ArrowRight } from 'lucide-react'
import { useState } from 'react'
import LoginHeader from '@/components/login/header'
import EnterEmailStep from '@/components/login/enter-email'

const Login = () => {

    const [currentStep, setCurrentStep] = useState<'email' | 'otp' | 'reg'>('email')

    return (
        <div
            className='h-full min-h-screen w-full flex items-center justify-center bg-cover bg-center'
            style={{ backgroundImage: `url(${pageBg.src})` }}
        >

            <div className='flex flex-col items-center justify-center gap-10x p-10x'
                style={{ backgroundImage: `url(${contentBg.src})` }}
            >

                <Image src={logo} alt='Logo' />
                <LoginHeader title='Welcome to ROTA' desc='Enter your email to receive a one-time verification code.' />

                
                    <EnterEmailStep />
    

                <Button className='rounded-full w-full p-6x'>
                    Send Code
                    <ArrowRight />
                </Button>
            </div>

        </div>
    )
}

export default Login