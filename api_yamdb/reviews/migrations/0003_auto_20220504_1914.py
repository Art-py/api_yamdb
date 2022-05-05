# Generated by Django 2.2.16 on 2022-05-04 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220504_0927'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория произведения', 'verbose_name_plural': 'Категории произведений'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Жанр произведения', 'verbose_name_plural': 'Жанр произведений'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Используйте буквы латиницы, цифры и символы "-" и "_"', unique=True, verbose_name='Уникальный идентифиактор'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(help_text='Используйте буквы латиницы, цифры и символы "-" и "_"', unique=True, verbose_name='Уникальный идентифиактор'),
        ),
    ]