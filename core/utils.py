# file of all the utility functions, variables and classes
from django.conf import settings
from starknet_py.hash.utils import verify_message_signature
from starknet_py.utils.typed_data import Domain, Parameter, TypedData

DOMAIN_NAME = settings.SIG_DOMAIN_NAME
CHAIN_ID = settings.SIG_CHAIN_ID
VERSION = settings.SIG_VERSION


class SignatureUtils:
    @classmethod
    def login_typed_data_format(cls) -> dict:
        data = {
            "domain": Domain(
                **{
                    "name": DOMAIN_NAME,
                    "chain_id": CHAIN_ID,
                    "version": VERSION,
                }
            ),
            "types": {
                "StarknetDomain": [
                    Parameter(**{"name": "name", "type": "felt"}),
                    Parameter(**{"name": "chainId", "type": "felt"}),
                    Parameter(**{"name": "version", "type": "felt"}),
                ],
                "Message": [
                    Parameter(**{"name": "name", "type": "felt"}),
                    Parameter(**{"name": "age", "type": "felt"}),
                    Parameter(**{"name": "address", "type": "felt"}),
                ],
            },
            "primary_type": "Message",
            "message": {},
        }
        return data.copy()

    @classmethod
    def generate_signature_typed_data(cls, data: dict, type_format: dict) -> TypedData:
        login_signature_request_format = type_format
        login_signature_request_format["message"] = data
        return TypedData(**login_signature_request_format)

    @classmethod
    def verify_signatures(
        cls, typed_data: TypedData, signatures: list[str], public_key: str
    ) -> bool:
        int_signatures = list(map(lambda x: int(x), signatures))
        int_public_key = int(public_key, 16)
        message_hash = typed_data.message_hash(int_public_key)
        return verify_message_signature(message_hash, int_signatures, public_key)
