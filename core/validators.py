from rest_framework import serializers


def is_positive_number(value: str):
    """
    Validate that the value is a positive integer
    """
    try:
        val = int(value)
        if val <= 0:
            raise ValueError
    except Exception:
        raise serializers.ValidationError("This field must be a positive integer")
