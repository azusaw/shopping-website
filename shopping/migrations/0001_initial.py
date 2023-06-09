# Generated by Django 4.1.7 on 2023-04-04 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='BaseColour',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('hex_code', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MasterCategory',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('season', models.TextField()),
                ('year', models.IntegerField()),
                ('usage', models.TextField()),
                ('display_name', models.TextField()),
                ('article_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.articletype')),
                ('base_colour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.basecolour')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.gender')),
                ('master_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.mastercategory')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.subcategory')),
            ],
        ),
    ]
