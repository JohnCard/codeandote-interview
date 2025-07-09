from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    # Page size
    page_size = 100
    # Allow us to specify how many we want on every page
    page_size_query_param = 'count'
    # How many it can take
    max_page_size = 200
    # Page query parameter name
    page_query_param = 'page'