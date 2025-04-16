from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserIngredients, ExcludedIngredients
from .serializers import UserIngredientsSerializer, ExcludedIngredientsSerializer


class UserIngredientsListCreateView(generics.ListCreateAPIView):
    serializer_class = UserIngredientsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserIngredients.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class UserIngredientsDeleteView(generics.DestroyAPIView):
    serializer_class = UserIngredientsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_ingredient_id'

    def get_queryset(self):
        return UserIngredients.objects.filter(user_id=self.request.user)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({"message": "재료가 삭제되었습니다."}, status=status.HTTP_200_OK)


class ExcludedIngredientsListCreateView(generics.ListCreateAPIView):
    serializer_class = ExcludedIngredientsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExcludedIngredients.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ExcludedIngredientsDeleteView(generics.DestroyAPIView):
    serializer_class = ExcludedIngredientsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'excluded_id'

    def get_queryset(self):
        return ExcludedIngredients.objects.filter(user_id=self.request.user)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({"message": "제외 목록에서 재료가 삭제되었습니다."}, status=status.HTTP_200_OK)
