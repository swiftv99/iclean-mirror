# Generated by Django 4.0.4 on 2022-05-28 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_review_commentslug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='commentslug',
            new_name='slug',
        ),
    ]