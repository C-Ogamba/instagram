# Generated by Django 4.0.5 on 2022-06-08 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instaclone', '0007_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
