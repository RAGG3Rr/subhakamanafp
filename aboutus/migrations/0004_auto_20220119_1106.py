# Generated by Django 3.2 on 2022-01-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutus', '0003_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
