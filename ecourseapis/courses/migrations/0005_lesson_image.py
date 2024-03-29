# Generated by Django 5.0.3 on 2024-03-26 08:31

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_user_avatar_alter_lesson_course_alter_tag_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='image',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255),
        ),
    ]
