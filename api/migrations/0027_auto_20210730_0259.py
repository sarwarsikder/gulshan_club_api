# Generated by Django 3.0.6 on 2021-07-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20210730_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
