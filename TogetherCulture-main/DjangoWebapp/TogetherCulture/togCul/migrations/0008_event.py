# Generated by Django 5.1.7 on 2025-04-08 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('togCul', '0007_userbenefits_userinterests'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(blank=True, editable=False, max_length=12, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
    ]
