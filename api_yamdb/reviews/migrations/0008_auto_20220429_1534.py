# Generated by Django 2.2.16 on 2022-04-29 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_merge_20220429_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title'),
        ),
    ]