# Generated by Django 3.0.6 on 2020-11-26 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20201126_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='designation',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
