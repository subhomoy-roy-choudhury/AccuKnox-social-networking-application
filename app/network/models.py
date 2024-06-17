from django.db import models
from authentication.models import AuthUser

# Create your models here.
class Friendship(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    sender = models.ForeignKey(AuthUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(AuthUser, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='sent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')