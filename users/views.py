from django.db.models import Q
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from helper.pagination import Pagination
from users.models import CustomUser
from users.serializers import UserSerializer, UserSignupSerializer, LoginSerializer

# Create your views here.
class SignupView(views.APIView):
    """Sign Up"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(views.APIView):
    """Login"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.get_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserSearchView(generics.ListAPIView):
    """List Users"""
    serializer_class = UserSerializer
    pagination_class = Pagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_keyword = self.request.query_params.get('q', '')
        return CustomUser.objects.filter(
            Q(email__iexact=search_keyword) | Q(first_name__icontains=search_keyword)
        )

