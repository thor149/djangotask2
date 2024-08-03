from django.urls import path
from . import views

urlpatterns = [
    path("", views.blogs, name="blogs"),
    path("create-blog", views.create_blog, name="createblog"),
    path('all-blog', views.all_blogs, name='allblog'),
    path('update-blog/<str:pk>/', views.updateBlog, name='updateblog'),
    path('delete-blog/<str:pk>/', views.deleteBlog, name='deleteblog'),
]