# Generated by Django 4.2.7 on 2024-02-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='discounted_total_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='discounted total price'),
        ),
    ]
