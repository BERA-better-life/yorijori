
from django.db import models  
from ingredients.models import Ingredients


class Recipes(models.Model):
    rcp_number = models.IntegerField(primary_key=True)
    rcp_name = models.CharField(max_length=40, blank=True, null=True)
    rcp_method = models.CharField(max_length=200, blank=True, null=True)
    rcp_keyword = models.CharField(max_length=200, blank=True, null=True)
    rcp_allergy = models.CharField(max_length=200, blank=True, null=True)
    rcp_type = models.CharField(max_length=200, blank=True, null=True)
    rcp_ingredient = models.TextField(blank=True, null=True)
    rcp_cooktime = models.IntegerField(blank=True, null=True)
    rcp_picture = models.TextField(blank=True, null=True)
    rcp_laststep = models.IntegerField(blank=True, null=True)
    rcp_ingredient_cnt = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'Recipes'


class RecipeSteps(models.Model):
    step_id = models.AutoField(primary_key=True)
    rcp_number = models.ForeignKey(Recipes, models.DO_NOTHING, db_column='rcp_number', blank=True, null=True)
    step_order = models.IntegerField()
    instruction = models.TextField()
    image_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Recipe_Steps'

class RecipesIngredients(models.Model):
    recipe_ingredient_id = models.AutoField(primary_key=True)
    rcp_number = models.ForeignKey(Recipes, models.DO_NOTHING, db_column='rcp_number', blank=True, null=True)
    ingredient = models.ForeignKey(Ingredients, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Recipes_Ingredients'


