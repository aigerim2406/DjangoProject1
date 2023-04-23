# import to
from rest_framework import serializers
# from rest_framework.parsers import JSONParser
# from rest_framework.renderers import JSONRenderer

from .models import Aigerim


class AigerimSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Aigerim
        fields = "__all__"