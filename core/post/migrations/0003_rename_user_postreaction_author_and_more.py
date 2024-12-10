# Generated by Django 5.1.3 on 2024-12-09 10:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='postreaction',
            old_name='user',
            new_name='author',
        ),
        migrations.AlterUniqueTogether(
            name='postreaction',
            unique_together={('author', 'post')},
        ),
    ]