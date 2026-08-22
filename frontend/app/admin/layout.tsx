import AdminTopBar from '@/components/admin/top-bar'

const AdminLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className='h-full w-full p-8x bg-muted flex flex-col gap-4'>
      <AdminTopBar />
      <div className='bg-white rounded-4xl h-full w-full p-4'>
        {children}
      </div>

    </div>
  )
}

export default AdminLayout