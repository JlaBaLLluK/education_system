from django.contrib.auth import get_user_model
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from student.models import Student


class StudentSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password']

    def save(self, **kwargs):
        Student.objects.create_user(username=self.data['username'],
                                    first_name=self.data['first_name'],
                                    last_name=self.data['last_name'],
                                    password=self.data['password'])


class LoginSerializer(Serializer):
    username = CharField(required=True)
    password = CharField(required=True)
