# Generated by Django 4.1.7 on 2023-02-22 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coreapp", "0006_alter_page_description_alter_page_follow_requests_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(choices=[("user", "User"), ("moderator", "Moderator"), ("admin", "Admin")], default="user", max_length=9),
        ),
    ]
