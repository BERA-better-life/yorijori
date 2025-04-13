from django.db import models
from users.models import Users
from recipes.models import Recipes

# Create your models here.
class Bookmarks(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    rcp_number = models.ForeignKey(Recipes, models.DO_NOTHING, db_column='rcp_number', blank=True, null=True)




class Likes(models.Model):
    like_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    rcp_number = models.ForeignKey(Recipes, models.DO_NOTHING, db_column='rcp_number', blank=True, null=True)

