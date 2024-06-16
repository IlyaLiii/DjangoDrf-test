from books.api.v1.views import UserViewSet, GroupViewSet, BookViewSet, get_books_by_category
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'books', BookViewSet, basename='book')


books_list = BookViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

books_detail = BookViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Desctiption here",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
swagger_urls = [
    re_path(
        r'^swagger(\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

urlpatterns = [
    path('', include(router.urls)),

    path('books/', books_list, name='books-list'),
    path('books/<int:pk>/', books_detail, name='books-detail'),
    path('category/<str:pk>/', get_books_by_category),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
] + swagger_urls
