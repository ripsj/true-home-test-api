# Generated by Django 2.2.2 on 2020-08-06 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('disabled_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Disabled at')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('name', models.CharField(max_length=75)),
                ('slug', models.CharField(max_length=75, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('disabled_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Disabled at')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('name', models.CharField(max_length=75)),
                ('slug', models.CharField(max_length=75, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]