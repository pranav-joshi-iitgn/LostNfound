# Generated by Django 4.0.6 on 2023-12-20 01:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lostNfound', '0011_remove_claim_contact_remove_claim_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='location',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
