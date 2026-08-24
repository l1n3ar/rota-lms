from rest_framework import generics, permissions, serializers
from ticket.models import Ticket, Comment
from ticket.api.v1.serializers import CommentSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Ticket"],
    summary="Add a comment to a ticket",
    description="Authenticated users can add a comment to their own ticket by providing text and optional attachment.",
    request=CommentSerializer,
    responses={201: CommentSerializer},
)
class TicketCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get("ticket_id")
        # 'created_by' is the model field (renamed from 'user')
        ticket = Ticket.objects.filter(ticket_id=ticket_id, created_by=self.request.user).first()
        if not ticket:
            raise serializers.ValidationError("Ticket not found or not yours.")
        serializer.save(created_by=self.request.user, ticket=ticket)
