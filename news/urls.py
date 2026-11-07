from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='detail'),
    path('category/<slug:slug>/', views.category_list, name='category'),
]
