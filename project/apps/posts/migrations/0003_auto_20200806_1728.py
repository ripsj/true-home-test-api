# Generated by Django 2.2.2 on 2020-08-06 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200806_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Subcategory'),
        ),
    ]
