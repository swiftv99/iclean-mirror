# Generated by Django 4.0.4 on 2022-05-12 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notification', '0001_initial'),
        ('user', '0001_initial'),
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.company'),
        ),
        migrations.AddField(
            model_name='notification',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.request'),
        ),
    ]