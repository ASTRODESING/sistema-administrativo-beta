# Generated by Django 4.2.1 on 2023-05-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("login", "0006_alter_datosempresa_telefono"),
    ]

    operations = [
        migrations.AddField(
            model_name="datosempresa",
            name="ci_rif",
            field=models.IntegerField(default=0),
        ),
    ]
