from django.db.models import Sum
from django.shortcuts import render
from inventory.models import Product
from transactions.models import SalesOrder


def dashboard_home(request):
    # 1. Calculate Summary Stats
    total_products = Product.objects.count()
    total_orders = SalesOrder.objects.count()

    # Calculate Total Revenue (Sum of all order totals)
    revenue_data = SalesOrder.objects.aggregate(Sum("total_amount"))
    total_revenue = revenue_data["total_amount__sum"] or 0

    # 2. Get Recent Orders (Limit to 5)
    recent_orders = SalesOrder.objects.select_related("customer").order_by("-date")[:5]

    # 3. Get Low Stock Items (Below threshold)
    low_stock_items = Product.objects.filter(stock_quantity__lte=10)

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
        "low_stock_items": low_stock_items,
    }
    return render(request, "dashboard/home.html", context)
