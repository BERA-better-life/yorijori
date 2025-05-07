from rest_framework import serializers
from .models import RecipeSteps

class IngredientInputSerializer(serializers.Serializer):
    ingredients = serializers.CharField(help_text="입력 재료들을 쉼표로 구분한 문자열")
    sort_by = serializers.CharField(required=False, allow_blank=True)

class IngredientInputSerializer(serializers.Serializer):
    ingredients = serializers.CharField()
    excluded_ingredients = serializers.CharField(required=False, allow_blank=True)



class RecipeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeSteps
        fields = ['step_order', 'instruction', 'image_url']
