# Generated by Django 4.2.1 on 2023-05-19 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("compras", "0004_perdida"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ordendecompra",
            name="numero_orden",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
