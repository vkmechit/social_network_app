from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()

class EmailLoginSerializer(serializers.Serializer):
    """
    Serializer for handling email-based user login.
    This serializer validates the email and password fields required for user authentication. 
    It ensures that the provided email is in a valid format and that the password is captured for processing.
    
    Args:
        email: The email address of the user attempting to log in.
        password: The password associated with the user's email address.
    """

    email = serializers.EmailField()
    password = serializers.CharField()
    
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user instances in the application.
    This serializer is used to convert user model instances into a format suitable for rendering in responses. 
    It includes essential user information such as the user's ID, email, first name, and last name.

    Meta:
        model: The user model associated with this serializer.
        fields: The fields to be included in the serialized output.
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)
    

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, handling validation and creation of user accounts.
    This serializer validates user input for registration, ensuring that the email is unique 
    and properly formatted, and that required fields are provided. It also hashes the password 
    before creating a new user instance.
    
    Args:
        email: The email address of the user, which must be unique.
        first_name: The first name of the user.
        last_name: The last name of the user.
        password: The password for the user account, which must meet length requirements.
        
    Returns:
        User: A newly created user instance.
    
    Raises:
        ValidationError: If the email is not unique, if required fields are missing, or if the email format is invalid.
    """

    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(), message="User already exists!")])
    first_name = serializers.CharField(
        required=True, max_length=100, min_length=1, allow_blank=True)
    last_name = serializers.CharField(
        required=True, max_length=100, min_length=1, allow_blank=True)
    password = serializers.CharField(
        required=True, max_length=20, min_length=8)

    def validate(self, data):
        email = data.get('email', None)
        
        # Check if email is provided
        if not email:
            raise serializers.ValidationError({'message': "Email is required."})
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError as e:
            raise serializers.ValidationError({'message': "Invalid email format."}) from e
        
        # Set username as email if the format is valid
        data['username'] = email  
        
        return super().validate(data)
    
    def create(self, validated_data):
        # Hashing the password 
        validated_data['password'] = make_password(
            validated_data.get('password'))

        return super().create(validated_data)


    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }