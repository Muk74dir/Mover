# Generated by Django 4.2.7 on 2023-12-08 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MoverApp', '0004_paymentgatewaysettingsmodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TripRequestModel',
        ),
    ]
