# Generated by Django 5.0.4 on 2024-04-11 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_student_last_participation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="discord_id",
            field=models.BigIntegerField(),
        ),
    ]
