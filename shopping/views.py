from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from collections import Counter
from recipes.models import RecipesIngredients
from ingredients.models import UserIngredients

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_ingredients(request):
    user_ingredients = UserIngredients.objects.filter(user_id=request.user).values_list('ingredient_id__ingredient_name', flat=True)

    # 1. 유저가 가진 재료를 포함하는 레시피 ID 찾기
    matched_recipes = RecipesIngredients.objects.filter(
        ingredient_id__ingredient_name__in=user_ingredients
    ).values_list('rcp_number', flat=True).distinct()

    # 2. 해당 레시피에서 유저가 없는 재료들 수집
    matched_ingredients = RecipesIngredients.objects.filter(
        rcp_number__in=matched_recipes
    ).exclude(ingredient_id__ingredient_name__in=user_ingredients)

    # 3. 빈도수 계산
    counter = Counter(matched_ingredients.values_list('ingredient_id__ingredient_name', flat=True))

    # 4. 상위 5개 추천
    recommendations = [ingredient for ingredient, _ in counter.most_common(5)]

    return Response({
        "input_ingredients": list(user_ingredients),
        "recommended_ingredients": recommendations
    })
