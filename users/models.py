from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# Create your models here.
class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password = models.TextField()
    USERNAME_FIELD = 'email'  #참고 : https://velog.io/@subb_ny/type-object-User-has-no-attribute-USERNAMEFIELD
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'Users'
