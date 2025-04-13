from django.db import models
from ingredients.models import Ingredients
from recipes.models import Recipes
from users.models import Users
# Create your models here.

class ShoppingList(models.Model):
    shopping_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    rcp_number = models.ForeignKey(Recipes, models.DO_NOTHING, db_column='rcp_number', blank=True, null=True)
    ingredient_id = models.ForeignKey(Ingredients, models.DO_NOTHING, blank=True, null=True)
