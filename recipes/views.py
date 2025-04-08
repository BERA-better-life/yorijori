from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendRecipeAPIView(APIView):
    def post(self, request):
        user_ingredients = request.data.get('ingredients', [])

        if not user_ingredients:
            return Response({'error': 'ingredients list is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 레시피 재료 문자열 생성
        recipes = Recipe.objects.prefetch_related('ingredients').all()
        ingredient_docs = []
        recipe_info = []

        for recipe in recipes:
            ingredient_names = [i.ingredient_name for i in recipe.ingredients.all()]
            ingredient_docs.append(' '.join(ingredient_names))
            recipe_info.append({'rcp_number': recipe.rcp_number, 'rcp_name': recipe.rcp_name})

        # 벡터화 및 유사도 계산
        vectorizer = CountVectorizer()
        matrix = vectorizer.fit_transform(ingredient_docs)
        user_vector = vectorizer.transform([' '.join(user_ingredients)])
        similarity = cosine_similarity(user_vector, matrix)[0]

        # 상위 10개 추출
        top_indices = similarity.argsort()[::-1][:10]
        result = [recipe_info[i] for i in top_indices]

        return Response(result)
