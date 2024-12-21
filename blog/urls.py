from django.conf.urls.static import static
from django.urls import path

from blog import views
from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, \
    ArticleUnpublishView, ArticlePublishView
from config import settings

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', ArticleListView.as_view(), name='article_list'),
    path('blog/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('blog/create/', ArticleCreateView.as_view(), name='article_create'),
    path('blog/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('blog/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('<int:pk>/unpublish', ArticleUnpublishView.as_view(), name='article_unpublish'),
    path('<int:pk>/publish', ArticlePublishView.as_view(), name='article_publish'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
