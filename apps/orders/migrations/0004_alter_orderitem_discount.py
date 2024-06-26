# Generated by Django 4.2.7 on 2024-02-07 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_comment_author'),
        ('orders', '0003_alter_order_discounted_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.discount', verbose_name='discount'),
        ),
    ]
