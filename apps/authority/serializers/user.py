# !/usr/bin/env python
# Time 19-05-06
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework import serializers
from ..models import ExtendUser, Group

__all__ = [
    'UserSerializer'
]


class UserSerializer(serializers.ModelSerializer):
    group_name = serializers.StringRelatedField(source="get_group_name", read_only=True)
    email8531 = serializers.StringRelatedField(source="get_8531email", read_only=True)
    groups = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=Group.objects.all())

    class Meta:
        model = ExtendUser
        fields = (
            'id', 'uuid', 'is_active', 'phone', 'username', 'full_name', 'group_name', 'email8531', 'groups', 'email',
            'info', 'have_qrcode', 'expire',
        )
        read_only_fields = (
            'id',
        )


class UserDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtendUser
        fields = (
            'id', 'uuid',
        )

    def update(self, instance, validated_data):
        instance.is_active = False
        instance.visible()
        return super(UserDeleteSerializer, self).update(instance, {})