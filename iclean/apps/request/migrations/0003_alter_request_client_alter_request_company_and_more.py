# Generated by Django 4.0.4 on 2022-05-25 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_service_company'),
        ('user', '0002_alter_client_user_alter_company_user_alter_user_role'),
        ('request', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='user.client'),
        ),
        migrations.AlterField(
            model_name='request',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='user.company'),
        ),
        migrations.AlterField(
            model_name='request',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='service.service'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='requests', to='request.request_status'),
        ),
    ]
