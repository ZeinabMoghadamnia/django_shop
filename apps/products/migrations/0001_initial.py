# Generated by Django 4.2.7 on 2024-01-14 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date updated')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='delete status')),
                ('deleted_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date deleted')),
                ('restored_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date restored')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='image')),
                ('slug', models.SlugField(max_length=20, unique=True, verbose_name='slug')),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'brand',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date updated')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='delete status')),
                ('deleted_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date deleted')),
                ('restored_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date restored')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='image')),
                ('slug', models.SlugField(max_length=20, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date updated')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='delete status')),
                ('deleted_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date deleted')),
                ('restored_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date restored')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='discount code')),
                ('discount_type', models.CharField(choices=[('percentage', 'Percent'), ('amount', 'Amount')], max_length=20, verbose_name='discount type')),
                ('value', models.PositiveIntegerField(verbose_name='value')),
            ],
            options={
                'verbose_name': 'discount code',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date updated')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='delete status')),
                ('deleted_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date deleted')),
                ('restored_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date restored')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='image')),
                ('discounted_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='discounted price')),
                ('slug', models.SlugField(max_length=20, unique=True, verbose_name='slug')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='brands', to='products.brand', verbose_name='brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='products.category', verbose_name='category')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='discounts', to='products.discount', verbose_name='discount')),
            ],
            options={
                'verbose_name': 'product',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date updated')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='delete status')),
                ('deleted_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date deleted')),
                ('restored_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date restored')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='products.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_who_liked', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'likes',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date updated')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='delete status')),
                ('deleted_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date deleted')),
                ('restored_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date restored')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('sub_image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='gallery')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='products.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'images',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date updated')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='delete status')),
                ('deleted_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date deleted')),
                ('restored_at', models.DateTimeField(auto_now=True, null=True, verbose_name='date restored')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('context', models.TextField(verbose_name='content')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authors', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='products.product', verbose_name='product')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='products.comment', verbose_name='reply')),
            ],
            options={
                'verbose_name': 'comments',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.discount', verbose_name='discount'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.category', verbose_name='parent category'),
        ),
        migrations.AddField(
            model_name='brand',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.discount', verbose_name='discount'),
        ),
    ]
