from rest_framework import serializers
from ticket.models import Ticket, Comment


class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Used for creating tickets.
    The user is set from JWT automatically.
    """

    class Meta:
        model = Ticket
        # Included 'category' and 'priority' since they are part of the TS interface
        fields = ["category", "subject", "issue_description", "priority"]

    def create(self, validated_data):
        user = self.context["request"].user
        # Mapped the authenticated user to the new 'created_by' field
        return Ticket.objects.create(created_by=user, **validated_data)


class TicketListSerializer(serializers.ModelSerializer):
    """
    List tickets for the authenticated user.
    Includes last comment date.
    """
    last_comment_date = serializers.SerializerMethodField()
    # Aliased 'ticket_id' to 'id' to perfectly match the TS interface requirement 'id: string'
    id = serializers.CharField(source="ticket_id", read_only=True)

    class Meta:
        model = Ticket
        # Updated fields to reflect the new model properties and TS types
        fields = [
            "id",
            "category",
            "subject",
            "status",
            "priority",
            "last_comment_date",
            "updated_at"
        ]

    def get_last_comment_date(self, obj):
        # Swapped 'comment_set' for 'comments' (from related_name) and 'created_date' for 'created_at'
        last_comment = obj.comments.order_by("-created_at").first()
        return last_comment.created_at if last_comment else None


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments.
    """
    # Renamed from 'user' to 'created_by'
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        # Updated 'created_date' to 'created_at'
        fields = ["id", "created_by", "text", "created_at", "attachment"]


class TicketDetailSerializer(serializers.ModelSerializer):
    """
    Detailed view of a ticket with all comments.
    """
    # Removed source="comment_set" because we set related_name="comments" in the model
    comments = CommentSerializer(many=True, read_only=True)

    # Aliasing to match the TS 'id' field
    id = serializers.CharField(source="ticket_id", read_only=True)

    # Returning string representations for the frontend (or you can nest a UserSerializer here)
    created_by = serializers.StringRelatedField(read_only=True)
    assignee = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        # Brought in all the required fields from the TS SupportTicket type
        fields = [
            "id",
            "created_by",
            "category",
            "subject",
            "issue_description",
            "priority",
            "status",
            "assignee",
            "created_at",
            "updated_at",
            "comments"
        ]