import { requestOTP } from '@/actions/auth'


const ApiExample = async () => {

    const response = await requestOTP('mehulchattopadhyaypersonal@gmail.com')

    return (
        <div>{JSON.stringify(response)}</div>
    )
}

export default ApiExample