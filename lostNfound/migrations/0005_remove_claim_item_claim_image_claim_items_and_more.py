# Generated by Django 4.0.6 on 2023-12-17 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostNfound', '0004_item_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='item',
        ),
        migrations.AddField(
            model_name='claim',
            name='image',
            field=models.ImageField(default='Do.png', max_length=500, upload_to=''),
        ),
        migrations.AddField(
            model_name='claim',
            name='items',
            field=models.ManyToManyField(to='lostNfound.item'),
        ),
        migrations.AddField(
            model_name='claim',
            name='password',
            field=models.CharField(default='X', max_length=100),
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='Do.png', max_length=500, upload_to=''),
        ),
    ]
