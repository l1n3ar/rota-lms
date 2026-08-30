import { Label } from '../ui/label'
import { InputGroup, InputGroupAddon, InputGroupInput } from '../ui/input-group'
import { Mail, User } from 'lucide-react'

import { FormFieldIcon } from '../ui/form-field'

const CompleteRegistrationStep = () => {
    return (
        <div className='flex flex-col gap-4x w-full '>
            <div className='flex flex-col gap-2x'>
                <Label>First Name</Label>
                <InputGroup className=" py-6x rounded-full">
                    <InputGroupAddon className='mr-2'>
                        <FormFieldIcon icon={User} />
                    </InputGroupAddon>
                    <InputGroupInput
                        id="subject"
                        placeholder="e.g. hussen"

                    />
                </InputGroup>
            </div>
            <div className='flex flex-col gap-2x'>
                <Label>Last Name</Label>
                <InputGroup className=" py-6x rounded-full">
                    <InputGroupAddon className='mr-2'>
                        <FormFieldIcon icon={User} />
                    </InputGroupAddon>
                    <InputGroupInput
                        id="subject"
                        placeholder="e.g. Valizadeh"

                    />
                </InputGroup>
            </div>

        </div>
    )
}

export default CompleteRegistrationStep