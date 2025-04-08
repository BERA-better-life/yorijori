import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings

class RecipeRecommendationView(APIView):
    def post(self, request):
        user_ingredients = request.data.get('ingredients', [])

        if not user_ingredients:
            return Response({'error': 'ingredients is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # CSV 파일 경로 설정 (settings.py와 같은 위치 기준)
        base_dir = settings.BASE_DIR
        recipe_csv = os.path.join(base_dir, 'data/recipes_table_0408.csv')
        ingredient_csv = os.path.join(base_dir, 'data/ingredients_table_0408.csv')
        recipe_ingredient_csv = os.path.join(base_dir, 'data/recipes_ingredients_0408.csv')

        # 데이터 불러오기
        recipes = pd.read_csv(recipe_csv, encoding='utf-8-sig')
        ingredients = pd.read_csv(ingredient_csv, encoding='utf-8-sig')
        recipe_ingredient = pd.read_csv(recipe_ingredient_csv, encoding='utf-8-sig')

        # 전처리 및 벡터화
        recipe_ingredient_grouped = recipe_ingredient.groupby('rcp_number')['ingredient_name'].apply(lambda x: ' '.join(x)).reset_index()
        recipe_ingredient_grouped = recipe_ingredient_grouped.merge(
    recipes[['rcp_number', 'rcp_name', 'rcp_picture']],
    on='rcp_number',
    how='left'
)


        vectorizer = CountVectorizer()
        ingredient_matrix = vectorizer.fit_transform(recipe_ingredient_grouped['ingredient_name'])

        user_input_str = ' '.join(user_ingredients)
        user_vector = vectorizer.transform([user_input_str])

        similarity_scores = cosine_similarity(user_vector, ingredient_matrix)
        top_indices = similarity_scores[0].argsort()[::-1][:10]

        recommended = recipe_ingredient_grouped.iloc[top_indices][['rcp_number', 'rcp_name', 'rcp_picture']]

        return Response(recommended.to_dict(orient='records'), status=status.HTTP_200_OK)
