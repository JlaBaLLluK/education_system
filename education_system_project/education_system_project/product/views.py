from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from product.models import Product, Group


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
