# Generated by Django 3.2 on 2022-01-14 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20220114_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='sub_category',
            field=models.CharField(max_length=50),
        ),
    ]
