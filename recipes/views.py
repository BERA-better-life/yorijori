from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from .models import Recipes, RecipeSteps, UserIngredients
from .serializers import IngredientInputSerializerWithExcluded
from .serializers import IngredientInputSerializer
from .serializers import RecipeDetailSerializer
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_ingredients(request):
    user = request.user
    user_ingredients = UserIngredients.objects.filter(user_id=user).select_related('ingredient_id')
    ingredient_names = [ui.ingredient_id.ingredient_name for ui in user_ingredients if ui.ingredient_id]
    return Response({"ingredients": ingredient_names})

def sort_recipes(recipes, sort_by):
    def safe_int(val, default):
        try:
            return int(val)
        except (TypeError, ValueError):
            return default
        
    if sort_by == "rcp_cooktime_asc": # 조리시간 짧은 순
        return sorted(recipes, key=lambda x: int(x.get("rcp_cooktime", 9999)))
    elif sort_by == "rcp_cooktime_desc": # 조리시간 오래걸리는 순
        return sorted(recipes, key=lambda x: int(x.get("rcp_cooktime", 0)), reverse=True)
    elif sort_by == "rcp_ingredient_cnt_asc": # 재료 수 적은 순
        return sorted(recipes, key=lambda x: int(x.get("rcp_ingredient_cnt", 999)))
    elif sort_by == "rcp_ingredient_cnt_desc": # 재료 수 많은 순
        return sorted(recipes, key=lambda x: int(x.get("rcp_ingredient_cnt", 0)), reverse=True)
    elif sort_by == "likes_desc": # 좋아요 많은 순 정렬 (0515 아현)
        from favorite.models import Likes
        like_counts = Likes.objects.values('rcp_number').annotate(count=Count('rcp_number'))
        like_count_map = {item['rcp_number']: item['count'] for item in like_counts}
        return sorted(recipes, key=lambda x: like_count_map.get(x['rcp_number'], 0), reverse=True)
    elif sort_by == "likes_asc": # 좋아요 적은 순 정렬 (0515 아현)
        from favorite.models import Likes
        like_counts = Likes.objects.values('rcp_number').annotate(count=Count('rcp_number'))
        like_count_map = {item['rcp_number']: item['count'] for item in like_counts}
        return sorted(recipes, key=lambda x: like_count_map.get(x['rcp_number'], 0))
    return recipes  # sort_by가 없거나 잘못된 경우, 기본 순서로 반환


class RecipeRecommendAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = IngredientInputSerializer(data=request.data)
            if serializer.is_valid():
                # 1) 클라이언트가 직접 입력한 재료 (옵션)
                ingredients = serializer.validated_data.get('ingredients', '').strip()

                # 2) 로그인 했으면 재료 없을 때 저장 재료 불러오기
                if request.user.is_authenticated and not ingredients:
                    user_ingredients = UserIngredients.objects.filter(user_id=request.user).select_related('ingredient_id')
                    ingredients_list = [ui.ingredient_id.ingredient_name for ui in user_ingredients if ui.ingredient_id]
                    ingredients = ", ".join(ingredients_list)

                 # 3) 재료가 여전히 없으면 에러 반환
                if not ingredients:
                    return Response({"error": "재료가 입력되지 않았고, 저장된 재료도 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

                sort_by = request.data.get("sort_by", "").strip()

                # 다중 선택 필터 리스트 처리
                rcp_keywords = request.data.get("rcp_keyword", [])
                rcp_types = request.data.get("rcp_type", [])

                if isinstance(rcp_keywords, str):
                    rcp_keywords = [rcp_keywords]
                if isinstance(rcp_types, str):
                    rcp_types = [rcp_types]

                recipes = Recipes.objects.all().values(
                    'rcp_number', 'rcp_name', 'rcp_method', 'rcp_keyword','rcp_type', 'rcp_ingredient', 
                    'rcp_picture', 'rcp_cooktime', 'rcp_laststep', 'rcp_ingredient_cnt'
                )
                recipes = [recipe for recipe in recipes if recipe['rcp_ingredient']]
                df = pd.DataFrame(recipes)

                tfidf = TfidfVectorizer()
                tfidf_matrix = tfidf.fit_transform(df['rcp_ingredient'].tolist() + [ingredients])

                cosine_sim = linear_kernel(tfidf_matrix[-1:], tfidf_matrix[:-1])
                sim_scores = list(enumerate(cosine_sim[0]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                top_indices = [i[0] for i in sim_scores[:100]]

                result = df.iloc[top_indices][[
                    'rcp_number', 'rcp_name', 'rcp_method', 'rcp_keyword','rcp_type', 'rcp_ingredient',  
                    'rcp_picture', 'rcp_cooktime', 'rcp_laststep', 'rcp_ingredient_cnt'
                ]].to_dict(orient='records')

                #다중 조건 필터 적용 (and 조건)
                if rcp_keywords and rcp_types:
                    result = [r for r in result if r.get('rcp_keyword') in rcp_keywords and r.get('rcp_type') in rcp_types]
                elif rcp_keywords:
                    result = [r for r in result if r.get('rcp_keyword') in rcp_keywords]
                elif rcp_types:
                    result = [r for r in result if r.get('rcp_type') in rcp_types]

                result = sort_recipes(result, sort_by)

                return Response(result, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
class RecipeRecommendWithExcludedAPIView(APIView):
    def post(self, request):
        try:
            serializer = IngredientInputSerializerWithExcluded(data=request.data)
            if serializer.is_valid():
                ingredients = serializer.validated_data['ingredients']
                excluded_ingredients = serializer.validated_data.get('excluded_ingredients', '')
                sort_by = request.data.get("sort_by", "").strip()

                # 다중 선택 필터 리스트 처리
                rcp_keywords = request.data.get("rcp_keyword", [])
                rcp_types = request.data.get("rcp_type", [])

                if isinstance(rcp_keywords, str):
                    rcp_keywords = [rcp_keywords]
                if isinstance(rcp_types, str):
                    rcp_types = [rcp_types]

                recipes = Recipes.objects.all().values(
                    'rcp_number', 'rcp_name', 'rcp_method', 'rcp_keyword', 'rcp_type', 'rcp_ingredient', 
                    'rcp_picture', 'rcp_cooktime', 'rcp_laststep', 'rcp_ingredient_cnt'
                )
                recipes = [recipe for recipe in recipes if recipe['rcp_ingredient']]
                df = pd.DataFrame(recipes)

                # TF-IDF 벡터화
                tfidf = TfidfVectorizer()
                all_text = df['rcp_ingredient'].tolist() + [ingredients]
                tfidf_matrix = tfidf.fit_transform(all_text)

                cosine_sim = linear_kernel(tfidf_matrix[-1:], tfidf_matrix[:-1])
                sim_scores = list(enumerate(cosine_sim[0]))

                # 제외할 재료가 포함된 레시피는 유사도 0으로 설정
                excluded_words = [word.strip() for word in excluded_ingredients.split(',') if word.strip()]
                for i, recipe in enumerate(df['rcp_ingredient']):
                    if any(ex in recipe for ex in excluded_words):
                        sim_scores[i] = (i, 0.0)

                # 유사도 순 정렬 및 상위 100개 선택
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                top_indices = [i[0] for i in sim_scores[:100] if i[1] > 0]

                result = df.iloc[top_indices][[
                    'rcp_number', 'rcp_name', 'rcp_method', 'rcp_keyword', 'rcp_type', 'rcp_ingredient', 
                    'rcp_picture', 'rcp_cooktime', 'rcp_laststep', 'rcp_ingredient_cnt'
                ]].to_dict(orient='records')

                #다중 조건 필터 적용 (and 조건)
                if rcp_keywords and rcp_types:
                    result = [r for r in result if r.get('rcp_keyword') in rcp_keywords and r.get('rcp_type') in rcp_types]
                elif rcp_keywords:
                    result = [r for r in result if r.get('rcp_keyword') in rcp_keywords]
                elif rcp_types:
                    result = [r for r in result if r.get('rcp_type') in rcp_types]
                
                result = sort_recipes(result, sort_by)

                return Response(result, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class RecipeDetailAPIView(APIView):
    def get(self, request, rcp_number):
        try:
            recipe = Recipes.objects.filter(rcp_number=rcp_number).first()
            if not recipe:
                return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

            steps = RecipeSteps.objects.filter(rcp_number=rcp_number).order_by('step_order')
            steps_serializer = RecipeDetailSerializer(steps, many=True)

            recipe_data = {
                "rcp_number": recipe.rcp_number,
                "rcp_name": recipe.rcp_name,
                "rcp_method": recipe.rcp_method,
                "rcp_keyword": recipe.rcp_keyword,
                "rcp_type": recipe.rcp_type,
                "rcp_ingredient": recipe.rcp_ingredient,
                "rcp_picture": recipe.rcp_picture,
                "rcp_cooktime": recipe.rcp_cooktime,
                "rcp_laststep": recipe.rcp_laststep,
                "rcp_ingredient_cnt": recipe.rcp_ingredient_cnt,
                "steps": steps_serializer.data
            }

            return Response(recipe_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)