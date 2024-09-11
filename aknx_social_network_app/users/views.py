from django.shortcuts import render
from .serializers import (
    EmailLoginSerializer,
    UserSerializer,
    RegisterSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.contrib.auth import authenticate
from django.db.models import Q

User = get_user_model()

class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
    @action(
        methods=['post'], 
        detail=False, 
        permission_classes=[AllowAny, ], 
        serializer_class=RegisterSerializer
        )
    def register(self, request, pk=None):
        """
        Handles user registration by validating input data and creating a new user account.
        
        Args:
            request: The HTTP request object containing the registration data.
            pk: An optional primary key for additional context (not used in this method).

        Returns:
            Response: A serialized representation of the newly created user account.

        Raises:
            ValidationError: If the provided registration data is invalid.
        """

        data = request.data
        serializer = RegisterSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = UserSerializer(user)
        response_data = response.data
        user.save()
        return Response(response_data)
    
    @action(
        methods=['post'], 
        detail=False, 
        permission_classes=[AllowAny, ], 
        serializer_class=EmailLoginSerializer
        )
    def email_login(self, request):
        """
        Handles user login via email and password authentication.
        This method validates the provided email and password, authenticates the user, and 
        returns a success message upon successful login. 
        If the credentials are invalid, it raises a validation error.
        
        Args:
            request: The HTTP request object containing the login data.
        
        Returns:
            Response: A success message indicating the user has logged in successfully.
        
        Raises:
            ValidationError: If the email or password is invalid.
        """

        data = request.data
        serializer = EmailLoginSerializer(
            data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            email = data.get('email', None)
            password = data.get('password', None)
            user = authenticate(username=email, password=password)
            if user is None:
                raise ValidationError(
                    {"message": ["Email or password is invalid"]})
            return Response({"message": "Logged in successfully!"})
    
    @action(
        methods=['get'], 
        detail=False, 
        permission_classes=[IsAuthenticated, ]
        )
    def search_users(self, request):
        """
        Retrieves a list of users based on optional search parameters.
        This method allows authenticated users to search for other users by a specified search term. 
        If no search term is provided, it returns all users, and the results can be paginated.
        
        Args:
            request: The HTTP request object containing the search parameters.
        
        Returns:
            Response: A paginated response containing the list of users matching the search criteria.
        
        Examples:
        To search for users with a specific title:
            GET /users/search?search=example
        """

        search_params = request.GET.get('search')
        queryset = User.objects.filter(
            Q(email__icontains=search_params) | 
            Q(first_name__icontains=search_params) |
            Q(last_name__icontains=search_params)) if search_params else User.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
