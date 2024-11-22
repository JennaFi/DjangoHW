from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView

from catalog.forms import ProductForm
from catalog.models import Product, Contact, Category

class AddProduct(CreateView):
    model = Product
    form = ProductForm

    context = {'products': Product.objects.all()}
    template_name = 'catalog/add_product.html'
    success_url = '/add_product/'



def home_page(request):
    products = Product.objects.all().order_by("-created_at")[:5]
    # for product in products:
    #     print(product.name)

    return render(request, 'catalog/home_page.html', {'products': products})


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        context = {'name': name, 'phone': phone}

        return render(request, 'catalog/feedback_form.html', context)

    queryset = Contact.objects.all()
    context = {"contacts": queryset}
    return render(request, 'catalog/contacts.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product},)


def product_list(request):
    products = Product.objects.all()

    return render(request, 'catalog/product_list.html', {'products': products})




