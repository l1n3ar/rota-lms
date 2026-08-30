import {
    InputOTP,
    InputOTPGroup,
    InputOTPSlot,
} from "@/components/ui/input-otp"
import { Button } from "../ui/button"
import { ArrowRight } from "lucide-react"


const VerifyOTPStep = () => {
    return (
        <div className="flex flex-col gap-4x  items-center justify-center">
            <InputOTP maxLength={6}>
                <InputOTPGroup>
                    <InputOTPSlot index={0} />
                    <InputOTPSlot index={1} />
                    <InputOTPSlot index={2} />
                    <InputOTPSlot index={3} />
                    <InputOTPSlot index={4} />
                    <InputOTPSlot index={5} />
                </InputOTPGroup>
            </InputOTP>
            <div className="flex w-full items-center justify-between">
                <span className="text-xs">00:59</span>
                <Button variant='outline' size='sm' className='rounded-full'>
                    Resend Code
                    <ArrowRight />
                </Button>
            </div>
        </div>
    )
}

export default VerifyOTPStep