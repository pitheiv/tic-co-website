from django.db import models

class Category(models.Model):
    name = models.CharField("Tên danh mục", max_length=50)
    icon = models.CharField("Icon (emoji)", max_length=10, blank=True)
    description = models.CharField("Mô tả ngắn", max_length=60, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Tên món", max_length=100)
    description = models.CharField("Mô tả", max_length=200, blank=True)
    price = models.PositiveIntegerField("Giá (đ)")
    image = models.ImageField("Ảnh", upload_to="products/")
    tag = models.CharField("Nhãn (BEST SELLER, FRESH...)", max_length=20, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    is_featured = models.BooleanField("Món cưng", default=False)
    is_available = models.BooleanField("Còn bán", default=True)

    def __str__(self):
        return self.name