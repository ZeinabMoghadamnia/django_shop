# Generated by Django 4.2.7 on 2024-01-13 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_discounted_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
