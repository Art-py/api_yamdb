import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    )

User = get_user_model()
DATA_DIR = os.path.join(settings.STATICFILES_DIRS[0], 'data')


class Command(BaseCommand):
    help = 'Наполняет базу данными из CSV-таблиц'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.add_users()
        self.add_categories()
        self.add_genres()
        self.add_titles()
        self.add_title_genre_relations
        self.add_reviews()
        self.add_comments()
        self.stdout.write(self.style.SUCCESS('Данные добавлены'))

    def get_csv_reader(self, name):
        """Загружает таблицу по имени (расширение передавать не требуется)"""
        path = os.path.join(DATA_DIR, name)+'.csv'
        f = open(path, 'r', encoding='utf-8')
        return csv.DictReader(f)

    def add_users(self):
        reader = self.get_csv_reader('users')
        for row in reader:
            User.objects.create_user(**row)

    def add_categories(self): 
        reader = self.get_csv_reader('category')
        for row in reader:
            Category.objects.create(**row)

    def add_genres(self):
        reader = self.get_csv_reader('genre')
        for row in reader:
            Genre.objects.create(**row)

    def add_titles(self):
        reader = self.get_csv_reader('titles')
        for row in reader:
            row['category_id'] = row.pop('category')
            Title.objects.create(**row)

    def add_title_genre_relations(self):
        reader = self.get_csv_reader('genre_title')
        for row in reader:
            Title.genre.through.objects.create(**row)

    def add_reviews(self):
        reader = self.get_csv_reader('review')
        for row in reader:
            row['author_id'] = row.pop('author')
            Review.objects.create(**row)

    def add_comments(self):
        reader = self.get_csv_reader('comments')
        for row in reader:
            row['author_id'] = row.pop('author')
            Comment.objects.create(**row)
