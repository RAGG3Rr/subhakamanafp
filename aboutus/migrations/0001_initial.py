# Generated by Django 3.1.1 on 2021-09-02 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Location', models.CharField(blank=True, max_length=80, null=True)),
                ('phone_no1', models.IntegerField(blank=True, null=True)),
                ('phone_no2', models.IntegerField(blank=True, null=True)),
                ('phone_no3', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Customer_view',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('review_by', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('content', models.TextField()),
                ('title_image', models.ImageField(upload_to='aboutus_images')),
            ],
        ),
        migrations.CreateModel(
            name='OurClients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='aboutus_images')),
            ],
        ),
        migrations.CreateModel(
            name='OurTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('designation', models.CharField(max_length=64)),
                ('short_description', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('upload_image', models.ImageField(upload_to='aboutus_images')),
            ],
        ),
        migrations.CreateModel(
            name='Userquery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=80, null=True)),
                ('lastname', models.CharField(blank=True, max_length=80, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=80, null=True)),
                ('email', models.EmailField(blank=True, max_length=64, null=True)),
                ('subject', models.CharField(blank=True, max_length=80, null=True)),
                ('message', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
    ]
