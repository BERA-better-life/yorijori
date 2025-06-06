# Generated by Django 4.2.20 on 2025-03-22 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                ("rcp_seq", models.IntegerField(primary_key=True, serialize=False)),
                ("rcp_nm", models.CharField(max_length=255)),
                ("rcp_way2", models.CharField(max_length=100)),
                ("rcp_pat2", models.CharField(max_length=100)),
                ("info_wgt", models.CharField(blank=True, max_length=50, null=True)),
                ("info_eng", models.IntegerField(blank=True, null=True)),
                (
                    "info_car",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "info_pro",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "info_fat",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "info_na",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ("hash_tag", models.TextField(blank=True, null=True)),
                ("att_file_no_main", models.TextField(blank=True, null=True)),
                ("att_file_no_mk", models.TextField(blank=True, null=True)),
                ("rcp_parts_dtls", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
