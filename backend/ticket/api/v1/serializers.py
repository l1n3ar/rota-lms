from rest_framework import serializers
from ticket.models import Ticket, Comment

class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Used for creating tickets (only title + issue_description).
    The user is set from JWT automatically.
    """
    class Meta:
        model = Ticket
        fields = ["title", "issue_description"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Ticket.objects.create(user=user, **validated_data)


class TicketListSerializer(serializers.ModelSerializer):
    """
    List tickets for the authenticated user.
    Includes last comment date.
    """
    last_comment_date = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["ticket_id", "title", "completed_status", "last_comment_date"]

    def get_last_comment_date(self, obj):
        last_comment = obj.comment_set.order_by("-created_date").first()
        return last_comment.created_date if last_comment else None


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments.
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created_date", "attachment"]


class TicketDetailSerializer(serializers.ModelSerializer):
    """
    Detailed view of a ticket with all comments.
    """
    comments = CommentSerializer(source="comment_set", many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ["ticket_id", "title", "issue_description", "created_date", "comments"]
