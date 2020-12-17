# Generated by Django 3.0.6 on 2020-12-17 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'active'), ('Inactive', 'inactive')], default='inactive', max_length=50, null=True),
        ),
    ]
