from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Category')
    description = models.TextField(default=None, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Product_name')
    description = models.TextField(default=None, blank=True)
    image = models.ImageField(upload_to='products_photo/%Y/%m/%d', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name', 'category', 'price']

    def __str__(self):
        return f'{self.name}, {self.category}'


class Contact(models.Model):

    first_name = models.CharField(max_length=150, verbose_name="Name")
    last_name = models.CharField(max_length=150, verbose_name="Last name")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = [
            "email",
        ]