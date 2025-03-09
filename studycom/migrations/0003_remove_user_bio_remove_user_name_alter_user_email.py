# Generated by Django 5.1.7 on 2025-03-09 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studycom', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
