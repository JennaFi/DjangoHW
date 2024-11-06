from django.contrib import admin

from catalog.models import Product, Category, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = ("id", "first_name", "last_name", "email")