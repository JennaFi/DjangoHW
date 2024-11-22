from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from catalog.forms import ProductForm
from catalog.models import Product, Contact, Category

# class AddProduct(CreateView):
#     model = Product
#     form = ProductForm
#
#     context = {'products': Product.objects.all()}
#     template_name = 'catalog/add_product.html'
#     success_url = '/add_product/'

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])
#
#
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["contacts"] = Contact.objects.all()
        return context

    @staticmethod
    def post(request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(
            f"{name}, Ваше сообщение получено<br>Телефон: {phone}<br>Сообщение: {message}"
        )
# def home_page(request):
#     products = Product.objects.all().order_by("-created_at")[:5]
#     # for product in products:
#     #     print(product.name)
#
#     return render(request, 'catalog/home_page.html', {'products': products})
#
#
# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         context = {'name': name, 'phone': phone}
#
#         return render(request, 'catalog/feedback_form.html', context)
#
#     queryset = Contact.objects.all()
#     context = {"contacts": queryset}
#     return render(request, 'catalog/contacts.html', context)
#

# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'catalog/product_detail.html', {'product': product},)
#
#
# def product_list(request):
#     products = Product.objects.all()
#
#     return render(request, 'catalog/product_list.html', {'products': products})
#



