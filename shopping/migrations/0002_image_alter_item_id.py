# Generated by Django 4.1.7 on 2023-04-04 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='shopping.item', unique=True)),
                ('link', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.TextField(primary_key=True, serialize=False, unique=True),
        ),
    ]
