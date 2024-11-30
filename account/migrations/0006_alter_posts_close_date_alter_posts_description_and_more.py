# Generated by Django 5.1 on 2024-11-30 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_posts_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='close_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
