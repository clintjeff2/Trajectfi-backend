from rest_framework.exceptions import APIException


class LoginValidationFailed(APIException):
    status_code = 400
    default_code = "login_validation_failed"
    default_detail = "Cannot Login or SignUp"
