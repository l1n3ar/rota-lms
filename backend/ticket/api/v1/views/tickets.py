from rest_framework import generics, permissions
from ticket.models import Ticket
from ticket.api.v1.serializers import (
    TicketCreateSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
)
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Ticket"],
    summary="Create a new ticket",
    description="Authenticated users can create a ticket by providing category, subject, issue_description, and priority. "
                "The ticket_id is generated automatically.",
    request=TicketCreateSerializer,
    responses={201: TicketDetailSerializer},
)
class TicketCreateView(generics.CreateAPIView):
    serializer_class = TicketCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=["Ticket"],
    summary="List user tickets",
    description="Returns all tickets. Superusers see all tickets in the system. "
                "Regular users only see tickets they created.",
    responses={200: TicketListSerializer(many=True)},
)
class TicketListView(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request_user = self.request.user
        # Superusers can see every ticket
        if request_user.is_superuser:
            # Added .select_related() and .prefetch_related() to optimize database queries
            return Ticket.objects.all().order_by('-updated_at')

        # Regular users only see their own - UPDATED to use 'created_by'
        return Ticket.objects.filter(created_by=request_user).order_by('-updated_at')


@extend_schema(
    tags=["Ticket"],
    summary="Retrieve or update ticket details",
    description="Retrieve a ticket by ticket_id. Superusers can access and update ANY ticket. "
                "Regular users can only access their own.",
    responses={200: TicketDetailSerializer},
)
# Changed to RetrieveUpdateAPIView so superusers can send PATCH/PUT requests to respond/update
class TicketDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TicketDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "ticket_id"

    def get_queryset(self):
        user = self.request.user
        # Allow superusers to query ANY ticket so they can view and update it
        if user.is_superuser:
            return Ticket.objects.all()

        # Restrict regular users to only their own tickets - UPDATED to use 'created_by'
        return Ticket.objects.filter(created_by=user)