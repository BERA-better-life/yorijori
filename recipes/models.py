
from django.db import models  

class Recipe(models.Model):
    rcp_seq = models.IntegerField(primary_key=True)
    rcp_nm = models.CharField(max_length=255)
    rcp_way2 = models.CharField(max_length=100)
    rcp_pat2 = models.CharField(max_length=100)
    info_wgt = models.IntegerField( null=True, blank=True)
    info_eng = models.IntegerField( null=True, blank=True)
    info_car = models.IntegerField( null=True, blank=True)
    info_pro = models.IntegerField( null=True, blank=True)
    info_fat = models.IntegerField( null=True, blank=True)
    info_na = models.IntegerField( null=True, blank=True)
    hash_tag = models.TextField(null=True, blank=True)
    att_file_no_main = models.TextField(null=True, blank=True)
    att_file_no_mk = models.TextField(null=True, blank=True)
    rcp_parts_dtls = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.rcp_nm

