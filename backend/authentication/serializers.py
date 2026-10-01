from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

from access.services import read_access

User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    employee_ID = serializers.CharField()

    class Meta:
        model = User
        fields = ["public_id", "email", "first_name", "last_name", "is_staff", "must_change_password",
                  "employee_ID", "roles", "permissions"]

    def get_roles(self, user):
        return read_access(user[0])

    def get_permissiosn(self, user):
        return read_access(user[0])

    def get_employee(self, user):
        employee = getattr(user, "employee", None)
        return employee.pk if employee else None

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSummarySerializer(self.user).data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value

    def validate_new_password(self, value):
        user = self.context["request"].user
        validate_password(value, user)
        if user.check_password(value):
            raise serializers.ValidationError("The new password must be different from the current one.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])
        return user
