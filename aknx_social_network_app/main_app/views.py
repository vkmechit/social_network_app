from django.shortcuts import render
from .serializers import (
    SocialRequestSerializer,
    FriendsSerializer
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
from django.db.models import Q
from .models import FriendRequest
from .throttles import FriendRequestRateThrottle

    
class SocialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = FriendRequest.objects.all()
    serializer_class = SocialRequestSerializer
    
    
    @action(
        methods=['post'], 
        detail=False, 
        permission_classes=[IsAuthenticated, ], 
        serializer_class=SocialRequestSerializer,
        # throttle_scope = 'friend_request',
        throttle_classes=[FriendRequestRateThrottle, ]
        # throttle_classes=[FriendRequestRateThrottle,]
        )
    def send_request(self, request):
        """
        Handles the sending of friend requests between users.
        This method validates the incoming request data for creating 
        a friend request and processes it if valid. Upon successful creation, 
        it returns the serialized data of the newly created friend request.

        Args:
            request: The HTTP request object containing the friend request data.
            pk: An optional primary key for additional context (not used in this method).

        Returns:
            Response: A serialized representation of the created friend request with a status of 201 Created.

        Raises:
            ValidationError: If the provided friend request data is invalid.
        """
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        friend_request = serializer.save()
        return Response({"message": "Request Sent Successfully!"}, status=status.HTTP_201_CREATED)
    
    @action(
        methods=['post'], 
        detail=True, 
        permission_classes=[IsAuthenticated]
        )
    def update_request_status(self, request, pk=None):
        """
        Updates the status of a friend request based on the provided input.
        This method allows authenticated users to change the status of a friend request to either 'accepted' or 'rejected'. 
        It verifies the current status of the request and ensures that only valid status values are processed.
        
        Args:
            request: The HTTP request object containing the status for the friend request.
            pk: The primary key of the friend request to be updated.
        
        Returns:
            Response: A message indicating the result of the status update.
        
        Raises:
            ValidationError: If the provided status is not 'accepted' or 'rejected'.
        """

        try:
            friend_request = self.get_object()

            # Verify wether request already sent
            if friend_request.status != 'pending':
                return Response({"message": "This request has already been processed."}, status=status.HTTP_400_BAD_REQUEST)

            status_value = request.data.get('status')

            if status_value not in ['accepted', 'rejected']:
                raise ValidationError({"message": "Invalid status. Only 'accepted' or 'rejected' are allowed."})

            friend_request.status = status_value
            friend_request.save()

            action_message = "accepted" if status_value == 'accepted' else "rejected"
            return Response({"message": f"Friend request {action_message}."}, status=status.HTTP_200_OK)
        
        except FriendRequest.DoesNotExist:
            return Response({"message": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(
        methods=['get'], 
        detail=False, 
        permission_classes=[IsAuthenticated]
        )
    def get_friend_list(self, request):
        """
        Retrieves the list of friends for the authenticated user.
        This method fetches and returns a list of accepted friend requests for the user making the request. 
        
        Args:
            request: The HTTP request object used to access the authenticated user's information.
        
        Returns:
            Response: A paginated response containing the list of friends associated with the authenticated user.
        """

        # Extract user from request data
        receiver = request.user
        
        queryset = FriendRequest.objects.filter(receiver=receiver, status='accepted')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FriendsSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = FriendsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['get'], 
        detail=False, 
        permission_classes=[IsAuthenticated]
        )
    def get_pending_friend_requests(self, request):
        """
        Retrieves the list of pending friend requests for the authenticated user.
        This method fetches and returns all friend requests that are currently pending for the user making the request. 
        
        Args:
            request: The HTTP request object used to access the authenticated user's information.
        
        Returns:
            Response: A paginated response containing the list of pending friend requests for the authenticated user.
        """

        # Extract current user from request data
        logged_in_user = request.user
        
        queryset = FriendRequest.objects.filter(receiver=logged_in_user, status='pending')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FriendsSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = FriendsSerializer(queryset, many=True)
        return Response(serializer.data)