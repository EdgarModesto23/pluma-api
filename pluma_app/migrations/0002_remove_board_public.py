# Generated by Django 5.0.2 on 2024-02-19 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pluma_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='public',
        ),
    ]
