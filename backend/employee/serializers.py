import re

from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers

from access.catalog import ALL_PERMISSION_KEYS, ROLE_BY_KEY
from access.services import (
    apply_access,
    grant_problems,
    read_access,
    record_audit,
)
from authentication.passwords import generate_temporary_password

from .models import Employee


User = get_user_model()

NATIONAL_ID_RE = re.compile(r"^\d{7,8}$")
PHONE_RE = re.compile(r"^(?:\+?254|0)([17]\d{8})$")


def normalize_phone(value):
    cleaned = re.sub(r"[\s-]", "", value)
    match = PHONE_RE.match(cleaned)

    if not match:
        raise serializers.ValidationError(
            "Enter a valid Kenyan phone number, "
            "e.g. 0712345678 or +254712345678."
        )

    return "+254" + match.group(1)


class EmployeeSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name", max_length=150)
    last_name = serializers.CharField(source="user.last_name", max_length=150)

    employment_date = serializers.DateField(
        input_formats=["iso-8601", "%d/%m/%Y"]
    )

    must_change_password = serializers.BooleanField(
        source="user.must_change_password",
        read_only=True,
    )

    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=list(ROLE_BY_KEY)),
        write_only=True,
        required=False,
    )

    permissions = serializers.ListField(
        child=serializers.ChoiceField(choices=ALL_PERMISSION_KEYS),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "national_ID",
            "employee_ID",
            "job_title",
            "employment_date",
            "status",
            "must_change_password",
            "roles",
            "permissions",
        ]
        read_only_fields = ["id", "employee_ID"]

    # ---------- field validation ----------

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.user_id)
        if qs.exists():
            raise serializers.ValidationError(
                "An employee with this email already exists."
            )
        return value

    def validate_phone_number(self, value):
        return normalize_phone(value)

    def validate_national_ID(self, value):
        if not NATIONAL_ID_RE.match(value):
            raise serializers.ValidationError(
                "Enter a valid National ID (7-8 digits)."
            )
        return value

    def validate(self, attrs):
        """Stop callers granting access they don't hold themselves."""
        request = self.context.get("request")
        if not (request and request.user.is_authenticated):
            return attrs

        new_roles = set(attrs.get("roles", []))
        new_perms = set(attrs.get("permissions", []))

        if self.instance is not None:  # only check what is newly granted
            old_roles, old_perms = read_access(self.instance.user)
            new_roles -= set(old_roles)
            new_perms -= set(old_perms)

        problems = grant_problems(request.user, new_roles, new_perms)
        if problems:
            raise serializers.ValidationError({"permissions": problems})

        return attrs

    # ---------- output ----------

    def to_representation(self, instance):
        data = super().to_representation(instance)

        roles, permissions = read_access(instance.user)
        data["roles"] = roles
        data["permissions"] = permissions

        # Only present on the create response, never stored
        temp_password = getattr(instance, "_temporary_password", None)
        if temp_password:
            data["temporary_password"] = temp_password

        return data

    # ---------- create ----------

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        roles = validated_data.pop("roles", [])
        permissions = validated_data.pop("permissions", [])

        temp_password = generate_temporary_password()

        # No `username`: this User model logs in with email.
        user = User.objects.create_user(
            email=user_data["email"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
            password=temp_password,
        )

        if hasattr(user, "must_change_password"):
            user.must_change_password = True
            user.save(update_fields=["must_change_password"])

        employee = Employee.objects.create(user=user, **validated_data)
        employee._temporary_password = temp_password

        apply_access(user, roles=roles, permissions=permissions)

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            record_audit(
                actor=request.user,
                action="create_employee",
                target_id=employee.id,
                target_label=str(employee),
                details={
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "job_title": employee.job_title,
                    "roles": roles,
                    "permissions": permissions,
                },
            )

        return employee

    # ---------- update ----------
    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        roles = validated_data.pop("roles", None)
        permissions = validated_data.pop("permissions", None)

        changes = {}

        if user_data:
            user = instance.user

            for field in ("email", "first_name", "last_name"):
                old = getattr(user, field)
                new = user_data.get(field, old)
                if old != new:
                    changes[field] = {"old": old, "new": new}
                setattr(user, field, new)

            user.save()

        for attr, value in validated_data.items():
            old_value = getattr(instance, attr)
            if old_value != value:
                changes[attr] = {"old": str(old_value), "new": str(value)}
            setattr(instance, attr, value)

        instance.save()

        if roles is not None or permissions is not None:
            old_roles, old_permissions = read_access(instance.user)

            apply_access(
                instance.user,
                roles=roles if roles is not None else old_roles,
                permissions=permissions if permissions is not None else old_permissions,
            )

            if roles is not None:
                changes["roles"] = {"new": roles}
            if permissions is not None:
                changes["permissions"] = {"new": permissions}

        request = self.context.get("request")
        if request and request.user.is_authenticated and changes:
            record_audit(
                actor=request.user,
                action="update_employee",
                target_id=instance.id,
                target_label=str(instance),
                details=changes,
            )

        return instance


class SelfProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        read_only_fields = ["email"]  # email is the login; changing it needs its own flow