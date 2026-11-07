from django.shortcuts import get_object_or_404, render

from .models import Article, Category


def home(request):
    """Front page: latest articles."""
    articles = Article.objects.select_related('author').prefetch_related('categories')
    return render(request, 'news/home.html', {'articles': articles})


def article_detail(request, pk):
    """Single article page."""
    article = get_object_or_404(
        Article.objects.select_related('author').prefetch_related('categories'), pk=pk
    )
    return render(request, 'news/article_detail.html', {'article': article})


def category_list(request, slug):
    """Articles that belong to one category."""
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.select_related('author').prefetch_related('categories')
    return render(request, 'news/category_list.html', {'category': category, 'articles': articles})
