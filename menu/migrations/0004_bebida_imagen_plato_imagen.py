# Generated by Django 5.1.6 on 2025-03-18 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0003_remove_bebida_id_remove_plato_id_bebida_nombre_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bebida",
            name="imagen",
            field=models.ImageField(blank=True, null=True, upload_to="bebidas/"),
        ),
        migrations.AddField(
            model_name="plato",
            name="imagen",
            field=models.ImageField(blank=True, null=True, upload_to="platos/"),
        ),
    ]
