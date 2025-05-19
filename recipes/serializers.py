from rest_framework import serializers
from .models import RecipeSteps

class IngredientInputSerializer(serializers.Serializer):
    ingredients = serializers.CharField(required=False, allow_blank=True)
    rcp_keyword = serializers.ListField(child=serializers.CharField(), required=False)
    rcp_type = serializers.ListField(child=serializers.CharField(), required=False)
    sort_by = serializers.CharField(required=False, allow_blank=True)

class IngredientInputSerializerWithExcluded(serializers.Serializer):
    ingredients = serializers.CharField()
    excluded_ingredients = serializers.CharField(required=False, allow_blank=True)


class RecipeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeSteps
        fields = ['step_order', 'instruction', 'image_url']
