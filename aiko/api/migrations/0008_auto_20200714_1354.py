# Generated by Django 3.0.8 on 2020-07-14 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_linha_paradas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paradas',
            name='lat_parada',
            field=models.BigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='paradas',
            name='long_parada',
            field=models.BigIntegerField(blank=True),
        ),
    ]