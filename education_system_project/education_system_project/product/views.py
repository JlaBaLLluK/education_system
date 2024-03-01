from django.db.models import Count, Value, ExpressionWrapper, FloatField
from django.db.models.functions import Concat
from django.utils import timezone
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from product.models import Product, Group, Lesson
from product.serializers import ProductSerializer, LessonSerializer, ProductStatsSerializer
from student.models import Student


class GrantAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_pk):
        student = request.user
        product = get_object_or_404(Product, id=product_pk)
        if student.available_product == product:
            return Response({'forbidden': "Already in this product group!"}, status=HTTP_403_FORBIDDEN)

        student.available_product = product
        student.save()
        groups = Group.objects.filter(product=product).select_related('product')
        if len(groups) == 0:
            return self.make_new_group(student, product, len(groups) + 1)

        for i, group in enumerate(groups):
            if group.current_students_amount < group.product.max_students_amount:
                student.group = group
                student.save()
                group.current_students_amount += 1
                group.save()
                return Response({'success': f'Access granted, distributed to group {i + 1}'}, status=HTTP_200_OK)
        else:
            return self.make_new_group(student, product, len(groups) + 1)

    @staticmethod
    def make_new_group(student, product, group_num):
        group = Group(group_name=f'{product.product_name} group {group_num}', product=product)
        group.save()
        student.group = group
        student.save()
        group.current_students_amount += 1
        group.save()
        return Response({'success': 'New group created, access granted!'}, status=HTTP_200_OK)


class AvailableProductView(ListAPIView):
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        all_products = Product.objects.filter(start_time__gt=timezone.now()).annotate(
            lessons_amount=Count('lessons_on_product'),
            author_name=Concat('author__first_name', Value(' '), 'author__last_name'))
        products_serializer = ProductSerializer(all_products, many=True)
        return Response(products_serializer.data, status=HTTP_200_OK)


class ProductLessonsView(APIView):

    @staticmethod
    def get(request, product_pk):
        if request.user.available_product is None or request.user.available_product.id != product_pk:
            return Response({'forbidden': "You don't have access to this product!"}, status=HTTP_403_FORBIDDEN)

        lessons = Lesson.objects.filter(product=product_pk)
        if len(lessons) == 0:
            return Response({'No lessons'})

        return Response(LessonSerializer(lessons, many=True).data, status=HTTP_200_OK)


class ProductsStatistics(APIView):

    def get(self, request):
        total_students_amount = Student.objects.count()
        all_products = Product.objects.annotate(students_amount=Count('students_on_product', distinct=True),
                                                groups_amount=Count('groups_on_product', distinct=True))
        stats = []
        for product in all_products:
            stats.append(
                {
                    'product': product.product_name,
                    'students_on_product': product.students_amount,
                    'student_in_group_percentage': product.students_amount / (
                            product.groups_amount * product.max_students_amount) * 100
                    if product.groups_amount != 0 else 0,
                    'student_in_product_percentage': product.students_amount / total_students_amount * 100
                }
            )

        return Response(stats, status=HTTP_200_OK)
