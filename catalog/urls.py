from django.conf.urls.static import static
from django.urls import path, include


from catalog.apps import CatalogConfig
from catalog.views import ProductListView, \
    ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ContactsView
from config import settings

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home_page'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('contacts/', ContactsView.as_view(), name='feedback_form'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('products/create', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)