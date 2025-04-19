from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers

from . import exceptions, models
from .service import CoreService


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
    """
    Convert the user model class to dict-like data for json serialization.
    """

    class Meta:
        model = models.User
        fields = ["id", "public_key", "email"]


class SignInSerializer(serializers.Serializer):
    """
    Serializer class for the sign in request call.
    It validates the signstures to ensure it is the right user that is
    making the signin request.
    This is for signing in with the wallet (account).

    Data:
        signatures: A list of strings representing the signatures of
            the signed login message
        public_key: The public key of the signer
    """

    signatures = serializers.ListField(child=serializers.CharField())
    public_key = serializers.CharField()

    def validate(self, attrs: dict) -> dict:
        """
        Validate the request data
        """
        # The signature list length must be greater than or equals to 5
        # according to the starknet signature format.
        if len(attrs["signatures"]) < 5:
            raise exceptions.InvalidSignature

        # validate the signature
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

    def save(self) -> dict:
        """
        Create or get the user and generate an auth token data
        for requests authentications

        Returns:
            dict: Data of the user
        """
        public_key = self.validated_data["public_key"]
        user, is_new = CoreService.login_or_register_user(public_key)
        data = UserSerializer(user).data
        data["is_new"] = is_new
        token_info = CoreService.generate_auth_token_data(user)
        return {**data, **token_info}
