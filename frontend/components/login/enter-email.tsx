import React from 'react'
import { Label } from '../ui/label'
import { InputGroup, InputGroupAddon, InputGroupInput } from '../ui/input-group'
import { AlignLeft, Mail } from 'lucide-react'

import { FormFieldIcon } from '../ui/form-field'

const EnterEmailStep = () => {
    return (
        <div className='flex flex-col gap-2 w-full '>

            <Label>Email Address</Label>
            <InputGroup className=" py-6x rounded-full">
                <InputGroupAddon className='mr-2'>
                    <FormFieldIcon icon={Mail} />
                </InputGroupAddon>
                <InputGroupInput
                    id="subject"
                    placeholder="e.g. hussein@example.com"

                />
            </InputGroup>
        </div>
    )
}

export default EnterEmailStep