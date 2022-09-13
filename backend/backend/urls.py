from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static
#from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Pribos",
        default_version="v1",
        description="AI Workflow for freelancing translators",
        contact=openapi.Contact(email="pribos.official@gmail.com"),
        license=openapi.License(name="MIT License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # path('', views.getFront, name="front"),
    path('', include('common.urls')),
    path('api/accounts/', include('dj_rest_auth.urls')),
    path('api/accounts/', include('allauth.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/task/', include('task.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
        re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]


admin.site.site_header = "Pribos - AI workflow for freelancers"
admin.site.site_title = "Pribos - AI workflow for freelancers"
admin.site.index_title = "Welcome to Pribos"
