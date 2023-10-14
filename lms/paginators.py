from rest_framework.pagination import PageNumberPagination


class LMSPaginator(PageNumberPagination):
    page_size = 10
