# Generated by Django 3.1.7 on 2021-10-11 01:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_remove_blog_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='bookmark',
            field=models.ManyToManyField(blank=True, related_name='bookmark', to=settings.AUTH_USER_MODEL),
        ),
    ]
