# Generated by Django 4.0.5 on 2022-06-13 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stattracker', '0010_alter_leaderboard_statistic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaderboard',
            name='id',
        ),
        migrations.AlterField(
            model_name='leaderboard',
            name='statistic',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]