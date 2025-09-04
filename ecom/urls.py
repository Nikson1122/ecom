from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
      path('signup/', views.signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('product/', views.product, name='product'),
    path('orders/', views.orders, name='orders'),
    path('productlist/', views.product_list, name='productlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)