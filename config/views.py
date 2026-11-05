from django.shortcuts import render
from store.models import Category, Product

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    cat_id = request.GET.get("cat")   # lọc theo danh mục: /?cat=1
    if cat_id:
        products = products.filter(category_id=cat_id)

    return render(request, "home.html", {
        "categories": categories,
        "products": products,
        "current_cat": cat_id,
    })

def menu(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    cat_id = request.GET.get("cat")
    if cat_id:
        products = products.filter(category_id=cat_id)

    return render(request, "menu.html", {
        "categories": categories,
        "products": products,
        "current_cat": cat_id,
    })