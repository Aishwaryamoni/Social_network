from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        ACCEPTED = 'A', 'Accepted'
        REJECTED = 'R', 'Rejected'

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    
    def __str__(self):
        return f"{self.id} ->{self.from_user} -> {self.to_user} ({self.status})"
