from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate

from users.models import User
from .serializers import UserSerializer


class LoginView(APIView):
    """
    POST /api/users/login
    Login with email and password
    """
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data.get('user', {})
        email = user_data.get('email')
        password = user_data.get('password')

        if not email or not password:
            return Response(
                {'errors': {'body': ['Email and password are required']}},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'errors': {'body': ['Invalid email or password']}},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        serializer = UserSerializer(user)
        return Response({'user': serializer.data})


class RegisterView(APIView):
    """
    POST /api/users
    Register a new user
    """
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data.get('user', {})

        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'user': UserSerializer(user).data},
                status=status.HTTP_201_CREATED
            )

        # Format errors according to RealWorld spec
        errors = []
        for field, messages in serializer.errors.items():
            for message in messages:
                errors.append(f"{field}: {message}")

        return Response(
            {'errors': {'body': errors}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class GetCurrentUserView(APIView):
    """
    GET /api/user - Get current user
    PUT /api/user - Update current user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user"""
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data})

    def put(self, request):
        """Update current user"""
        user_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user,
            data=user_data,
            partial=True  # Allow partial updates
        )

        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': UserSerializer(user).data})

        # Format errors according to RealWorld spec
        errors = []
        for field, messages in serializer.errors.items():
            for message in messages:
                errors.append(f"{field}: {message}")

        return Response(
            {'errors': {'body': errors}},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
