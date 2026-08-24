from django.contrib import admin
from .models import Ticket, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # What columns show up in the main list view
    list_display = (
        'ticket_id',
        'subject',
        'status',
        'priority',
        'category',
        'created_by',
        'assignee',
        'updated_at'
    )

    # Adds a filter sidebar on the right
    list_filter = ('status', 'priority', 'category', 'created_at')

    # Adds a search bar at the top
    search_fields = ('ticket_id', 'subject', 'issue_description', 'created_by__email', 'created_by__first_name', 'created_by__last_name')

    # Protects auto-generated fields from being edited manually
    readonly_fields = ('ticket_id', 'created_at', 'updated_at', 'resolved_date')

    # Allows you to see and add comments directly inside the Ticket view
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'ticket__ticket_id', 'created_by__email', 'created_by__first_name', 'created_by__last_name')
    readonly_fields = ('created_at',)