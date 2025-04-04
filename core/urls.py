from django.urls import path  # noqa

from . import views

urlpatterns = [
    path(
        "accepted-nfts/",
        views.AcceptedNFTListAPIView.as_view(),
        name="accepted-nfts-list-view",
    )
]
