from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    preview = models.ImageField(upload_to='blog/previews/', null=True, blank=True, verbose_name='Preview')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0, verbose_name='View Count')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']
