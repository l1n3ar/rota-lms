import { ComponentType } from 'react'

import EnterEmailStep from './enter-email'
import VerifyOTPStep from './verify-otp'
import CompleteRegistrationStep from './complete-reg'
import { LOGIN_STEPS } from '@/types/auth'


interface LoginStepConfig {
    header: {
        title: string
        desc: string
    }
    button: {
        text: string
    }
    component: ComponentType
}

export const LOGIN_STEP_CONFIG: Record<LOGIN_STEPS, LoginStepConfig> = {

    email: {
        header: {
            title: 'Welcome to ROTA',
            desc: 'Enter your email to receive a one-time verification code.',
        },
        button: { text: 'Send Code' },
        component: EnterEmailStep,
    },

    otp: {
        header: {
            title: 'Check your Inbox',
            desc: 'Enter the 6-digit code we sent to your email address.',
        },
        button: { text: 'Verify Code' },
        component: VerifyOTPStep,
    },

    reg: {
        header: {
            title: 'Complete your profile',
            desc: 'Tell us a bit about yourself to finish setting up your account.',
        },
        button: { text: 'Register' },
        component: CompleteRegistrationStep,
    },

}
