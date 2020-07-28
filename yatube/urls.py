from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings



handler404 = "posts.views.page_not_found" # noqa
handler500 = "posts.views.server_error" # noqa

urlpatterns = [
    path("", include("posts.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about/", include("django.contrib.flatpages.urls")),
    path("admin/", admin.site.urls),


]

urlpatterns += [
    path("about-us/", views.flatpage, {"url": "/about-us/"}, name="about"),
    path("terms/", views.flatpage, {"url": "/terms/"}, name="terms"),
    path("about-author/", views.flatpage, {"url": "/about-author/"}, name="author"),
    path("about-spec/", views.flatpage, {"url": "/about-spec/"}, name="spec"),
]
# add debug_toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path("__debug__/", include(debug_toolbar.urls)),
                  ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)