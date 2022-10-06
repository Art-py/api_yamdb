import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, Review, Title)

User = get_user_model()
DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')


class Command(BaseCommand):
    help = 'Наполняет базу данными из CSV-таблиц'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.add_users()
        self.add_categories()
        self.add_genres()
        self.add_titles()
        self.add_title_genre_relations()
        self.add_reviews()
        self.add_comments()
        self.stdout.write(self.style.SUCCESS('Данные добавлены'))

    def get_csv_reader(self, name):
        """Загружает таблицу по имени (расширение передавать не требуется)"""
        path = os.path.join(DATA_DIR, name) + '.csv'
        f = open(path, 'r', encoding='utf-8')
        return csv.DictReader(f)

    def add_users(self):
        reader = self.get_csv_reader('users')
        users = []
        for row in reader:
            users.append(User(**row))
        User.objects.bulk_create(users)

    def add_categories(self):
        reader = self.get_csv_reader('category')
        categories = []
        for row in reader:
            categories.append(Category(**row))
        Category.objects.bulk_create(categories)

    def add_genres(self):
        reader = self.get_csv_reader('genre')
        genres = []
        for row in reader:
            genres.append(Genre(**row))
        Genre.objects.bulk_create(genres)

    def add_titles(self):
        reader = self.get_csv_reader('titles')
        titles = []
        for row in reader:
            row['category_id'] = row.pop('category')
            titles.append(Title(**row))
        Title.objects.bulk_create(titles)

    def add_title_genre_relations(self):
        reader = self.get_csv_reader('genre_title')
        relations = []
        model = Title.genre.through
        for row in reader:
            relations.append(model(**row))
        model.objects.bulk_create(relations)

    def add_reviews(self):
        reader = self.get_csv_reader('review')
        reviews = []
        for row in reader:
            row['author_id'] = row.pop('author')
            reviews.append(Review(**row))
        Review.objects.bulk_create(reviews)

    def add_comments(self):
        reader = self.get_csv_reader('comments')
        comments = []
        for row in reader:
            row['author_id'] = row.pop('author')
            comments.append(Comment(**row))
        Comment.objects.bulk_create(comments)
