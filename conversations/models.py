from django.db import models
import uuid


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    user = models.CharField(max_length=255) # models.ForeignKey('users.User', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} with {self.user} started at {self.start_time}"


class Interaction(models.Model):
    interaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='interactions')
    timestamp = models.DateTimeField(auto_now_add=True)
    query = models.TextField()
    response = models.TextField()

    def __str__(self):
        return f"{self.conversation.user} - {self.timestamp}"
