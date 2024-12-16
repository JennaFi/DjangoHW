from django import forms
from django.core.exceptions import ValidationError
from django.db.models import BooleanField

from catalog.models import Product


# class StyleFirmMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             if isinstance(field, BooleanField):
#                 field.widget.attrs["class"] = "form-check-input"
#             else:
#                 field.widget.attrs["class"] = "form-control"
#                 field.widget.attrs["placeholder"] = field.label


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control mb-3 mt-1", "placeholder": "Введите название товара", "required": True}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control mb-3 mt-1", "placeholder": "Добавьте описание товара"}
        )
        self.fields["image"].widget.attrs.update(
            {"class": "form-control mb-5 mt-1", "placeholder": "Загрузите изображение товара"}
        )
        self.fields["category"].widget.attrs.update({"class": "form-select mb-5 my-1"})
        self.fields["price"].widget.attrs.update(
            {
                "class": "form-control mb-3 mt-1",
                "placeholder": "Укажите цену товара с копейками",
                "required": True,
                "step": "0.01",
            }
        )
        self.fields["is_published"].widget.attrs.update({"class": "form-check-input"})

    banned_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in self.banned_words:
            if word in name.lower():
                raise ValidationError(f"Наименование не может содержать слово '{word}'")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        for word in self.banned_words:
            if word in description.lower():
                raise ValidationError(f"Описание не может содержать слово '{word}'")
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.content_type.endsswith('jpg', 'jpeg', 'png'):
                raise ValidationError("Изображение должно быть в формате PNG, JPEG, JPG")
            if image.size > 8 * 1024 * 1024:  # 8 MB
                raise ValidationError("Размер изображения не должен превышать 8 МБ")
        return image

    class Meta:
        model = Product
        fields = '__all__'
        labels = {'name': 'Name of new product',
                  'category': 'Category of product',
                  'description': 'Description of the product',
                  'image': 'Image',
                  'price': 'Price of the product',
                  'created_at': 'created at'
                  }
        exclude = ('views_counter', 'owner')


class ProductModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('is_published',)
