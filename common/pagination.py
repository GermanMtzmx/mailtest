from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    """Page number pagination"""

    page_size = 10

    max_page_size = 100

    page_query_param = 'page'
    page_size_query_param = 'size'
