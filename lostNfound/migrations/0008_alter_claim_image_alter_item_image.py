# Generated by Django 4.0.6 on 2023-12-18 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostNfound', '0007_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='image',
            field=models.TextField(default='default.png', max_length=1000),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.TextField(default='default.png', max_length=1000),
        ),
    ]
