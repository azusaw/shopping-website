import csv
import webcolors
from pathlib import Path

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from shopping.models import Item, Gender, MasterCategory, SubCategory, ArticleType, BaseColour, Image


def get_hex_code(str):
    colour = str.lower().split(' ')[-1]
    if colour == 'copper' or colour == 'rust' or colour == 'bronze':
        colour = 'brown'
    elif colour == 'nude' or colour == 'mustard' or colour == 'skin':
        colour = 'wheat'
    elif colour == 'cream':
        colour = 'white'
    elif colour == 'rose' or colour == 'burgundy':
        colour = 'red'
    elif colour == 'mauve':
        colour = 'mediumpurple'
    elif colour == 'peach':
        colour = 'lightpink'
    elif colour == 'charcoal' or colour == 'steel' or colour == 'taupe' or colour == 'melange':
        colour = 'gray'
    try:
        hex_code = webcolors.name_to_hex(colour)
    except Exception:
        hex_code = None
    return hex_code


class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):
        # Delete data from tables to avoid duplicate values
        print("START: DELETE ALL RECORDS FROM DATABASE")
        Item.objects.all().delete()
        Gender.objects.all().delete()
        MasterCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        ArticleType.objects.all().delete()
        BaseColour.objects.all().delete()
        print("--> Delete all record successfully.")

        # Insert data from styles.csv
        print("START: READ DATA FROM CSV FROM styles.csv")
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        with open(str(base_dir) + '/data/styles.csv', newline='', encoding='latin-1') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)

            items = []
            gender = set()
            master_category = set()
            sub_category = set()
            article_type = set()
            base_colour = set()

            # Insert data to the relevant tables
            for row in reader:
                gender.add(Gender(id=row[1]))
                master_category.add(MasterCategory(id=row[2]))
                sub_category.add(SubCategory(id=row[3]))
                article_type.add(ArticleType(id=row[4]))
                base_colour.add(BaseColour(id=row[5], hex_code=get_hex_code(row[5])))

                # Reduce the number of record into 3000 - 7000 filter by year
                if row[7] > '2015':
                    item = Item(
                        id=row[0],
                        gender_id=row[1],
                        master_category_id=row[2],
                        sub_category_id=row[3],
                        article_type_id=row[4],
                        base_colour_id=row[5],
                        season=row[6],
                        year=row[7],
                        usage=row[8],
                        display_name=row[9]
                    )
                    items.append(item)
            print("--> Read all from styles.csv record successfully.")

            print("START: INSERT DATA INTO DATABASE")
            Gender.objects.bulk_create(gender)
            MasterCategory.objects.bulk_create(master_category)
            SubCategory.objects.bulk_create(sub_category)
            ArticleType.objects.bulk_create(article_type)
            BaseColour.objects.bulk_create(base_colour)
            Item.objects.bulk_create(items)
            print("--> Data parsed successfully.")

            # Insert data from images.csv
            print("START: READ DATA FROM CSV FROM images.csv")
            with open(str(base_dir) + '/data/images.csv', newline='', encoding='latin-1') as f:
                reader = csv.reader(f, delimiter=",")
                next(reader)

                images = []

                for row in reader:
                    try:
                        item = Item.objects.get(pk=row[0].removesuffix('.jpg'))
                    except Item.DoesNotExist:
                        # Skip if a item does not exist in shopping_item table
                        continue
                    image = Image(
                        item=item,
                        link=row[1],
                        )
                    images.append(image)
                print("--> Read all from images.csv record successfully.")

                print("START: INSERT DATA INTO DATABASE")
                Image.objects.bulk_create(images)
                print("--> Data parsed successfully.")

        print("--> Complete all data parse successfully.")
