# Generated by Django 3.0.6 on 2021-07-29 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_reservation_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
