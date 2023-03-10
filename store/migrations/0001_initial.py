# Generated by Django 4.1.4 on 2022-12-20 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=100)),
                ('store_address', models.CharField(max_length=100)),
                ('store_manager', models.CharField(max_length=100)),
                ('store_image', models.ImageField(blank=True, upload_to='store_images')),
            ],
        ),
    ]
