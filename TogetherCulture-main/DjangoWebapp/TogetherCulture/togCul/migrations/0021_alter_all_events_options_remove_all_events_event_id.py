# Generated by Django 5.1.7 on 2025-04-08 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('togCul', '0020_rename_events_all_events'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='all_events',
            options={'verbose_name': 'All event', 'verbose_name_plural': 'All events'},
        ),
        migrations.RemoveField(
            model_name='all_events',
            name='event_id',
        ),
    ]
