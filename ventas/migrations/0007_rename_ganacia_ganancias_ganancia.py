# Generated by Django 4.2.1 on 2023-05-19 18:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ventas", "0006_ganancias_numerodeclientes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ganancias",
            old_name="ganacia",
            new_name="ganancia",
        ),
    ]
