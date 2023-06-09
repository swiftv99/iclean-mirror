# Generated by Django 4.0.4 on 2022-06-09 14:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reviews', to='user.client')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='user.company')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
