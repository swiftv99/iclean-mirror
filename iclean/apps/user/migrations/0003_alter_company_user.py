# Generated by Django 4.0.4 on 2022-05-25 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_client_user_alter_company_user_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='companys', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
