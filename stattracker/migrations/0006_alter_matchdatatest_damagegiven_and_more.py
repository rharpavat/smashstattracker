# Generated by Django 4.0.5 on 2022-06-11 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stattracker', '0005_playerstatstest_avgdmggiven_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchdatatest',
            name='damagegiven',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='matchdatatest',
            name='damagetaken',
            field=models.IntegerField(null=True),
        ),
    ]