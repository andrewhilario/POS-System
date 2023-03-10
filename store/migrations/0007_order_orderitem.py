# Generated by Django 4.1.4 on 2022-12-24 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_remove_product_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField(blank=True, null=True)),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_created', models.DateTimeField(blank=True, null=True)),
                ('order_products', models.ManyToManyField(to='store.product')),
                ('order_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_item_id', models.CharField(max_length=100)),
                ('order_item_quantity', models.IntegerField()),
                ('order_item_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_item_created', models.DateTimeField(blank=True, null=True)),
                ('order_item_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('order_item_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
