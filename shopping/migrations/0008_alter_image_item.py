# Generated by Django 4.1.7 on 2023-04-10 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0007_order_total_price_orderitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='shopping.item'),
        ),
    ]