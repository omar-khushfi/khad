# views.py
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Order, product_in_order
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
  
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'quantity': 1,
            'price': str(product.price),
            'title': product.title
        }
    
    request.session['cart'] = cart
    messages.success(request, 'تم إضافة المنتج إلى السلة')
    return redirect('home')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]  # إزالة العنصر من السلة

    # إعادة حساب المجموع الإجمالي
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    # تحديث الجلسة
    request.session['cart'] = cart
    request.session['total'] = total

    messages.success(request, 'تمت إزالة المنتج من السلة.')
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        total += subtotal
        cart_items.append({
            'id': product_id,
            'title': item['title'],
            'quantity': item['quantity'],
            'price': item['price'],
            'subtotal': subtotal
        })
    
    # تأكد من تخزين المجموع في الجلسة
    request.session['total'] = total

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
    
    
    
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        quantity = int(request.POST.get('quantity', 0))
        
        # التحقق من وجود المنتج في السلة
        if product_id_str in cart:
            if quantity > 0:
                cart[product_id_str]['quantity'] = quantity  # تحديث الكمية
            else:
                del cart[product_id_str]  # إزالة العنصر إذا كانت الكمية 0
        else:
            messages.error(request, 'المنتج غير موجود في السلة.')

        # إعادة حساب المجموع الإجمالي
        total = sum(float(item['price']) * item['quantity'] for item in cart.values())

        # تحديث المجموع الإجمالي في الجلسة
        request.session['cart'] = cart
        request.session['total'] = total  # تخزين المجموع في الجلسة

        return redirect('cart')
    else:
        messages.error(request, 'طلب غير صالح.')
        return redirect('cart')
    
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'السلة فارغة')
            return redirect('cart')

        # حساب المجموع الكلي
        total = sum(float(item['price']) * item['quantity'] for item in cart.values())

        # إنشاء الطلب
        order = Order.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone_number=request.POST['phone_number'],
            total=total
        )

        # إضافة المنتجات إلى الطلب
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']  # الحصول على الكمية من السلة
            product_in_order.objects.create(
                product=product,
                order=order,
                quantity=quantity  # تخزين الكمية هنا
            )

        # تفريغ السلة
        request.session['cart'] = {}
        messages.success(request, 'تم إرسال طلبك بنجاح')
        return redirect('home')

    return render(request, 'checkout.html', {
        'cart': request.session.get('cart', {})
    })
    
    
def home_view(request):
    products = Product.objects.all()
    paginator=Paginator(products,1) 
    page_number=request.GET.get("page")
    oredr_count=Order.objects.all().count()
    try:
        products=paginator.page(page_number)
    except PageNotAnInteger: 
        products=paginator.page(1)
    except EmptyPage: 
        products=paginator.page(1)

  
    cart = request.session.get('cart', {})
    return render(request, 'home.html', {
        'products': products,
        'cart': cart,
        'oredr_count':oredr_count
    })
    
    
def us(request):
    return render(request,'us.html')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})