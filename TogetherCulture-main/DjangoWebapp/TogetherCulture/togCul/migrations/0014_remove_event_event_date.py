# Generated by Django 5.1.7 on 2025-04-08 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('togCul', '0013_alter_event_event_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_date',
        ),
    ]
