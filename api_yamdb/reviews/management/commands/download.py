import os

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Пробуем новый функционал'

    def handle(self, *args, **options):
        files = os.listdir(settings)
        for file in files:
            print(os.path)
        print('Вроде ок')
