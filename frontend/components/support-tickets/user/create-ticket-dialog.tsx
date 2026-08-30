"use client"

import * as React from "react"
import { Controller, useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { AlignLeft, ArrowRight, Clock, GraduationCap, ListTree, Paperclip, Upload } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group"
import { FormField, FormFieldIcon } from "@/components/ui/form-field"
import { Separator } from "@/components/ui/separator"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import type { SUPPORT_TICKET_PRIORITY } from "@/types/support-ticket"

const CATEGORY_OPTIONS = ["Billing", "Course Access", "Bug Report", "Account"] as const

const PRIORITY_OPTIONS: {
  value: SUPPORT_TICKET_PRIORITY
  label: string
  description: string
}[] = [
    { value: "low", label: "Low", description: "Minor issue, no urgency" },
    { value: "medium", label: "Medium", description: "Impacts work, needs attention soon" },
    { value: "high", label: "High", description: "Blocking issue, needs urgent help" },
  ]

const createTicketSchema = z.object({
  subject: z.string().min(1, "Subject is required"),
  category: z.string().min(1, "Category is required"),
  priority: z.enum(["low", "medium", "high"]),
  relatedCourseId: z.string().optional(),
  description: z.string().min(1, "Description is required"),
  attachment: z.instanceof(File).optional(),
})

type CreateTicketFormValues = z.infer<typeof createTicketSchema>

interface CreateTicketDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  courses?: { id: string; name: string }[]
  onSubmit?: (values: CreateTicketFormValues) => void
}

const CreateTicketDialog = ({
  open,
  onOpenChange,
  courses = [],
  onSubmit,
}: CreateTicketDialogProps) => {
  const fileInputRef = React.useRef<HTMLInputElement>(null)

  const { register, control, handleSubmit, reset, formState: { errors } } =
    useForm<CreateTicketFormValues>({
      resolver: zodResolver(createTicketSchema),
      defaultValues: { priority: "low", category: "", relatedCourseId: "" },
    })

  const handleFormSubmit = (values: CreateTicketFormValues) => {
    onSubmit?.(values)
    reset()
    onOpenChange(false)
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(nextOpen) => {
        if (!nextOpen) reset()
        onOpenChange(nextOpen)
      }}
    >
      <DialogContent size='2xl'>
        <DialogHeader>
          <DialogTitle >Create Ticket</DialogTitle>
          <Separator className='mt-2' />
        </DialogHeader>

        <form onSubmit={handleSubmit(handleFormSubmit)} className="flex flex-col gap-4x">
          <div className="grid grid-cols-2 gap-2x">
            <FormField label="Subject" htmlFor="subject" error={errors.subject?.message}>
              <InputGroup className="py-6 px-2">
                <InputGroupAddon>
                  <FormFieldIcon icon={AlignLeft} />
                </InputGroupAddon>
                <InputGroupInput
                  id="subject"
                  placeholder="Briefly describe your issue"
                  {...register("subject")}
                />
              </InputGroup>
            </FormField>

            <FormField label="Category" error={errors.category?.message}>
              <Controller
                control={control}
                name="category"
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange} >
                    <SelectTrigger className="w-full px-4 py-6">
                      <FormFieldIcon icon={ListTree} />
                      <SelectValue placeholder="Select Category" />
                    </SelectTrigger>
                    <SelectContent>
                      {CATEGORY_OPTIONS.map((category) => (
                        <SelectItem key={category} value={category}>
                          {category}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </FormField>
          </div>

          <div className="grid grid-cols-2 gap-2x">
            <FormField label="Priority" >
              <Controller
                control={control}
                name="priority"
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange}>
                    <SelectTrigger className="w-full">
                      <FormFieldIcon icon={Clock} />
                      <SelectValue placeholder="Select priority">
                        {(value: SUPPORT_TICKET_PRIORITY | null) => {
                          const option = PRIORITY_OPTIONS.find((o) => o.value === value)
                          return option ? `${option.label} – ${option.description}` : "Select priority"
                        }}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {PRIORITY_OPTIONS.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label} <span className="text-muted-foreground">{option.description}</span>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </FormField>

            <FormField label="Related course" hint="optional">
              <Controller
                control={control}
                name="relatedCourseId"
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange} disabled={courses.length === 0}>
                    <SelectTrigger className="w-full">
                      <FormFieldIcon icon={GraduationCap} />
                      <SelectValue placeholder="Select a course..." />
                    </SelectTrigger>
                    <SelectContent>
                      {courses.map((course) => (
                        <SelectItem key={course.id} value={course.id}>
                          {course.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </FormField>
          </div>

          <FormField label="Description" htmlFor="description" error={errors.description?.message}>
            <Textarea
              id="description"
              placeholder="Explain what's happening, what you expected, and any error messages you see."
              {...register("description")}
            />
          </FormField>

          <FormField label="Attachment">
            <Controller
              control={control}
              name="attachment"
              render={({ field }) => (
                <>
                  <InputGroup>
                    <InputGroupAddon>
                      <FormFieldIcon icon={Paperclip} />
                    </InputGroupAddon>
                    <InputGroupInput
                      readOnly
                      value={field.value?.name ?? ""}
                      placeholder="Upload file (to send a document)"
                      className="cursor-default"
                    />
                    <InputGroupAddon align="inline-end">
                      <InputGroupButton
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => fileInputRef.current?.click()}
                      >
                        Select File
                        <Upload />
                      </InputGroupButton>
                    </InputGroupAddon>
                  </InputGroup>
                  <input
                    ref={fileInputRef}
                    type="file"
                    className="hidden"
                    onChange={(e) => field.onChange(e.target.files?.[0])}
                  />
                </>
              )}
            />
          </FormField>

          <Button type="submit" className="w-full rounded-full">
            Submit Ticket
            <ArrowRight />
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export default CreateTicketDialog
