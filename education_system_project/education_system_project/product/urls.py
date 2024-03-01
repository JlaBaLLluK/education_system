from django.urls import path

from product.views import GrantAccessView

urlpatterns = [
    path('<int:product_pk>/grant-access/', GrantAccessView.as_view()),
]
