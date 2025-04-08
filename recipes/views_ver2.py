import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from .serializers import RecipeSerializer

class RecipeRecommendationView(APIView):
    def post(self, request):
        user_ingredients = request.data.get('ingredients', [])
        excluded_ingredients = request.data.get('excluded_ingredients', [])

        if not user_ingredients:
            return Response({'error': 'ingredients are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # CSV 파일 경로 설정 (settings.py와 같은 위치 기준)
        base_dir = settings.BASE_DIR
        recipe_csv = os.path.join(base_dir, 'data/recipes_table_0408.csv')
        ingredient_csv = os.path.join(base_dir, 'data/ingredients_table_0408.csv')
        recipe_ingredient_csv = os.path.join(base_dir, 'data/recipes_ingredients_0408.csv')

        # 데이터 불러오기
        recipes = pd.read_csv(recipe_csv, encoding='utf-8-sig')
        ingredient_data = pd.read_csv(ingredient_csv, encoding='utf-8-sig')
        recipe_ingredient = pd.read_csv(recipe_ingredient_csv, encoding='utf-8-sig')

        # 레시피별로 재료 이름을 하나의 문자열로 합치기
        recipe_ingredient_grouped = recipe_ingredient.groupby('rcp_number')['ingredient_name'].apply(lambda x: ' '.join(x)).reset_index()

        # 레시피 이름 붙이기
        recipe_ingredient_grouped = recipe_ingredient_grouped.merge(
            recipes[['rcp_number', 'rcp_name', 'rcp_picture']],
            on='rcp_number',
            how='left'
        )

        # CountVectorizer로 벡터화
        vectorizer = CountVectorizer()
        ingredient_matrix = vectorizer.fit_transform(recipe_ingredient_grouped['ingredient_name'])

        # 사용자 입력 벡터화
        user_input_str = ' '.join(user_ingredients)
        user_vector = vectorizer.transform([user_input_str])

        # 제외할 재료의 인덱스를 찾아서 벡터에서 0으로 설정
        excluded_indices = [vectorizer.vocabulary_.get(ingredient) for ingredient in excluded_ingredients if vectorizer.vocabulary_.get(ingredient) is not None]
        for idx in excluded_indices:
            user_vector[0, idx] = 0  # 해당 인덱스를 0으로 설정

        # 코사인 유사도 계산
        similarity_scores = cosine_similarity(user_vector, ingredient_matrix)

        # 상위 N개 인덱스 추출 (기본값은 10개)
        top_indices = similarity_scores[0].argsort()[::-1][:10]

        # 추천 결과
        recommended = recipe_ingredient_grouped.iloc[top_indices][['rcp_number', 'rcp_name', 'rcp_picture']]

        # 추천된 레시피를 Serializer로 직렬화
        serializer = RecipeSerializer(recommended, many=True)

        # 추천 레시피 반환
        return Response(recommended.to_dict(orient='records'), status=status.HTTP_200_OK)
