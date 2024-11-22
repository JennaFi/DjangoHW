from django import forms
from catalog.models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'image', 'price', 'created_at']
        labels = {'name': 'Name of new product',
                  'category': 'Category of product',
                  'description': 'Description of the product',
                  'image': 'Image',
                  'price': 'Price of the product',
                  'created_at': 'created at'
                  }