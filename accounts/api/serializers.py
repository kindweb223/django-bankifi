from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
    # Useful to add calculated data to the fields
    follower_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'follower_count'
        ]

    def get_follower_count(self, obj):
        return 0