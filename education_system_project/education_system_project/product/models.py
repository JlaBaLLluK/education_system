from django.db import models


class ProductAuthor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    information = models.TextField(blank=False)

    class Meta:
        db_table = 'product_authors'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    product_name = models.CharField(max_length=128)
    start_time = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    min_students_amount = models.IntegerField(blank=False)
    max_students_amount = models.IntegerField(blank=False)
    author = models.ForeignKey(ProductAuthor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.product_name


class Group(models.Model):
    group_name = models.CharField(blank=False, max_length=128)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    current_students_amount = models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.group_name


class Lesson(models.Model):
    lesson_name = models.CharField(blank=False, max_length=128)
    url = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'lessons'

    def __str__(self):
        return self.lesson_name
