from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category

# ==========================
# PRODUCT MANAGEMENT VIEWS
# ==========================

# 1. VIEW: LIST ALL PRODUCTS
def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})

# 2. VIEW: ADD STOCK (RESTOCK)
def add_stock(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        # Get the product and update the quantity
        product = get_object_or_404(Product, id=product_id)
        product.stock_quantity += quantity
        product.save()

        # Redirect back to the inventory list
        return redirect('product_list')

    # If it's a GET request, just show the form with all products
    products = Product.objects.all()
    return render(request, 'inventory/add_stock.html', {'products': products})

# 3. VIEW: CREATE NEW PRODUCT
def add_product(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        low_stock_threshold = request.POST.get('low_stock_threshold')

        # Get the actual Category object so we can assign it
        category = get_object_or_404(Category, id=category_id)

        # Create the new Product in the database
        Product.objects.create(
            name=name,
            category=category,
            sku=sku,
            price=price,
            stock_quantity=stock_quantity,
            low_stock_threshold=low_stock_threshold
        )

        return redirect('product_list')

    # GET request: Show the form with all available categories
    categories = Category.objects.all()
    return render(request, 'inventory/add_product.html', {'categories': categories})

# 4. VIEW: EDIT EXISTING PRODUCT
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.price = request.POST.get('price')
        product.low_stock_threshold = request.POST.get('low_stock_threshold')

        # Handle Category Change
        category_id = request.POST.get('category')
        product.category = get_object_or_404(Category, id=category_id)

        product.save()
        return redirect('product_list')

    categories = Category.objects.all()
    return render(request, 'inventory/edit_product.html', {
        'product': product,
        'categories': categories
    })

# 5. VIEW: DELETE PRODUCT (The Missing Piece!)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'inventory/delete_product.html', {'product': product})


# ==========================
# CATEGORY MANAGEMENT VIEWS
# ==========================

# 6. VIEW: LIST ALL CATEGORIES
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})

# 7. VIEW: ADD NEW CATEGORY
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        Category.objects.create(name=name, description=description)
        return redirect('category_list')

    return render(request, 'inventory/add_category.html')
