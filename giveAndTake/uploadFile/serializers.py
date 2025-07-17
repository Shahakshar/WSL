from rest_framework import serializers

class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    name = serializers.CharField()
    owner = serializers.EmailField()
    original_owner = serializers.EmailField()

class TransferFileSerializer(serializers.Serializer):
    public_id = serializers.CharField()
    from_user = serializers.EmailField()
    to_user = serializers.EmailField()

class RevokeTransferSerializer(serializers.Serializer):
    public_id = serializers.CharField()
    original_owner = serializers.EmailField()

class GetFileSerializer(serializers.Serializer):
    email = serializers.EmailField()
