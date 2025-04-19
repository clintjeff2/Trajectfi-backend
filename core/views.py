# Create your views here.
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from . import models, serializers


class AcceptedNFTListAPIView(ListAPIView):
    queryset = models.AcceptedNFT.objects.all().order_by("name")
    serializer_class = serializers.AcceptedNFTSerializer


class AcceptedTokenListAPIView(ListAPIView):
    queryset = models.AcceptedToken.objects.all().order_by("name")
    serializer_class = serializers.AcceptedTokenSerializer


class SignInAPIView(GenericAPIView):
    serializer_class = serializers.SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data)
