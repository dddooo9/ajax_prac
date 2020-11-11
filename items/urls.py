from django.urls import path
from . import views

app_name="items"
urlpatterns = [
    path('', views.main, name="main"),
    path('new/', views.new, name="new"),
    path('create/', views.create, name="create"),
    path('show/<int:post_id>/', views.show, name="show"),
    path('delete/<int:post_id>/', views.delete, name="delete"),
    path('like_toggle/<int:post_id>/', views.like_toggle, name="like_toggle"),
    path('dislike_toggle/<int:post_id>/', views.dislike_toggle, name="dislike_toggle"),
    path('create_comment/<int:post_id>/', views.create_comment, name="create_comment"),
]