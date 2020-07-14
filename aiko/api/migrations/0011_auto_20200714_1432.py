# Generated by Django 3.0.8 on 2020-07-14 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200714_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paradas',
            name='lat_parada',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='paradas',
            name='long_parada',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='posicaoveiculos',
            name='lat_veiculo',
            field=models.BigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='posicaoveiculos',
            name='long_veiculo',
            field=models.BigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='posicaoveiculos',
            name='veiculo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posicao', to='api.Veiculo'),
        ),
    ]
