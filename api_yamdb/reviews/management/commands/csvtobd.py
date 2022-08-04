import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Title_genre, Genre,
                            Review, Title, User)


class Command(BaseCommand):
    help = 'Заполняет БД модели из csv'

    def add_arguments(self, parser):
        parser.add_argument('model', nargs='+', type=str)
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        model = options['model'][0]
        file = options['file'][0]
        models = {
            'Category': Category, 'Comment': Comment,
            'Title_genre': Title_genre, 'Genre': Genre, 'Review': Review,
            'Title': Title, 'User': User}
        with open(
            f'{os.getcwd()}/static/data/{file}',
            newline='', encoding='utf-8'
        ) as op_file:
            reader = csv.reader(op_file)
            for row in reader:
                if row[0] == 'id':
                    fields = row[:]
                else:
                    # Модуль для автозагрузки, для кастомной
                    # воспользоваться модулем ниже
                    values = {}
                    for i in range(len(row)):
                        values[fields[i]] = row[i]
                    models[model].objects.get_or_create(**values)

                    # Для загрузки связанных полей написать куда загружать

                    # models[model].objects.get_or_create(
                    #     id=row[0],
                    #     title=Title.objects.get(id=row[1]),
                    #     genre=Genre.objects.get(id=row[2]),
                    # )
                    print(models[model].objects.get(id=row[0]))
