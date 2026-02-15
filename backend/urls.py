
from django.contrib import admin
from django.urls import path , include 
from django.conf.urls.static import static
from django.conf import settings 
from rest_framework_simplejwt.views import TokenRefreshView 
import Main
urlpatterns = [
    path('admin/', admin.site.urls),
    path('refresh/',TokenRefreshView.as_view()),
    path('user/',include('Main.urls'))
]
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)