# Generated by Django 4.2.1 on 2023-05-22 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("login", "0004_alter_preciodolar_precio"),
    ]

    operations = [
        migrations.CreateModel(
            name="DatosEmpresa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=255)),
                ("direccion", models.TextField()),
                ("telefono", models.IntegerField(max_length=11)),
                ("correo", models.EmailField(max_length=254)),
            ],
        ),
    ]
