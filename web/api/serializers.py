from rest_framework.serializers import ModelSerializer
from web.models import Signup


class SignupSerializer(ModelSerializer):
    class Meta:
        model = Signup
        fields = ('phonenumber',)