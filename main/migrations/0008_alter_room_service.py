# Generated by Django 3.2.12 on 2023-04-02 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_bron_cancel_date_alter_bron_canceller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_rooms', to='main.service'),
        ),
    ]
