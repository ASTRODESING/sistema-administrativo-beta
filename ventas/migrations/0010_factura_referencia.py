# Generated by Django 4.2.1 on 2023-05-23 12:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ventas", "0009_alter_ganancias_dia_alter_numerodeclientes_dia"),
    ]

    operations = [
        migrations.AddField(
            model_name="factura",
            name="referencia",
            field=models.IntegerField(null=True),
        ),
    ]
