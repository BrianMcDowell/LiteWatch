# Generated by Django 4.1 on 2022-11-30 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lw', '0003_result_sample_result_sent_result_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='elemattr',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='search',
            name='elemtype',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
