# Generated by Django 4.2.7 on 2023-11-06 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image_url', models.CharField(max_length=200)),
                ('disabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_id', models.CharField(max_length=50)),
                ('amount', models.PositiveIntegerField()),
                ('currency', models.CharField(max_length=3)),
                ('status', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_id', models.CharField(max_length=64)),
                ('meal_id', models.PositiveIntegerField()),
                ('item_name', models.CharField(max_length=100)),
                ('total_price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('done', models.BooleanField(default=False)),
            ],
            options={
                'indexes': [models.Index(fields=['meal_id'], name='meal_idx')],
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_name', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.PositiveIntegerField()),
                ('is_vegetarian', models.BooleanField(default=False)),
                ('is_spicy', models.BooleanField(default=False)),
                ('is_gluten_free', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_service.menucategory')),
            ],
            options={
                'indexes': [models.Index(fields=['item_name'], name='item_name_idx'), models.Index(fields=['category'], name='category_idx')],
            },
        ),
    ]
