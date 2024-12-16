from datetime import datetime
from itertools import product

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Contact, Category


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'catalog/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_moderator = self.request.user.has_perm('catalog.delete_product')

        context['is_moderator'] = is_moderator
        return context


class ProductDetailView(DetailView, LoginRequiredMixin):
    model = Product
    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_unpublish_product'):
            return ProductModeratorForm
        else:
            raise PermissionDenied("You don't have permission to unpublish this product")


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def get_object_delete(self, request, *args, **kwargs):
        product = super().get_object()

        if product.owner == self.request.user or request.user.has_perm('catalog.delete_product'):
            return ProductForm
        else:
            raise PermissionDenied("You don't have permission to delete this product")


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
