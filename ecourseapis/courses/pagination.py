from rest_framework import pagination


class CoursePaginator(pagination.PageNumberPagination):
    page_size = 1


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2
