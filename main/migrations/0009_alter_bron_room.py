# Generated by Django 3.2.12 on 2023-04-02 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_room_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bron',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_brons', to='main.room'),
        ),
    ]