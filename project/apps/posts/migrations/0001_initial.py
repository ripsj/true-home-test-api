# Generated by Django 2.2.2 on 2020-08-06 21:09

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('disabled_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Disabled at')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('slug', models.CharField(max_length=250, unique=True)),
                ('title', models.CharField(max_length=250, null=True)),
                ('body', models.TextField()),
                ('tags', django.contrib.postgres.fields.jsonb.JSONField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Subcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
