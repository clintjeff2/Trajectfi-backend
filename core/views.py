# Create your views here.
from rest_framework.generics import ListAPIView

from . import models, serializers


class AcceptedNFTListAPIView(ListAPIView):
    queryset = models.AcceptedNFT.objects.all().order_by("name")
    serializer_class = serializers.AcceptedNFTSerializer
