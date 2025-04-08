from django.db import models
from ingredients.models import Ingredients
from recipes.models import Recipe
from users.models import Users
# Create your models here.

class ShoppingList(models.Model):
    shopping_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    rcp_number = models.ForeignKey(Recipe, models.DO_NOTHING, db_column='rcp_number', blank=True, null=True)
    ingredient = models.ForeignKey(Ingredients, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Shopping_List'