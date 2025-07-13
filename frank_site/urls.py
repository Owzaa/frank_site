from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Site-Administration"
admin.site.site_title = "Themba-Tswai"
admin.site.index_title = "Manage your Applications Admin-Side"

urlpatterns = [
    path('admin/', admin.site.urls), # type: ignore
    path('accounts/', include('django.contrib.auth.urls')),  # Django authentication URLs # type: ignore
    path('', include('HOME.urls')), # type: ignore
    path('', include('APPS.STORE.urls')), # type: ignore
    path('', include('APPS.PORTFOLIO.urls')), # type: ignore
    # Removed duplicate STORE.urls include
    path('blog/', include('APPS.BLOG.urls')), # type: ignore
    path('',include('APPS.PAYMENTS.urls')), # type: ignore
    path('paypal/', include('paypal.standard.ipn.urls')), # type: ignore

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
