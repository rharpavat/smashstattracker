# Generated by Django 4.0.5 on 2022-06-12 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stattracker', '0009_leaderboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboard',
            name='statistic',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
