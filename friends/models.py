from django.db import models

from users.models import CustomUser

# Create your models here.

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name="send_request", on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name="received_request", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')

    class Meta:
        unique_together = ('from_user', 'to_user')

class Friend(models.Model):
    user = models.ForeignKey(CustomUser, related_name="friends", on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name="friends_of", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)