# Generated by Django 4.1.3 on 2024-04-20 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rank_cmnt'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='password',
            field=models.CharField(default='no password', max_length=20),
            preserve_default=False,
        ),
    ]
