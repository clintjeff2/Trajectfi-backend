from rest_framework import serializers

from . import models


class AcceptedNFTSerializer(serializers.ModelSerializer):
    """
    Serializer class for AcceptedNFT Model.
    Additionally return a number of listings that uses
    the nfts's contract address

    Fields:
        - name
        - contract_address
        - listing_count
    """

    listings_count = serializers.SerializerMethodField()

    class Meta:
        model = models.AcceptedNFT
        fields = ["name", "contract_address", "listings_count"]

    def get_listings_count(self, obj: models.AcceptedNFT) -> int:
        return models.Listing.objects.filter(
            nft_contract_address=obj.contract_address
        ).count()


class AcceptedTokenSerializer(serializers.ModelSerializer):
    """
    Serializer class for AcceptedToken Model.
    Additionally return a number of listings that uses
    the token's contract address

    Fields:
        - name
        - contract_address
        - listing_count
    """

    listings_count = serializers.SerializerMethodField()

    class Meta:
        model = models.AcceptedToken
        fields = ["name", "contract_address", "listings_count"]

    def get_listings_count(self, obj: models.AcceptedNFT) -> int:
        return models.Listing.objects.filter(
            token_contract_address=obj.contract_address
        ).count()
