# Generated by Django 4.1.6 on 2023-02-09 14:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0005_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='follow_requests',
            field=models.ManyToManyField(blank=True, related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='pages', to='coreapp.tag'),
        ),
    ]