import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from contents.models import Content, Detail, Genre

CSV_PATH_PRODUCT = "./backdata.csv"

with open(CSV_PATH_PRODUCT) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)

    for row in data_reader:
        gen1, created = Genre.objects.get_or_create(name = row[6])
        if created:
            print(f"success create {gen1}")
        gen2, created = Genre.objects.get_or_create(name = row[7])
        if created:
            print(f"success create {gen2}")

        content, created = Content.objects.filter(name=row[1]).get_or_create(
        name = row[1],
        category = row[2],
        description = row[3],
        nation = row[4],
        thumb_nail = row[5],
        )
        if created:
            print(f"success create {content}")

        content.genre.add(gen1)
        print(f"success create relation {content} with {gen1}")

        content.genre.add(gen2)
        print(f"success create relation {content} with {gen2}")

        detail, created = Detail.objects.filter(episode=row[9]).get_or_create(
        episode = row[9],
        description = row[10],
        running_time = row[11],
        thumb_nail = row[12],
        file = "video/"+row[9]+".mp4",
        content = content,
        )
        if created:
            print(f"success create {detail}")
