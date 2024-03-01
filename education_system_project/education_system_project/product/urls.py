from django.urls import path

from product.views import GrantAccessView, AvailableProductView

urlpatterns = [
    path('<int:product_pk>/grant-access/', GrantAccessView.as_view()),
    path('available-products/', AvailableProductView.as_view()),
]
