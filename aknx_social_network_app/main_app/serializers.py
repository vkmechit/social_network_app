from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .models import FriendRequest

User = get_user_model()

class SocialRequestSerializer(serializers.Serializer):
    """
    Serializer for handling social friend requests between users.
    This serializer validates and creates friend requests, ensuring 
    that the sender is not sending a request to themselves and that 
    no existing requests or friendships already exist between the users. 
    It includes fields for the sender, receiver, and additional request metadata.
    
    Args:
        sender: The user sending the friend request (read-only).
        receiver: The user receiving the friend request.
    
    Returns:
        FriendRequest: A newly created friend request instance.
    
    Raises:
        ValidationError: If the sender attempts to send a request to themselves or if a request already exists between the users.
    """


    receiver= serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={'does_not_exist': 'You can not send request to this user as it does not exist.'}
    )
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']

    def validate(self, data):
        sender = self.context['request'].user
        receiver = data.get('receiver')

        # Check if user sending request to himself
        if sender == receiver:
            raise serializers.ValidationError({"message": "You cannot send a friend request to yourself."})
        
        # Check if a connection already exists between these users
        existing_request = FriendRequest.objects.filter(
            sender=sender,
            receiver=receiver,
        ).exclude(status='rejected').exists()

        if existing_request:
            raise ValidationError({"message": "A friend request already exists, or you are already friends."})

        return data
    
    def create(self, validated_data):
        # Set the sender as the currently authenticated user
        validated_data['sender'] = self.context['request'].user

        return FriendRequest.objects.create(**validated_data)
    
class FriendsSerializer(serializers.ModelSerializer):
    """
    Serializer for friend request objects, providing user details.
    This serializer transforms friend request instances into a format that includes the receiver's email, first name, and last name. 
    It utilizes custom methods to extract these fields from the related user model.
    Attributes:
        email (str): The email address of the receiver.
        first_name (str): The first name of the receiver.
        last_name (str): The last name of the receiver.
    Meta:
        model: The model associated with this serializer (FriendRequest).
        fields: The fields to be included in the serialized output.
    """

    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'user_id', 'email', 'first_name', 'last_name']

    def get_email(self, obj):
        return obj.sender.email 

    def get_first_name(self, obj):
        return obj.sender.first_name

    def get_last_name(self, obj):
        return obj.sender.last_name
    
    def get_user_id(self, obj):
        return obj.sender.id

