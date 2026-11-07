from django.db import models
from django.urls import reverse


class Author(models.Model):
    """Person who writes news articles."""

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Topic used to group articles."""

    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news:category', kwargs={'slug': self.slug})


class Article(models.Model):
    """News article with featured image, author and categories."""

    title = models.CharField(max_length=200)
    summary = models.TextField(help_text='Short text shown in the article cards.')
    body = models.TextField()
    featured_image = models.ImageField(upload_to='articles/', blank=True)
    published_at = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='articles')
    categories = models.ManyToManyField(Category, related_name='articles')

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'pk': self.pk})
