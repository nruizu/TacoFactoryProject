# Generated by Django 5.0.7 on 2025-03-19 05:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_remove_bebida_id_remove_plato_id_bebida_nombre_and_more'),
        ('orden', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orden',
            old_name='fecha',
            new_name='fecha_creacion',
        ),
        migrations.RenameField(
            model_name='orden',
            old_name='total',
            new_name='monto_total',
        ),
        migrations.RemoveField(
            model_name='orden',
            name='cvv',
        ),
        migrations.AlterField(
            model_name='orden',
            name='metodo_pago',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='OrdenBebida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('bebida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.bebida')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orden.orden')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenPlato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orden.orden')),
                ('plato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.plato')),
            ],
        ),
        migrations.DeleteModel(
            name='ItemOrden',
        ),
    ]
