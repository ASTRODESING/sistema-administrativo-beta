# Generated by Django 4.1.7 on 2023-03-18 01:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("login", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usuario",
            name="prueba",
        ),
        migrations.AddField(
            model_name="usuario",
            name="is_cajero",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="usuario",
            name="is_gerente",
            field=models.BooleanField(default=False),
        ),
    ]
