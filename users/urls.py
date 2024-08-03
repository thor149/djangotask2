from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.homePage, name='homepage'),
    path('register/', views.registerUser, name='register'),
    path('dashboard/', views.userAccount, name='dashboard'),
    path('update-profile/<str:pk>/', views.updateProject, name='update'),
]

# urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)