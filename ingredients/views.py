from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserIngredients, ExcludedIngredients, Ingredients
from .serializers import UserIngredientsSerializer, ExcludedIngredientsSerializer, IngredientsSerializer
from rest_framework.permissions import AllowAny


from rest_framework.decorators import api_view, permission_classes #notification
from datetime import date, timedelta #notification
from rest_framework.views import APIView

class UserIngredientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = UserIngredients.objects.filter(user_id=request.user)
        serializer = UserIngredientsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        data = request.data if is_many else [request.data]

        created = []
        errors = []

        for entry in data:
            ingredient_id = entry.get("ingredient_id")
            try:
                ingredient = Ingredients.objects.get(ingredient_id=ingredient_id)
                ingredient_name = ingredient.ingredient_name
            except Ingredients.DoesNotExist:
                errors.append({
                    "ingredient_id": ingredient_id,
                    "error": "해당 재료를 찾을 수 없습니다."
                })
                continue

            serializer = UserIngredientsSerializer(data=entry)
            if serializer.is_valid():
                serializer.save(user_id=request.user)
                created.append(serializer.data)
            else:
                errors.append({
                    "data": entry,
                    "ingredient_name": ingredient_name,
                    "errors": serializer.errors
                })

        status_code = status.HTTP_207_MULTI_STATUS if errors else status.HTTP_201_CREATED
        return Response({"created": created, "errors": errors}, status=status_code)

    def delete(self, request, *args, **kwargs):
        user_ingredient_ids = request.data.get("user_ingredient_ids", [])
        if not isinstance(user_ingredient_ids, list):
            return Response({"error": "user_ingredient_ids는 리스트여야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        deleted = []
        errors = []

        for uid in user_ingredient_ids:
            try:
                obj = UserIngredients.objects.get(user_id=request.user, user_ingredient_id=uid)
                deleted.append({"user_ingredient_id": uid, "ingredient_name": obj.ingredient_id.ingredient_name})
                obj.delete()
            except UserIngredients.DoesNotExist:
                errors.append({"user_ingredient_id": uid, "error": "해당 재료를 찾을 수 없습니다."})

        status_code = status.HTTP_207_MULTI_STATUS if errors else status.HTTP_200_OK
        return Response({"deleted": deleted, "errors": errors}, status=status_code)


class ExcludedIngredientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = ExcludedIngredients.objects.filter(user_id=request.user)
        serializer = ExcludedIngredientsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        ingredient_ids = request.data.get("ingredient_ids", [])
        if not isinstance(ingredient_ids, list):
            return Response({"error": "ingredient_ids는 리스트여야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        errors = []

        for iid in ingredient_ids:
            try:
                ingredient = Ingredients.objects.get(ingredient_id=iid)
                ingredient_name = ingredient.ingredient_name
            except Ingredients.DoesNotExist:
                errors.append({
                    "ingredient_id": iid,
                    "error": "해당 재료를 찾을 수 없습니다."
                })
                continue

            if ExcludedIngredients.objects.filter(user_id=request.user, ingredient_id=iid).exists():
                errors.append({
                    "ingredient_id": iid,
                    "ingredient_name": ingredient_name,
                    "error": "이미 제외된 재료입니다."
                })
                continue

            serializer = ExcludedIngredientsSerializer(data={"ingredient_id": iid})
            if serializer.is_valid():
                serializer.save(user_id=request.user)
                created.append(serializer.data)
            else:
                errors.append({
                    "ingredient_id": iid,
                    "ingredient_name": ingredient_name,
                    "errors": serializer.errors
                })

        status_code = status.HTTP_207_MULTI_STATUS if errors else status.HTTP_201_CREATED
        return Response({"created": created, "errors": errors}, status=status_code)

    def delete(self, request, *args, **kwargs):
        excluded_ids = request.data.get("excluded_ids", [])
        if not isinstance(excluded_ids, list):
            return Response({"error": "excluded_ids는 리스트여야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        deleted = []
        errors = []

        for eid in excluded_ids:
            try:
                obj = ExcludedIngredients.objects.get(user_id=request.user, excluded_id=eid)
                deleted.append({"excluded_id": eid, "ingredient_name": obj.ingredient_id.ingredient_name})
                obj.delete()
            except ExcludedIngredients.DoesNotExist:
                errors.append({"excluded_id": eid, "error": "해당 제외 재료를 찾을 수 없습니다."})

        status_code = status.HTTP_207_MULTI_STATUS if errors else status.HTTP_200_OK
        return Response({"deleted": deleted, "errors": errors}, status=status_code)

#notifications
@api_view(['GET'])
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


# List all ingredients (public)
class AllIngredientsListView(generics.ListAPIView):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [AllowAny]
