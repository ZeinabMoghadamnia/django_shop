# Generated by Django 4.2.7 on 2024-01-15 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_brand_discount_alter_category_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=20, unique=True, verbose_name='slug'),
        ),
    ]