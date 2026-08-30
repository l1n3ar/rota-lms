import TopBar from "@/components/shared/top-bar"


const ProtectedLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className='min-h-screen h-full w-full p-8x bg-muted flex flex-col gap-4'>
      <TopBar />
      <div className='bg-card rounded-4xl h-full w-full p-6'>
        {children}
      </div>

    </div>
  )
}

export default ProtectedLayout