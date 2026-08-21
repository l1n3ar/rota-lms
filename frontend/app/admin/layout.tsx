import AdminTopBar from '@/components/admin/top-bar'

const AdminLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className='h-full w-full p-8x bg-neutral-100 flex flex-col gap-4'>
      <AdminTopBar />
      <div className='bg-white rounded-xl h-full w-full'>
        {children}
      </div>

    </div>
  )
}

export default AdminLayout