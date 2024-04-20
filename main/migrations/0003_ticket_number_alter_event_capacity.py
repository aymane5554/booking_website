# Generated by Django 4.1.3 on 2024-04-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_event_tickets_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='event',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
    ]
