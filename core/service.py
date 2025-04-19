from rest_framework_simplejwt.tokens import RefreshToken
from starknet_py.utils.typed_data import TypedData
from utils import SignatureUtils

from core import models


class CoreService:
    @classmethod
    def generate_auth_token_data(user: models.User):
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
        typed_data_dict = SignatureUtils.login_typed_data_format()
        typed_data = TypedData(**typed_data_dict)
        return SignatureUtils.verify_signatures(typed_data, signatures, public_key)

    @classmethod
    def login_or_register_user(cls, public_key: str) -> tuple[models.User, bool]:
        user, created = models.User.objects.get_or_create(public_key=public_key)
        return user, created
