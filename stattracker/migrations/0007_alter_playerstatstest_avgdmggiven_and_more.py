# Generated by Django 4.0.5 on 2022-06-11 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stattracker', '0006_alter_matchdatatest_damagegiven_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerstatstest',
            name='avgdmggiven',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='playerstatstest',
            name='avgdmgtaken',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]