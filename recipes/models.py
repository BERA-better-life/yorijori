from django.db import models

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100)

    def __str__(self):
        return self.ingredient_name

class Recipe(models.Model):
    rcp_number = models.CharField(max_length=50, unique=True)
    rcp_name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.rcp_name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
