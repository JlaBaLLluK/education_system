from django.db.models import Count, Value
from django.db.models.functions import Concat
from django.utils import timezone
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from product.models import Product, Group, Lesson
from product.serializers import ProductSerializer


class GrantAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_pk):
        student = request.user
        product = get_object_or_404(Product, id=product_pk)
        if student.available_product == product:
            return Response({'forbidden': "Already in this product group!"})

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
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        all_products = Product.objects.filter(start_time__gt=timezone.now()).annotate(
            lessons_amount=Count('product_lessons'),
            author_name=Concat('author__first_name', Value(' '), 'author__last_name'))
        products_serializer = ProductSerializer(all_products, many=True)
        return Response(products_serializer.data, status=HTTP_200_OK)
