# Generated by Django 5.1.7 on 2025-04-08 14:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('togCul', '0008_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
