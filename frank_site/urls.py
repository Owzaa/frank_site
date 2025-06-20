from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Site-Administration"
admin.site.site_title = "Themba-Tswai"
admin.site.index_title = "Manage your Applications Admin-Side"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Django authentication URLs
    path('', include('HOME.urls')),
    path('', include('APPS.STORE.urls')),
    path('', include('APPS.PORTFOLIO.urls')),
    # Removed duplicate STORE.urls include
    path('blog/', include('APPS.BLOG.urls')),
    path('payments/', include('APPS.PAYMENTS.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
