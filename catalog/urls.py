from django.conf.urls.static import static
from django.urls import path, include


from catalog.apps import CatalogConfig
from catalog.views import home_page, contacts, product_detail, product_list, AddProduct
from config import settings

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_page, name='home_page'),
    path('contacts/', contacts, name='contacts'),
    path('contacts/', contacts, name='feedback_form'),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>', product_detail, name='product_detail'),
    path("add_product/", AddProduct.as_view(), name="add_product"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)