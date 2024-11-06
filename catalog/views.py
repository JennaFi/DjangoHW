from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product, Contact


def home_page(request):
    products = Product.objects.all().order_by("-created_at")[:5]
    for product in products:
        print(product.name)

    return render(request, 'home_page.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        context = {'name': name, 'phone': phone}

        return render(request, 'feedback_form.html', context)

    queryset = Contact.objects.all()
    context = {"contacts": queryset}
    return render(request, 'contacts.html', context)

