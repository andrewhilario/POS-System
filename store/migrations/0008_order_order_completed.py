# Generated by Django 4.1.4 on 2022-12-26 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_completed',
            field=models.BooleanField(default=False),
        ),
    ]
