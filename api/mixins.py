class DttViewsetMixin(object):
    """
    All viewset customization goes here.
    """
    api_model = None
    list_serializer = None

    def get_queryset(self):
        return self.api_model.objects.all()

    def create(self, request, *args, **kwargs):
        return super(DttViewsetMixin, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        separate list serializer from create
        """
        self.serializer_class = self.list_serializer
        return super(DttViewsetMixin, self).list(request, *args, **kwargs)