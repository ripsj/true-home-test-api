# Generated by Django 2.2.2 on 2020-08-06 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='prev',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='title',
            field=models.CharField(default='title', max_length=250),
            preserve_default=False,
        ),
    ]
