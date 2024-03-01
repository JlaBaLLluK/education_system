from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer

from product.models import Product, Lesson


class ProductSerializer(ModelSerializer):
    lessons_amount = IntegerField()
    author_name = CharField()

    class Meta:
        model = Product
        fields = ['product_name', 'start_time', 'price', 'min_students_amount', 'max_students_amount', 'author_name',
                  'lessons_amount']


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['lesson_name', 'url']
