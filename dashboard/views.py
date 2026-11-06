import json

from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from store.models import Category, Order, OrderItem, Product


# Chỉ nhân viên (staff) đã đăng nhập mới vào được
staff_required = user_passes_test(
    lambda user: user.is_authenticated and user.is_staff,
    login_url="/dashboard/login/",
)


@staff_required
def index(request):
    today = timezone.localdate()

    today_orders = Order.objects.filter(created_at__date=today)

    today_revenue = today_orders.filter(
        status=Order.COMPLETED
    ).aggregate(total=Sum("total_price"))["total"] or 0

    pending_orders = Order.objects.filter(
        status__in=[Order.PENDING, Order.CONFIRMED, Order.PREPARING]
    ).count()

    context = {
        "today_revenue": today_revenue,
        "today_orders": today_orders.count(),
        "pending_orders": pending_orders,
        "product_count": Product.objects.count(),
        "recent_orders": Order.objects.order_by("-created_at")[:8],
    }

    return render(request, "dashboard/index.html", context)


@staff_required
def pos(request):
    context = {
        "products": Product.objects.filter(
            is_available=True
        ).select_related("category"),
        "categories": Category.objects.all(),
    }

    return render(request, "dashboard/pos.html", context)


def _error(message, status=400):
    return JsonResponse({"success": False, "message": message}, status=status)


@staff_required
@require_POST
def checkout(request):
    # 1. Đọc dữ liệu trình duyệt gửi lên (chỉ lấy id món và số lượng)
    try:
        data = json.loads(request.body)
        amount_received = int(data.get("amount_received", 0))
        raw_items = data.get("items", [])

        if not isinstance(raw_items, list) or not raw_items:
            return _error("Giỏ hàng đang trống.")

        if amount_received < 0:
            return _error("Số tiền không hợp lệ.")

        quantities = {}
        for item in raw_items:
            product_id = int(item["id"])
            quantity = int(item["quantity"])

            if not 0 < quantity <= 99:
                return _error("Số lượng không hợp lệ.")

            quantities[product_id] = quantities.get(product_id, 0) + quantity

    except (ValueError, TypeError, KeyError, AttributeError):
        # json.JSONDecodeError cũng là một loại ValueError nên được bắt ở đây
        return _error("Dữ liệu gửi lên không hợp lệ.")

    # 2. Lấy món từ database và tự tính tiền (không tin số tiền từ trình duyệt)
    products = list(
        Product.objects.filter(id__in=quantities, is_available=True)
    )

    if len(products) != len(quantities):
        return _error("Có món không tồn tại hoặc đã ngừng bán.")

    total = sum(product.price * quantities[product.id] for product in products)

    if amount_received < total:
        return _error("Tiền khách đưa chưa đủ!")

    # 3. Lưu đơn hàng
    with transaction.atomic():
        order = Order.objects.create(
            customer_name="Khách lẻ",
            phone="",
            order_type=Order.PICKUP,
            status=Order.COMPLETED,   # bán tại quầy, trả tiền xong là hoàn tất
            payment_method=Order.CASH,
            amount_received=amount_received,
            total_price=total,
        )

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=quantities[product.id],
            )
            for product in products
        ])

    return JsonResponse({
        "success": True,
        "message": "Thanh toán thành công!",
        "order_id": order.id,
        "total": total,
        "amount_received": amount_received,
        "change": amount_received - total,
    })