# Generated by Django 4.0.4 on 2022-05-16 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='type_of_notification',
        ),
    ]