from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Success'
            },
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username= serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return Response({
                    'message': 'Login success',
                    'access_token': str(access_token),  
                    'refresh_token': str(refresh), 
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid username or password'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



