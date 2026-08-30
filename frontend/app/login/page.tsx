'use client'

import { useState } from 'react'
import Image from 'next/image'

import pageBg from '@/public/login/gradient-bg.png'
import contentBg from '@/public/login/content-bg.png'
import logo from '@/public/logo-dark.png'

import LoginHeader from '@/components/login/header'
import LoginFooter from '@/components/login/footer'

import EnterEmailStep from '@/components/login/enter-email'
import VerifyOTPStep from '@/components/login/verify-otp'
import CompleteRegistrationStep from '@/components/login/complete-reg'


const Login = () => {

    const [currentStep, setCurrentStep] = useState<'email' | 'otp' | 'reg'>('email')

    return (
        <div
            className='h-full min-h-screen w-full flex items-center justify-center bg-cover bg-center'
            style={{ backgroundImage: `url(${pageBg.src})` }}
        >

            <div className='flex flex-col rounded-4xl items-center justify-center gap-10x p-10x bg-cover bg-center'
                style={{ backgroundImage: `url(${contentBg.src})` }}
            >

                <Image src={logo} alt='Logo' />
                <LoginHeader title='Welcome to ROTA' desc='Enter your email to receive a one-time verification code.' />
                <EnterEmailStep />
                <VerifyOTPStep />
                <CompleteRegistrationStep />
                <LoginFooter onClick={() => { }} buttonText='Send Code' />
            </div>

        </div>
    )
}

export default Login