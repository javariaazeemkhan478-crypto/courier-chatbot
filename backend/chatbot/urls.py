from django.urls import path
from . import views

urlpatterns = [
    path("models/", views.get_models, name="get_models"),
    path("chat/", views.chat, name="chat"),
    path("history/<str:session_id>/", views.get_history, name="get_history"),
    path("conversations/", views.list_conversations, name="list_conversations"),
    path("conversations/<str:session_id>/delete/", views.delete_conversation, name="delete_conversation"),
    path("stats/", views.get_stats, name="get_stats"),
]
