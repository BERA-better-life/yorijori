from django.db import models
from users.models import Users

class Ingredients(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = True
        db_table = 'Ingredients'

class ExcludedIngredients(models.Model):
    excluded_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    ingredient = models.ForeignKey(Ingredients, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Excluded_Ingredients'


class UserIngredients(models.Model):
    user_ingredient_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    ingredient = models.ForeignKey(Ingredients, models.DO_NOTHING, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'User_Ingredients'



