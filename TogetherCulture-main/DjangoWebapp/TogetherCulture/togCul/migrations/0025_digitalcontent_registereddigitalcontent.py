# Generated by Django 5.2 on 2025-04-10 01:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("togCul", "0024_rename_all_events_allevents_alter_allevents_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="DigitalContent",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("contentName", models.CharField(max_length=255)),
                ("contentDescription", models.TextField()),
                ("createdDate", models.DateField(auto_now_add=True)),
                (
                    "accessBy",
                    models.CharField(
                        choices=[("T1", "Tier 1"), ("T2", "Tier 2"), ("T3", "Tier 3")],
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RegisteredDigitalContent",
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
                ("registeredDate", models.DateField(auto_now_add=True)),
                (
                    "digitalContent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="togCul.digitalcontent",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="togCul.customuser",
                    ),
                ),
            ],
        ),
    ]
