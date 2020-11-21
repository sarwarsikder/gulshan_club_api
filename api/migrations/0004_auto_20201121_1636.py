# Generated by Django 3.0.6 on 2020-11-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201121_1604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noticeboard',
            options={'ordering': ['title', 'message', 'tag', 'created_at', 'updated_at']},
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='event',
            name='image_alt_text',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='noticeboard',
            name='deleted_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
