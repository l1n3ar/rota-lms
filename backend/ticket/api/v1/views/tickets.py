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
    description="Authenticated users can create a ticket by providing title and issue_description. "
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
    description="Returns all tickets created by the authenticated user. "
                "Includes ticket_id, title, status, and last comment date.",
    responses={200: TicketListSerializer(many=True)},
)
class TicketListView(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_superuser:
            return Ticket.objects.all()
        else:
            return Ticket.objects.filter(user=request_user)


@extend_schema(
    tags=["Ticket"],
    summary="Retrieve ticket details",
    description="Retrieve a ticket by ticket_id if it belongs to the authenticated user. "
                "Returns title, issue_description, created_date, and all comments.",
    responses={200: TicketDetailSerializer},
)
class TicketDetailView(generics.RetrieveAPIView):
    serializer_class = TicketDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "ticket_id"

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
