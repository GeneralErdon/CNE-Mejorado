
from rest_framework import serializers
class BaseReadOnlySerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:S", read_only=True)
    modified_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:S", read_only=True)
    deleted_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:S", read_only=True)
    changed_by = serializers.CharField(source="changed_by.username", read_only=True)