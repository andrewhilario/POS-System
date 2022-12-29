# Generated by Django 4.1.4 on 2022-12-28 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_orderitem_order_item_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_number', models.CharField(max_length=100)),
                ('transaction_code', models.CharField(max_length=100)),
                ('transaction_date', models.DateTimeField(blank=True, null=True)),
                ('transaction_total', models.CharField(max_length=100)),
                ('transaction_tax', models.CharField(max_length=100)),
                ('transaction_created', models.DateTimeField(blank=True, null=True)),
                ('transaction_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
    ]
