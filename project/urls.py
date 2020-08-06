from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import handler404, handler403
from project.apps.security import views as secview

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # App Paths
    url('', include('project.apps.security.urls')),
    url(r'^', include('project.apps.security.urls')),
    url(r'^v1', include('project.apps.security.urls')),
    url(r'^v1/', include('project.apps.security.urls')),
    url(r'^v1/auth/', include('project.apps.security.urls')),
    url(r'^v1/examples/', include('project.apps.examples.urls')),
]

handler404 = secview.error_404_def
# handler403 = secview.error_403_def

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

admin.site.site_header = settings.APPNAME
