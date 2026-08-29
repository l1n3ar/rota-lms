import React from 'react'

const UserSupportPage = () => {
    return (
        <div className='flex w-full h-full '>

            <div id='text-section' className='w-1/3 flex flex-col justify-between' >
                <div id='support-text' className='flex flex-col'>
                    <span className='text-xs'>How can we help?</span>
                    <div className='max-w-[20rem]'>
                        <span className='text-2xl'>Have a question? </span> <br />
                        <span className='text-2xl text-muted-foreground'>We’ve probably answered it here. If not, our support team is just a </span>
                        <span className='text-2xl'>ticket away.</span>
                    </div>


                </div>

            </div>

            <div id='table-section' className='w-2/3'>

            </div>
        </div>
    )
}

export default UserSupportPage