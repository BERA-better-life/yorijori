from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Users
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            # 이메일 형식 검증
            try:
                validate_email(data['email'])
            except ValidationError:
                return Response({"error": "올바른 형식의 이메일을 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
            user = Users.objects.create(
                email=data['email'],
                username=data['username'],
                password=make_password(data['password']),
            )
            return Response({"message": "회원가입 성공!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CheckUsernameView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get("username")
        if not username:
            return Response({"detail": "username 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        exists = Users.objects.filter(username=username).exists()
        return Response({"available": not exists}, status=status.HTTP_200_OK)

class CheckEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"detail": "email 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        exists = Users.objects.filter(email=email).exists()
        return Response({"available": not exists}, status=status.HTTP_200_OK)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원 탈퇴 완료!"}, status=status.HTTP_204_NO_CONTENT)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 클라이언트에게 refresh token 삭제를 유도하는 방식
        if "refresh" not in request.data:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "로그아웃 완료!"},
                        status=status.HTTP_205_RESET_CONTENT)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        data = request.data

        username = data.get("username")
        email = data.get("email")

        if username:
            user.username = username
        if email:
            user.email = email

        user.save()

        return Response({"message": "회원 정보가 수정되었습니다."}, status=status.HTTP_200_OK)

class AllUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = Users.objects.all().values("user_id", "username", "email")
        return Response(users, status=status.HTTP_200_OK)


# 알림 관련 
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_expo_token(request):
    token = request.data.get('token')
    if not token:
        return Response({"error": "Expo token is required."}, status=400)

    request.user.expo_push_token = token
    request.user.save()
    return Response({"message": "Token saved successfully."})
