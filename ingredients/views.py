from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserIngredients, ExcludedIngredients
from .serializers import UserIngredientsSerializer, ExcludedIngredientsSerializer


from rest_framework.decorators import api_view, permission_classes #notification
from datetime import date, timedelta #notification

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


#notifications
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expiring_soon_ingredients(request):
    today = date.today()
    three_days_later = today + timedelta(days=3)

    user_ingredients = UserIngredients.objects.filter(
        user_id=request.user, 
        expiration_date__range=(today, three_days_later)
    ).select_related('ingredient_id')  

    data = [
        {
            "ingredient_name": ui.ingredient_id.ingredient_name, 
            "expiration_date": ui.expiration_date
        }
        for ui in user_ingredients
    ]

    return Response(data)