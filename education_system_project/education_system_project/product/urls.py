from django.urls import path

from product.views import GrantAccessView, AvailableProductView, ProductLessonsView, ProductsStatistics

urlpatterns = [
    path('<int:product_pk>/grant-access/', GrantAccessView.as_view()),
    path('available-products/', AvailableProductView.as_view()),
    path('<int:product_pk>/lessons/', ProductLessonsView.as_view()),
    path('stats/', ProductsStatistics.as_view()),
]
