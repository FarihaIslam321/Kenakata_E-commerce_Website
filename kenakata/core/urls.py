from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('product_details/', views.product_details, name='product_details'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)