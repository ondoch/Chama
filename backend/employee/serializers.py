import re

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from access.catalog import ALL_PERMISSION_KEYS, ROLE_BY_KEY
from access.services import apply_access, grant_problems, read_access
from authentication.passwords import generate_temporary_password

from .models import Employee

User = get_user_model()

NATIONAL_ID_RE = re.compile(r"^\d{7,8}$")
PHONE_RE = re.compile(r"^(?:\+?254|0)([17]\d{8})$")

def normalize_phone(value):
    cleaned = re.sub(r"[\s-]", "", value)
    match = PHONE_RE.match(cleaned)
    if not match:
        raise serializers.ValidationError("Enter a valid Kenyan phone number, e.g. 0712345678 or +254712345678.")
    return "+254" + match.group(1)

class StatusField(serializers.ChoiceField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = data.strip().lower().replace(" ", "_")
        return super().to_internal_value(data)

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name", max_length=150)
    last_name = serializers.CharField(source="user.last_name", max_length=150)
    employement_date = serializers.DateField(input_formats=["iso-8601", "%d/%m/%Y"])
    must_change_password = serializers.BooleanField(source="user.must_change_password", read_only=True)
    roles = serializers.ListField(child=serializers.ChoiceField(choices=list(ROLE_BY_KEY)),
                                  write_only=True, required=False)
    permissions = serializers.ListField(child=serializers.ChoiceField(choices=ALL_PERMISSION_KEYS),
                                        write_only=True, required=False)

    class Meta:
        model = Employee
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'phone_number', 'national_ID', 'employee_ID', 'job_title', 'employment_date', 'status']
        read_only_fields = ['employee_ID']
