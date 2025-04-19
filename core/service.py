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
    def validate_login_request(
        cls, signatures: list[str], public_key: list[str]
    ) -> bool:
        """
        Validate the Signed data that verifies the login of the user.
        The data is signed by the user's wallet and it's components
        are sent for verifiction
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
