# Generated by Django 3.0.8 on 2020-07-14 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200714_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paradaslinha',
            name='linha',
        ),
        migrations.AddField(
            model_name='paradaslinha',
            name='linha',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Linha'),
        ),
    ]