# Generated by Django 4.1.4 on 2022-12-28 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_products',
            field=models.ManyToManyField(blank=True, related_name='order_products', to='store.product'),
        ),
    ]