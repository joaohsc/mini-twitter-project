# Generated by Django 5.1.2 on 2024-10-27 18:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 27, 15, 17, 26, 971746)),
        ),
    ]