from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('users.urls')),
    path('', include('faq.urls')),
    path('', include('career.urls')),
    path('', include('policies.urls')),
    path('', include('blog.urls')),
    path('', include('aboutus.urls')),
    path('', include('catelogue.urls')),


    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)