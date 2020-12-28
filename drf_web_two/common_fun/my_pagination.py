from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.utils.translation import gettext_lazy as _
class TwoPagePagination(PageNumberPagination):
    page_size = 2
    # page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_description = _('页数')
    # def get_paginated_response(self, data):
    #     return Response({
    #         'links': {
    #             'next': self.get_next_link(),
    #             'previous': self.get_previous_link()
    #         },
    #         'count': self.page.paginator.count,
    #         'results': data
    #     })

    # def get_paginated_response(self, data):
    #     return Response(OrderedDict([
    #         ('counts', self.page.paginator.count),
    #         ('next', self.get_next_link()),
    #         ('previous', self.get_previous_link()),
    #         ('results', data)
    #     ]))