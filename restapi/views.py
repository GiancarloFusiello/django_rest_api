from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from restapi.models import Prezi
from restapi.serializers import PreziSerializer


class BaseAPIView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    An API view that is restricted to getting a single instance, listing all
    instances and updating an instance if authenticated.
    """
    pass


class PreziAPIView(BaseAPIView):

    serializer_class = PreziSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Prezi.objects.all()
        order = self.request.query_params.get('order', None)
        if order and order.lower() == 'asc':
            return queryset.order_by('created_at')
        else:
            # order by newest first by default
            return queryset.order_by('-created_at')
