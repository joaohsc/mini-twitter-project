# Generated by Django 5.1.2 on 2024-10-27 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_profile_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]