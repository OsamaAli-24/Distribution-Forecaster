import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum, F  # <--- Added 'F' here
from django.db.models.functions import TruncDate
from django.shortcuts import render
from inventory.models import Product
from transactions.models import SalesItem, SalesOrder


def dashboard_home(request):
    # --- EXISTING STATS ---
    total_products = Product.objects.count()
    total_orders = SalesOrder.objects.count()
    revenue_data = SalesOrder.objects.aggregate(Sum("total_amount"))
    total_revenue = revenue_data["total_amount__sum"] or 0
    recent_orders = SalesOrder.objects.select_related("customer").order_by("-date")[:5]

    # ✅ FIXED: Compare stock vs. its own threshold (instead of hardcoded 10)
    low_stock_items = Product.objects.filter(stock_quantity__lte=F('low_stock_threshold'))

    # --- NEW: PREPARE DATA FOR CHARTS ---

    # 1. Daily Sales (Line Chart)
    daily_sales = (
        SalesOrder.objects.annotate(day=TruncDate("date"))
        .values("day")
        .annotate(total=Sum("total_amount"))
        .order_by("day")
    )

    # Convert to simple lists for JavaScript
    chart_dates = [x["day"].strftime("%Y-%m-%d") for x in daily_sales]
    chart_revenue = [float(x["total"]) for x in daily_sales]

    # 2. Top Selling Products (Bar Chart)
    top_products = (
        SalesItem.objects.values("product__name")
        .annotate(total_qty=Sum("quantity"))
        .order_by("-total_qty")[:5]
    )

    top_product_names = [x["product__name"] for x in top_products]
    top_product_qtys = [x["total_qty"] for x in top_products]

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
        "low_stock_items": low_stock_items,
        # Pass the chart data as JSON strings
        "chart_dates": json.dumps(chart_dates, cls=DjangoJSONEncoder),
        "chart_revenue": json.dumps(chart_revenue, cls=DjangoJSONEncoder),
        "top_product_names": json.dumps(top_product_names, cls=DjangoJSONEncoder),
        "top_product_qtys": json.dumps(top_product_qtys, cls=DjangoJSONEncoder),
    }
    return render(request, "dashboard/home.html", context)
