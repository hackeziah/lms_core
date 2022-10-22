from django.contrib import admin
from django.urls import path
from schema import schema

from django.views import View
from ariadne_django.views import GraphQLView
# admin/
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', admin.site.urls),
    path('graphql/', GraphQLView.as_view(schema=schema), name='graphql')
]
