# Generated by Django 4.1.4 on 2022-12-30 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_order_order_void'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting_id', models.CharField(max_length=100)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('currency', models.CharField(blank=True, max_length=100, null=True)),
                ('setting_created', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
