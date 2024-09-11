from django.db import models
from django.contrib.auth import get_user_model

class FriendRequest(models.Model):
    """
    Represents a friend request between users in the social network.
    This model stores information about friend requests, including 
    the sender, receiver, status of the request, and timestamps for 
    creation and updates. It enforces uniqueness on the combination 
    of sender and receiver to prevent duplicate requests.
    
    Attributes:
        REQUEST_STATUS (tuple): A set of choices for the status of the friend request.
        sender (ForeignKey): The user who sends the friend request.
        receiver (ForeignKey): The user who receives the friend request.
        status (CharField): The current status of the friend request (pending, accepted, rejected).
        created_at (DateTimeField): The timestamp when the friend request was created.
        updated_at (DateTimeField): The timestamp when the friend request was last updated.
        
    Meta:
        unique_together: Ensures that a sender cannot send multiple requests to the same receiver.
    """

    REQUEST_STATUS = (
        ('pending', 'Pending'), 
        ('accepted', 'Accepted'), 
        ('rejected', 'Rejected')
    )
    sender = models.ForeignKey(
        get_user_model(),
        null=False,
        related_name='sent_requests', 
        on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        get_user_model(), 
        null=False,
        blank=False,
        related_name='received_requests', 
        on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        unique_together = ('sender', 'receiver')
