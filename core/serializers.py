from rest_framework import exceptions as rest_exceptions, serializers
from service import CoreService

from . import exceptions, models


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "public_key", "email"]


class LoginSerializer(serializers.Serializer):
    signatures = serializers.ListSerializer(child=serializers.CharField)
    public_key = serializers.CharField()

    def validate(self, attrs):
        check = CoreService.validate_login_request(
            attrs["signatures"], attrs["public_key"]
        )
        if not check:
            raise exceptions.LoginValidationFailed

        # prevent login if account is not active
        if models.User.objects.filter(
            public_key=attrs["public_key"], is_active=False
        ).exists():
            raise rest_exceptions.AuthenticationFailed

        return attrs

    def save(self):
        public_key = self.validated_data["public_key"]
        user, is_new = CoreService.login_or_register_user(public_key)
        data = UserSerializer(user).data
        data["is_new"] = is_new
        token_info = CoreService.generate_auth_token_data(user)
        return {**data, **token_info}
