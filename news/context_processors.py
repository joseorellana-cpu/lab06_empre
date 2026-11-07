from .models import Category


def categories(request):
    """Make the category list available to the sidebar in every template."""
    return {'sidebar_categories': Category.objects.all()}
