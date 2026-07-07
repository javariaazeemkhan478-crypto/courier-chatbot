from django.db import models

class Conversation(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    model_used = models.CharField(max_length=100)
    title = models.CharField(max_length=200, default='New Chat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.session_id}"

class Message(models.Model):
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'Assistant')]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    is_favorite = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"