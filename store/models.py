
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
    tag = models.CharField(
        "Nhãn (BEST SELLER, FRESH...)", max_length=20, blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    is_featured = models.BooleanField("Món cưng", default=False)
    is_available = models.BooleanField("Còn bán", default=True)

    def __str__(self):
        return self.name

class Order(models.Model):

    DELIVERY = "delivery"
    PICKUP = "pickup"

    ORDER_TYPE_CHOICES = [
        (DELIVERY, "Giao hàng tận nơi"),
        (PICKUP, "Đến cửa hàng lấy"),
    ]

    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHOD_CHOICES = [
        (CASH, "Tiền mặt"),
        (TRANSFER, "Chuyển khoản"),
    ]

    payment_method = models.CharField(
        "Phương thức thanh toán",
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default=CASH
    )

    amount_received = models.PositiveIntegerField(
        "Tiền khách đưa",
        default=0
    )

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, "Chờ xác nhận"),
        (CONFIRMED, "Đã xác nhận"),
        (PREPARING, "Đang chuẩn bị"),
        (COMPLETED, "Hoàn thành"),
        (CANCELLED, "Đã hủy"),
    ]

    customer_name = models.CharField("Tên khách hàng", max_length=100)
    phone = models.CharField("Số điện thoại", max_length=15)

    order_type = models.CharField(
        "Hình thức nhận hàng",
        max_length=10,
        choices=ORDER_TYPE_CHOICES
    )

    address = models.CharField(
        "Địa chỉ giao hàng",
        max_length=255,
        blank=True
    )

    note = models.TextField("Ghi chú", blank=True)

    status = models.CharField(
        "Trạng thái đơn",
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    total_price = models.PositiveIntegerField(
        "Tổng tiền",
        default=0
    )

    created_at = models.DateTimeField(
        "Ngày đặt hàng",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "Cập nhật lần cuối",
        auto_now=True
    )

    def __str__(self):
        return f"Đơn #{self.pk} - {self.customer_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    product_name = models.CharField(
        "Tên món lúc đặt",
        max_length=100
    )

    price = models.PositiveIntegerField("Giá lúc đặt")

    quantity = models.PositiveIntegerField(
        "Số lượng",
        default=1
    )

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    def get_subtotal(self):
        return self.price * self.quantity
