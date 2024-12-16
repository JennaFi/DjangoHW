from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Article


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1

        if self.object.view_count == 100:
            subject = f"{self.object.title} - Количество просмотров достигло 100!"
            message = f"Статья {self.object.title} была просмотрена больше 100 раз!"
            from_email = "gazeta@mail.ru"
            recipient_list = ["eva.oww@gmail.com", "admin@example.com", ]
            send_mail(subject, message, from_email, recipient_list)
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_content_manager = self.request.user.groups.filter(
            name="Контент-менеджер"
        ).exists()

        context['is_content_manager'] = is_content_manager
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    queryset = Article.objects.filter(is_published=True)
    paginate_by = 5
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_content_manager = self.request.user.groups.filter(
            name="Контент-менеджер"
        ).exists()

        context['is_content_manager'] = is_content_manager
        return context

class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/article_create.html'
    success_url = reverse_lazy("blog:article_list")

    def form_valid(self, form):
        form.instance.created_at = datetime.now()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/article_update.html'
    success_url = reverse_lazy("blog:article_list")

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        form.instance.updated_at = datetime.now()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_object_changed(self, request, *args, **kwargs):
        article = super().get_object(*args, **kwargs)
        if article.author == self.request.user:
            return article
        else:
            raise PermissionDenied("You don't have permission to edit this article")

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("blog:article_list")

    def get_object_changed(self, request, *args, **kwargs):
        article = super().get_object(*args, **kwargs)
        if article.author == self.request.user:
            return article
        else:
            raise PermissionDenied("You don't have permission to delete this article")


class ArticlePublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        if request.user.has_perm('blog.can_unpublish_article') and article:

            article.is_published = True
            article.save()
            return redirect("blog:article_list")

        if article.author == self.request.user:

            article.is_published = True
            article.save()
            return redirect("blog:article_list")

        return HttpResponseForbidden('You do not have permission to publish this article')

class ArticleUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        if request.user.has_perm('blog.can_unpublish_article'):

            article.is_published = False
            article.save()
            return redirect("blog:article_list")

        if article.author == self.request.user:

            article.is_published = False
            article.save()
            return redirect("blog:article_list")

        return HttpResponseForbidden('You do not have permission to unpublish this article')
