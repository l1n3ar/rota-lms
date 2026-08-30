'use client'

import { useState } from 'react'
import Image from 'next/image'

import pageBg from '@/public/login/gradient-bg.png'
import contentBg from '@/public/login/content-bg.png'
import logo from '@/public/logo-dark.png'

import LoginHeader from '@/components/login/header'
import LoginFooter from '@/components/login/footer'

import { LOGIN_STEP_CONFIG } from '@/components/login/config'
import { LOGIN_STEPS } from '@/types/auth'


const Login = () => {

    const [currentStep, setCurrentStep] = useState<LOGIN_STEPS>('email')

    const { header, button, component: StepComponent } = LOGIN_STEP_CONFIG[currentStep]

    const setStep = () => {
        switch (currentStep) {
            case 'email':
                setCurrentStep('otp')
                break
            case 'otp':
                setCurrentStep('reg')
                break
            default:
                setCurrentStep('email')
        }
    }

    return (
        <div
            className='h-full min-h-screen w-full flex items-center justify-center bg-cover bg-center'
            style={{ backgroundImage: `url(${pageBg.src})` }}
        >

            <div className='flex flex-col h-[35rem] w-xl rounded-4xl items-center gap-10x p-10x bg-cover bg-center'
                style={{ backgroundImage: `url(${contentBg.src})` }}
            >

                <div className='flex flex-col items-center gap-10x'>
                    <Image src={logo} alt='Logo' />
                    <LoginHeader title={header.title} desc={header.desc} />
                </div>

                <div className='flex-1 w-full flex items-center justify-center'>
                    <StepComponent />
                </div>

                <LoginFooter onClick={setStep} buttonText={button.text} />
            </div>

        </div>
    )
}

export default Login