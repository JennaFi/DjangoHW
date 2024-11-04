from itertools import product

from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Add test products to the database'

    def handle(self, *args, **kwargs):

        Category.objects.all().delete()
        Product.objects.all().delete()

        category, _ = Category.objects.get_or_create(name='Верхняя одежда', description='Верхняя одежд')

        products = [
            {'name': 'Куртка_1', 'description': 'куртка', 'price': 49.99, 'category': category},
            {'name': 'Куртка_2', 'description': 'куртка', 'price': 59.99, 'category': category},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added product: {product.name} {product.price}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name} {product.price}'))