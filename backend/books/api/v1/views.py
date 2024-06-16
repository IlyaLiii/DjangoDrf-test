import json
import logging

from books.models import Book
from books.serializers import BookSerializer, UserSerializer, GroupSerializer
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from django_filters import FilterSet, CharFilter, ChoiceFilter, BaseCSVFilter, NumberFilter

from rest_framework import permissions, viewsets, renderers
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class CharArrayFilter(BaseCSVFilter, CharFilter):
    pass


class BookFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='contains')
    authors = CharArrayFilter(field_name='authors', lookup_expr='contains')
    status = ChoiceFilter(choices=Book.STATUS_CHOICE)
    pub_date = NumberFilter(field_name='pub_date', lookup_expr='year__gt')


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all().order_by('-pub_date')
    serializer_class = BookSerializer
    filterset_class = BookFilter

    @cache_page(60 * 15)
    def retrieve(self, request, pk=None):
        pre_query = Book.objects.filter(id=pk).order_by('-pub_date')
        category = pre_query[0].categories[0]

        query = Q(id=pk)
        try:
            query.add(Q(categories__contains=[category]), Q.OR)
        except Exception as e:
            logging.info(e)
            serializer = self.get_serializer(pre_query, many=True)
            return HttpResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = Book.objects.filter(query)
            serializer = self.get_serializer(queryset, many=True)
            serializer_return_list = serializer.data
            converted_data = []

            for ordered_dict in serializer_return_list:
                converted_data.append(dict(ordered_dict))

            for item in converted_data:
                if item.get('id') == pk:
                    main_item = item
                    converted_data[0].clear()
                    converted_data[0].update({'main_instance': main_item})

            converted_data = converted_data[:6]

            new_data = {}
            new_data.update({'main_instance': converted_data[0].get('main_instance')})
            list_books = []
            for i in converted_data:
                if not i.get('id') == pk:
                    list_books.append(i)
            new_data.update({'list_books': list_books})
            json.dumps(new_data, indent=2)
            return Response(new_data, status=status.HTTP_200_OK)

    @cache_page(60 * 15)
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def categories(self, request, *args, **kwargs):
        print('zxcqwezxc')
        book = self.get_object()
        all_categories = ', '.join(book.categories)
        return Response(all_categories)

    @cache_page(60 * 15)
    @action(detail=True, url_path=r'categories/(?P<subcategories>\w+)', url_name='categories-subcategories',
            renderer_classes=[renderers.StaticHTMLRenderer])
    def sub_categories(self, request, *args, **kwargs):
        book = self.get_object()
        all_subcategories = ', '.join(book.subcategories)
        return Response(all_subcategories)


class MultipleFieldLookupMixin:

    @cache_page(60 * 15)
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter[field] = self.kwargs[field]
        obj = get_list_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


@cache_page(60 * 15)
@api_view(['GET', 'POST'])
def get_books_by_category(request, pk: str):
    paginator = PageNumberPagination()

    try:
        books = Book.objects.filter(categories__contains=[pk])
        books = books.order_by('pub_date')
    except Exception as e:
        return HttpResponse(status=404)

    if request.method == 'GET':
        result_page = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, many=True, context={'request': request})
        serializer = serializer.data
        return Response(serializer, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

