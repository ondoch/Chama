from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import EmailTokenObtainPairSerializer, ChangePasswordSerializer, UserSummarySerializer

class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class MeView(APIView):
    def get(self, request):
        return Response(UserSummarySerializer(request.user).data)

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
