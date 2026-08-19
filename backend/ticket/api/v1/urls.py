from django.urls import path
from ticket.api.v1.views.tickets import *
from ticket.api.v1.views.comments import TicketCommentCreateView


urlpatterns = [
    path("create/", TicketCreateView.as_view(), name="ticket-create"),
    path("", TicketListView.as_view(), name="ticket-list"),
    path("<str:ticket_id>/", TicketDetailView.as_view(), name="ticket-detail"),

    path("<str:ticket_id>/comment/", TicketCommentCreateView.as_view(), name="ticket-comment-create"),
]
