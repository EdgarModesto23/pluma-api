# Generated by Django 5.0.2 on 2024-02-16 22:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pluma_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="allowed_users",
            field=models.ManyToManyField(
                related_name="board_users", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="note",
            name="board",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="note_board",
                to="pluma_app.board",
            ),
        ),
        migrations.AddField(
            model_name="note",
            name="creator",
            field=models.ForeignKey(
                db_column="email",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="note_creator",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]