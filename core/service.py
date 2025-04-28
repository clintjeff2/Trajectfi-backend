import json

from rest_framework_simplejwt.tokens import RefreshToken
from starknet_py.utils.typed_data import TypedData

from core import models

from .utils import SignatureUtils


class CoreService:
    @classmethod
    def generate_auth_token_data(user: models.User) -> dict:
        """
        Create the login token for validating protected requests.
        Args:
            user(models.User): the user model
        """
        token_data_obj = RefreshToken.for_user(user)
        expiry = token_data_obj.access_token["exp"]
        token_data = {
            "access": str(token_data_obj.access_token),
            "refresh": str(token_data_obj),
            "expiry": expiry,
        }
        return token_data

    @classmethod
    def validate_loan_offer_request(
        cls, data: dict, signatures: list[str], user: models.User
    ):
        """
        Validate the signed data that verifies the offer create functionality.
        The data is signed by the user's wallet and it's components
        are sent for verification
        Args:
            data(dict): the data required to complete the signature request
            signatures(list[str]): the signatures of the message
            user: The user that is signing the message,

        """
        request_format = SignatureUtils.offer_typed_data_format()
        typed_data = SignatureUtils.generate_signature_typed_data(data, request_format)
        return SignatureUtils.verify_signatures(typed_data, signatures, user.public_key)

    @classmethod
    def validate_login_request(
        cls, signatures: list[str], public_key: list[str]
    ) -> bool:
        """
        Validate the Signed data that verifies the login of the user.
        The data is signed by the user's wallet and it's components
        are sent for verification
        Args:
            signatures(list[str]): the signatures of the message
            public_key: The public key of the signer.

        Returns:
            bool: a bool representing whether the signature is valid or not.
        """
        typed_data_dict = SignatureUtils.login_typed_data_format()
        typed_data = TypedData(**typed_data_dict)
        return SignatureUtils.verify_signatures(typed_data, signatures, public_key)

    @classmethod
    def login_or_register_user(cls, public_key: str) -> tuple[models.User, bool]:
        """
        Create or get the existing user model
        Args:
            public_key: The public key of the user

        Returns:
            tuple[User, bool]: The User model and  a bool indicating
                whether is a new model or not
        """
        user, created = models.User.objects.get_or_create(public_key=public_key)
        return user, created

    @classmethod
    def create_offer(
        cls,
        user: models.User,
        listing: models.Listing,
        principal: int,
        repayment_amount: int,
        duration: int,
        signature: list[str],
        signature_expiry: int,
        signature_chain_id: int,
        signature_unique_id: int,
    ) -> models.Offer:
        """
        Create an Offer with all the required data.
        convert the signature to string json and save it as string in the db
        Returns:
            models.Offer: the newly created offer instance
        """
        offer = models.Offer()
        offer.user = user
        offer.listing = listing
        offer.borrow_amount = principal
        offer.repayment_amount = repayment_amount
        offer.duration = duration
        # convert signature to json string and save as string to db
        offer.signature = json.dumps(signature)
        offer.signature_expiry = signature_expiry
        offer.signature_chain_id = signature_chain_id
        offer.signature_unique_id = signature_unique_id
        offer.save()
        return offer

    @classmethod
    def cancel_offer(cls, offer_id: str):
        """
        Delete the offer
        Args:
            offer_id(str): The id of the offer
        """
        models.Offer.objects.get(id=offer_id).delete()
