# Generated by Django 4.2.20 on 2025-03-29 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ingredients", "0001_initial"),
        ("recipes", "0007_delete_recipe"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recipes",
            fields=[
                ("rcp_number", models.IntegerField(primary_key=True, serialize=False)),
                ("rcp_name", models.CharField(blank=True, max_length=40, null=True)),
                ("rcp_method", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "rcp_keyword",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "rcp_allergy",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("rcp_type", models.CharField(blank=True, max_length=200, null=True)),
                ("rcp_ingredient", models.TextField(blank=True, null=True)),
                (
                    "rcp_cooktime",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("rcp_picture", models.TextField(blank=True, null=True)),
            ],
            options={"db_table": "Recipes", "managed": True,},
        ),
        migrations.CreateModel(
            name="RecipeSteps",
            fields=[
                ("step_id", models.AutoField(primary_key=True, serialize=False)),
                ("step_order", models.IntegerField()),
                ("instruction", models.TextField()),
                ("image_url", models.TextField(blank=True, null=True)),
                (
                    "rcp_number",
                    models.ForeignKey(
                        blank=True,
                        db_column="rcp_number",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="recipes.recipes",
                    ),
                ),
            ],
            options={"db_table": "Recipe_Steps", "managed": True,},
        ),
        migrations.CreateModel(
            name="RecipesIngredients",
            fields=[
                (
                    "recipe_ingredient_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="ingredients.ingredients",
                    ),
                ),
                (
                    "rcp_number",
                    models.ForeignKey(
                        blank=True,
                        db_column="rcp_number",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="recipes.recipes",
                    ),
                ),
            ],
            options={"db_table": "Recipes_Ingredients", "managed": True,},
        ),
    ]
