from django.urls import path

from . import views

urlpatterns = [
    path(
        "accepted-nfts/",
        views.AcceptedNFTListAPIView.as_view(),
        name="accepted-nfts-list-view",
    ),
    path(
        "accepted-tokens/",
        views.AcceptedTokenListAPIView.as_view(),
        name="accepted-tokens-list-view",
    ),
    path(
        "sigin/",
        views.SignInAPIView.as_view(),
        name="signin",
    ),
]
