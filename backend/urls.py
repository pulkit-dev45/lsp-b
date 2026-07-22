from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from courses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("lsp_auth.urls")),
    path('courses/', include("courses.urls")),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.landing_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
