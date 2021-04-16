from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('main', views.main),
    path('logout', views.logout),
    path('return', views.return_m),
    path('add_book', views.add_book),
    path('books/<int:id>', views.view_book),
    path('books/<int:id>/destroy', views.destroy),
    path('books/<int:id>/update', views.update),
    path('books/<int:id>/like', views.like)
]