# Generated by Django 4.1.7 on 2023-03-01 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0009_page_is_blocked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='is_blocked',
        ),
        migrations.AddField(
            model_name='page',
            name='is_permanently_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
