import { AssignableAdmin } from "@/types/user"

export const mockAssignableAdmins: AssignableAdmin[] = [
  {
    first_name: "Priya",
    last_name: "Nair",
    role: "superuser",
    status: "online",
    open_tickets: 3,
    created_at: new Date("2025-01-14T08:00:00Z"),
    updated_at: new Date("2026-01-05T10:30:00Z"),
  },
  {
    first_name: "Arjun",
    last_name: "Verma",
    role: "superuser",
    status: "away",
    open_tickets: 5,
    created_at: new Date("2025-06-01T08:00:00Z"),
    updated_at: new Date("2026-02-20T17:00:00Z"),
  },
  {
    first_name: "Kavya",
    last_name: "Menon",
    role: "superuser",
    status: "offline",
    open_tickets: 0,
    created_at: new Date("2025-04-11T08:00:00Z"),
    updated_at: new Date("2026-02-01T09:00:00Z"),
  },
]
