from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from .models import Recipes
from .serializers import IngredientInputSerializer


class RecipeRecommendAPIView(APIView):
    def post(self, request):
        try:
            serializer = IngredientInputSerializer(data=request.data)
            if serializer.is_valid():
                ingredients = serializer.validated_data['ingredients']
                recipes = Recipes.objects.all().values(
                    'rcp_number', 'rcp_name', 'rcp_method', 'rcp_keyword','rcp_type', 'rcp_ingredient', 'rcp_keyword', 
                    'rcp_picture', 'rcp_cooktime', 'rcp_laststep', 'rcp_ingredient_cnt'
                )
                recipes = [recipe for recipe in recipes if recipe['rcp_ingredient']]  # 빈 값 필터링       
                df = pd.DataFrame(recipes)

                tfidf = TfidfVectorizer()
                tfidf_matrix = tfidf.fit_transform(df['rcp_ingredient'].tolist() + [ingredients])

                cosine_sim = linear_kernel(tfidf_matrix[-1:], tfidf_matrix[:-1])
                sim_scores = list(enumerate(cosine_sim[0]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                top_indices = [i[0] for i in sim_scores[:100]]

                # 결과 반환 시 필요한 모든 필드를 포함시킴
                result = df.iloc[top_indices][[
                    'rcp_number', 'rcp_name', 'rcp_method', 'rcp_keyword','rcp_type', 'rcp_ingredient', 'rcp_keyword', 
                    'rcp_picture', 'rcp_cooktime', 'rcp_laststep', 'rcp_ingredient_cnt'
                ]].to_dict(orient='records')
                return Response(result, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
