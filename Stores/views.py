from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import Product_infoForm, Service_infoForm, PageForm, location_gambiaForm
from .models import Product_info, Service_info, UserProfile, Usercreatedpage, OrderItem, Order, Ordered
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm, OrderForm, TariffsForm
from .models import UserProfile, User_Page, Tariffs, Tariff_query, location_gambia
from .cart import Cart
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse


from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict


from django import forms
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


def aboutus(request):
    return render(request, 'index.html')


def home(request):
    all_pages = Usercreatedpage.objects.all().order_by('-id')
    return render(request, 'home.html', {'all_pages': all_pages})


def homeproducts(request):
    all_products = Product_info.objects.all()[20:50]
    new_products = Product_info.objects.all().order_by('-id')[:10]
    return render(request, 'products.html', {'all_products': all_products, 'new_products': new_products})


def homeservices(request):
    all_services = Service_info.objects.all()
    return render(request, 'services.html', {'all_services': all_services})


def Search_page(request):
    q = request.GET.get('q')

    if q:
        vector = SearchVector('page_name', 'page_description', 'location', 'user')
        query = SearchQuery(q)
        description_headline = SearchHeadline('page_description', query)
        location_headline = SearchHeadline('location', query)

        pages = Usercreatedpage.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=description_headline).annotate(highlight=location_headline).filter(rank__gte=0.01).order_by('-rank')

    else:
        pages = None

    context = {'pages': pages}
    return render(request, 'searchedpages.html', context)


def Search_productpage(request):
    p = request.GET.get('p')

    if p:
        vector = SearchVector('product_name', 'product_description', 'product_price', 'page_owner')
        query = SearchQuery(p)

        products = Product_info.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.01).order_by('-rank')

    else:
        products = None

    context = {'products': products}
    return render(request, 'searchedproducts.html', context)


def Search_servicepage(request):
    if request.method == "POST":
        searched_services = request.POST.get('searched_services', False)
        services = Service_info.objects.filter(service_name__contains=searched_services)
        return render(request, 'searchedservices.html', {'searched_services': searched_services, 'services': services})
    else:
        return render(request, 'searchedservices.html', {})


def login_account(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            # Redirect to a success page.
        else:
            messages.success(request, ('Error, invalid password or username, try Again'))
            return redirect('login-user')
            # Return an 'invalid login' error message.
    return render(request, 'LoginBase.html', {})


def logout_account(request):
    logout(request)
    return redirect('home')


def signup_account(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,  password=password)
            login(request, user)
            messages.success(request, ("Congratulations, you've signed up"))
            return redirect('home')
    else:
        form = SignupForm

    return render(request, 'signup.html', {'form': form})


def view_products(request, pk):
    view_products = Product_info.objects.get(id=pk)
    return render(request, 'WriberProductView.html', {'view_products': view_products})


def view_services(request, pk):
    view_services = Service_info.objects.get(id=pk)
    return render(request, 'WriberServiceView.html', {'view_services': view_services})


def account_profile(request, pk=None):
    if request.user.is_authenticated:
        accountprofile = UserProfile.objects.get(user_id=pk)
        pages = Usercreatedpage.objects.filter(user_id=pk)
        products = Product_info.objects.filter(user_id=pk)[:100]
        return render(request, 'Dashboardtemplates/index.html', {'accountprofile': accountprofile, 'pages': pages,
                                                                 'products': products})
    else:
        return render(request, 'Dashboardtemplates/index.html', {})


def account_page(request, pk=None):
    if request.user.is_authenticated:
        pages = Usercreatedpage.objects.filter(user_id=pk)
        orders = Order.objects.filter(created_by=request.user)
        return render(request, 'Dashboardtemplates/form-elements.html', {'pages': pages, 'orders': orders})
    else:
        return render(request, 'Dashboardtemplates/form-elements.html', {})


def orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(created_by=request.user).order_by('-id')
        return render(request, 'Dashboardtemplates/buttons.html', {'orders': orders})
    else:
        return render(request, 'Dashboardtemplates/buttons.html', {})


def user_page(request, pk=None):
    view_page = User_Page.objects.get(page_id__id=pk)
    product_forpage = Product_info.objects.filter(page_owner_id=pk)
    service_forpage = Service_info.objects.filter(page_owner_id=pk)
    tariff_button = Tariff_query.objects.filter(tariff__page_owner__id=pk)
    return render(request, 'WriberPageView.html', {'view_page': view_page,
                                                   'product_forpage': product_forpage,
                                                   'service_forpage': service_forpage,
                                                   'tariff_button': tariff_button})


def page_dashboard(request, pk):
    if request.user.is_authenticated:
        product_page = Product_info.objects.filter(page_owner_id=pk)
        service_page = Service_info.objects.filter(page_owner_id=pk)
        return render(request, 'Dashboardtemplates/productpagelist.html', {'product_page': product_page,
                                                      'service_page': service_page})
    else:
        return render(request, 'Dashboardtemplates/productpagelist.html', {})


def perpage_product(request, pk):
    if request.user.is_authenticated:
        products = Product_info.objects.filter(user_id=pk)
        return render(request, 'Dashboardtemplates/productlist.html', {'products': products})
    else:
        return render(request, 'Dashboardtemplates/productlist.html', {})


def addnew_page(request):
    if request.user.is_authenticated:
        form = PageForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                page = form.save(commit=False)
                page.user = request.user
                page.save()
                messages.success(request, ('Your page has been created successfully!!'))
                return redirect(page.get_absolute_url())

        else:
            return render(request, 'Dashboardtemplates/addpage.html', {'form': form})
    else:
        return render(request, 'Dashboardtemplates/addpage.html', {})


def addnew_product(request):
    if request.user.is_authenticated:
        page = Product_info.objects.filter(user=request.user)
        form = Product_infoForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            print(form)
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                product.save()
                return redirect(product.get_absolute_url())
        else:
            form.fields["page_owner"].queryset=Usercreatedpage.objects.filter(user=request.user)
        return render(request, 'Dashboardtemplates/Addproduct.html', {'form': form})
    else:
        return render(request, 'Dashboardtemplates/Addproduct.html', {})


@login_required
def addnew_product_homescreen(request):
    if request.user.is_authenticated:
        page = Product_info.objects.filter(user=request.user)
        form = Product_infoForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            print(form)
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                product.save()
                return redirect(product.get_absolute_url())
        else:
            form.fields["page_owner"].queryset = Usercreatedpage.objects.filter(user=request.user)
        return render(request, 'WriberProductsAddHomeScreen.html', {'form': form})
    else:
        return render(request, 'WriberProductsAddHomeScreen.html', {})


@login_required
def addnew_page_homescreen(request):
    if request.user.is_authenticated:
        form = PageForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                page = form.save(commit=False)
                page.user = request.user
                page.save()
                messages.success(request, ('Your page has been created successfully!!'))
                return redirect(page.get_absolute_url())

        else:
            return render(request, 'WriberPageAddHomeScreen.html', {'form': form})
    else:
        return render(request, 'WriberPageAddHomeScreen.html', {})


def addnew_service(request):
    if request.user.is_authenticated:
        page = Service_info.objects.filter(user=request.user)
        form = Service_infoForm(request.POST or None)
        if request.method == "POST":
            print(form)
            if form.is_valid():
                service = form.save(commit=False)
                service.user = request.user
                service.save()
                return redirect(service.get_absolute_url())
        else:
            form.fields["page_owner"].queryset=Usercreatedpage.objects.filter(user=request.user)
        return render(request, 'WriberServicesAdd.html', {'form': form})
    else:
        return render(request, 'WriberServicesAdd.html', {})


def update_products(request, pk):
    show_products = Product_info.objects.get(id=pk)
    form = Product_infoForm(request.POST or None, request.FILES or None, instance=show_products)
    form.fields["page_owner"].queryset = Usercreatedpage.objects.filter(user=request.user)
    if form.is_valid():
        form.save()
        return render(request, 'Updatedproductalert.html')
    return render(request, 'Dashboardtemplates/updateproduct.html', {'show_products': show_products, 'form': form})


def update_services(request, pk):
    show_services = Service_info.objects.get(id=pk)
    form = Service_infoForm(request.POST or None, request.FILES or None, instance=show_services)
    if form.is_valid():
        form.save()
        return render(request, 'Updatedservicealert.html')
    return render(request, 'WriberServicesUpdate.html', {'show_services': show_services, 'form': form})


def update_page(request, pk):
    view_page = Usercreatedpage.objects.get(id=pk)
    form = PageForm(request.POST or None, request.FILES or None, instance=view_page)
    if form.is_valid():
        form.save()
        return render(request, 'Updatedpagealert.html')
    return render(request, 'Dashboardtemplates/updatedpage.html', {'view_page': view_page, 'form': form})


def delete_wriber_products_ondash(request, pk):
    show_products = Product_info.objects.get(id=pk)
    show_products.delete()
    return render(request, 'Dashboardtemplates/productlist.html')


def delete_wriber_services(request, pk):
    show_services = Service_info.objects.get(id=pk)
    show_services.delete()
    return redirect()


def delete_wriber_products_onpagemanage(request, pk):
    show_products = Product_info.objects.get(id=pk)
    show_products.delete()
    return render(request, 'Updatedproductalert.html')


def add_to_cart(request, pk):
    cart = Cart(request)
    cart.add(pk)

    return redirect('cart-view')


def cart_view(request):
    cart = Cart(request)

    return render(request, 'CartView.html', {'cart': cart})


def remove_from_cart(request, pk):
    cart = Cart(request)
    cart.remove(pk)

    return redirect('cart-view')


def change_quantity(request, pk):
    action = request.GET.get('action', '')

    if action:
        quantity = 1
        if action == 'decrease':
            quantity = -1
        cart = Cart(request)
        cart.add(pk, quantity, True)
    return redirect('cart-view')


@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():

            total_price = 0

            for item in cart:
                product = item['product']
                total_price = total_price + product.product_price * int(item['quantity'])

                if item['quantity'] > product.stock_available:
                    return render(request, 'checkoutfailed.html')
                else:
                    order = form.save(commit=False)
                    order.created_by = request.user
                    order.paid_amount = total_price
                    order.save()

                    for item in cart:
                        product = item['product']
                        quantity = int(item['quantity'])
                        price = product.product_price * int(item['quantity'])

                        item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

                        product = Product_info.objects.get(id=item.product.id)

                        product.stock_available = product.stock_available - item.quantity
                        product.save()

                    cart.clear()

                    orders = Order.objects.filter(created_by=request.user)

                    items = OrderItem.objects.filter(order=order)

                    item_user = OrderItem.objects.filter(order=order)

                    if item_user:
                        for user in item_user:
                            email = user.product.user.email

                    user_email = email
                    subject = "An order was made!!!"
                    from_email = settings.EMAIL_HOST_USER
                    to_email = [settings.EMAIL_RECIEVER, settings.EMAIL_RECIEVER_ALEX, settings.EMAIL_RECIEVER_EMEKA, user_email]
                    stuff = settings.BASE_DIR
                    fullpath = stuff.joinpath("Stores/templates/order_info_email.html")
                    fullpath = stuff / ("Stores/templates/order_info_email.html")
                    with open(fullpath) as f:
                        # with open(settings.BASE_DIR + "/Stores/templates/order_info_email.html") as f:
                        order_message = f.read()
                    order_message = EmailMultiAlternatives(subject=subject, body=order_message, from_email=from_email, to=to_email)
                    html_template = get_template('order_info_email.html').render({'orders': orders, 'items': items, 'cart': cart})
                    order_message.attach_alternative(html_template, "text/html")
                    order_message.send()
                    # order_message = """This is the order info"""
                    # send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=order_message, fail_silently=False)

                    return render(request, 'ConfirmOrder.html')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'cart': cart, 'form': form})


def order_items(request, pk):
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=order)
        return render(request, 'Dashboardtemplates/orderinfo.html', {'order': order, 'items': items})
    else:
        return render(request, 'Dashboardtemplates/orderinfo.html', {})


def order_history(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(product__user=request.user).order_by('-id')
        return render(request, 'Dashboardtemplates/tables.html', {'order_items': order_items})
    else:
        return render(request, 'Dashboardtemplates/tables.html', {})


def view_locations(request, pk):
    tariff_detail = location_gambia.objects.get(id=pk)
    return render(request, 'WriberTariffid.html', {'tariff_detail': tariff_detail})


def dashboard_tariff(request):
    if request.user.is_authenticated:
        tariff_page = Tariffs.objects.filter(user=request.user)
        return render(request, 'Dashboardtariff.html', {'tariff_page': tariff_page})
    else:
        return render(request, 'Dashboardtariff.html', {})


def tariff_detail(request, pk=None):
    if request.user.is_authenticated:
        tariff = Tariffs.objects.get(id=pk)
        detail = location_gambia.objects.filter(tariff_owner_id=pk)
        return render(request, 'tariffdetail.html', {'tariff': tariff, 'detail': detail})
    else:
        return render(request, 'tariffdetail.html', {})


def view_tariff(request, pk=None):
    tariff_button = Tariffs.objects.filter(page_owner_id=pk)
    locations_forpage = location_gambia.objects.filter(page_owner_id=pk)
    return render(request, 'WriberTariffView.html', {'tariff_button': tariff_button, 'locations_forpage': locations_forpage})


def view_tariff_page(request, pk=None):
    locations_forpage = location_gambia.objects.filter(tariff_owner_id=pk)
    return render(request, 'TariffView.html', {'locations_forpage': locations_forpage})


def addnew_tariff(request):
    if request.user.is_authenticated:
        page = location_gambia.objects.filter(user=request.user)
        form = TariffsForm(request.POST or None)
        if request.method == "POST":
            print(form)
            if form.is_valid():
                tariff = form.save(commit=False)
                tariff.user = request.user
                tariff.save()
                return render(request, 'Dashboardtariff.html')
        else:
            form.fields["page_owner"].queryset = Usercreatedpage.objects.filter(user=request.user)
        return render(request, 'WriberTariffAdd.html', {'form': form})
    else:
        return render(request, 'WriberTariffAdd.html', {})


# this add tariff view function must me made in a way that allows for users to update and add new tariffs.
def addnew_tariff_location(request):
    if request.user.is_authenticated:
        page = location_gambia.objects.filter(user=request.user)
        form = location_gambiaForm(request.POST or None)
        if request.method == "POST":
            print(form)
            if form.is_valid():
                locations = form.save(commit=False)
                locations.user = request.user
                locations.save()
                return redirect(locations.get_absolute_url())
        else:
            form.fields["page_owner"].queryset = Usercreatedpage.objects.filter(user=request.user)
            form.fields["tariff_owner"].queryset = Tariffs.objects.filter(user=request.user)
        return render(request, 'WriberTariffmodify.html', {'form': form})
    else:
        return render(request, 'WriberTariffmodify.html', {})


def update_location(request, pk):
    locations = location_gambia.objects.get(id=pk)
    form = location_gambiaForm(request.POST or None, request.FILES or None, instance=locations)
    form.fields["page_owner"].queryset = Usercreatedpage.objects.filter(user=request.user)
    form.fields["tariff_owner"].queryset = Tariffs.objects.filter(user=request.user)
    if form.is_valid():
        form.save()
        return render(request, 'Dashboardtemplates/form-elements.html')
    return render(request, 'WriberTariffUpdate.html', {'locations': locations, 'form': form})


def update_tariff(request, pk):
    tariffs = Tariffs.objects.get(id=pk)
    form = TariffsForm(request.POST or None, request.FILES or None, instance=tariffs)
    form.fields["page_owner"].queryset = Usercreatedpage.objects.filter(user=request.user)
    if form.is_valid():
        form.save()
        return render(request, 'Dashboardtemplates/form-elements.html')
    return render(request, 'WriberTarifflistupdate.html', {'tariffs': tariffs, 'form': form})


def settings_dashboard(request, pk):
    if request.user.is_authenticated:
        accountprofile = UserProfile.objects.get(user_id=pk)
        return render(request, 'Dashboardtemplates/settings.html', {'accountprofile': accountprofile})
    else:
        return render(request, 'Dashboardtemplates/settings.html', {})


def update_account_profile(request):
    if request.user.is_authenticated:
        accountprofile = User.objects.get(id=request.user.id)
        form = SignupForm(request.POST or None, request.FILES or None, instance=accountprofile)
        if form.is_valid():
            form.save()
            login(request, accountprofile)
            messages.success(request, ("Congratulations, your profile is updated"))
            return render(request, 'accountupdatedalert.html')
        return render(request, 'Dashboardtemplates/updateaccount.html', {'accountprofile': accountprofile, 'form': form})
    else:
        return render(request, 'Dashboardtemplates/updateaccount.html', {})


# allow users to be able to view and see all there products on one page and allow them to be able to add products to the database without having a page

# allow users to choose their location choice for the delivery, from the options presented by the checkout
# page which can be done by query setting the checkout page just like i did in the update page
#sudo dscl . -create /Users/postgres UserShell /bin/sh

#sudo dscl . -create /Users/postgres NFSHomeDirectory /Library/PostgreSQL


# Charts For User Details
@staff_member_required
def get_user_filter_options(request):
    grouped_profiles = UserProfile.objects.annotate(year=ExtractYear("created_at")).values("year").order_by(
        "-year").distinct()
    options = [profile["year"] for profile in grouped_profiles]

    return JsonResponse({
        "options": options,
    })


@staff_member_required
def get_user_growth_chart(request, year):
    profiles = UserProfile.objects.filter(created_at__year=year)
    grouped_profiles = profiles.annotate(price=F("pk")).annotate(month=ExtractMonth("created_at")) \
        .values("month").annotate(average=Sum("pk")/19.571428).values("month", "average").order_by("month")

    users_dict = get_year_dict()

    for group in grouped_profiles:
        users_dict[months[group["month"] - 1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"New Users in {year}",
        "data": {
            "labels": list(users_dict.keys()),
            "datasets": [{
                "label": "New Users",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(users_dict.values()),
            }]
        },
    })


# Chart For Page Details
def get_page_filter_options(request):
    grouped_pages = Usercreatedpage.objects.annotate(year=ExtractYear("created_at")).values("year").order_by(
        "-year").distinct()
    options = [page["year"] for page in grouped_pages]

    return JsonResponse({
        "options": options,
    })


def get_page_growth_chart(request, year):
    pages = Usercreatedpage.objects.filter(created_at__year=year)
    grouped_pages = pages.annotate(price=F("pk")).annotate(month=ExtractMonth("created_at")) \
        .values("month").annotate(average=Sum("pk")/14.66666).values("month", "average").order_by("month")

    pages_dict = get_year_dict()

    for group in grouped_pages:
        pages_dict[months[group["month"] - 1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"New Pages in {year}",
        "data": {
            "labels": list(pages_dict.keys()),
            "datasets": [{
                "label": "New Pages",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(pages_dict.values()),
            }]
        },
    })


# Chart For Product Details
@staff_member_required
def get_product_filter_options(request):
    grouped_products = Product_info.objects.annotate(year=ExtractYear("created_at")).values("year").order_by(
        "-year").distinct()
    options = [product["year"] for product in grouped_products]

    return JsonResponse({
        "options": options,
    })


@staff_member_required
def get_product_growth_chart(request, year):
    products = Product_info.objects.filter(created_at__year=year)
    grouped_products = products.annotate(price=F("pk")).annotate(month=ExtractMonth("created_at")) \
        .values("month").annotate(average=Sum("pk")/64.0454545).values("month", "average").order_by("month")

    products_dict = get_year_dict()

    for group in grouped_products:
        products_dict[months[group["month"] - 1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"New Products in {year}",
        "data": {
            "labels": list(products_dict.keys()),
            "datasets": [{
                "label": "New Products",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(products_dict.values()),
            }]
        },
    })


# Charts For Order Detials
@staff_member_required
def get_filter_options(request):
    grouped_orders = Order.objects.annotate(year=ExtractYear("created_at")).values("year").order_by("-year").distinct()
    options = [order["year"] for order in grouped_orders]

    return JsonResponse({
        "options": options,
    })


@staff_member_required
def get_order_sales_chart(request, year):
    orders = Order.objects.filter(created_at__year=year)
    grouped_orders = orders.annotate(price=F("paid_amount")).annotate(month=ExtractMonth("created_at")) \
        .values("month").annotate(average=Sum("paid_amount")).values("month", "average").order_by("month")

    sales_dict = get_year_dict()

    for group in grouped_orders:
        sales_dict[months[group["month"] - 1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Amount (D)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(sales_dict.values()),
            }]
        },
    })


@staff_member_required
def get_order_number_chart(request, year):
    orders = Order.objects.filter(created_at__year=year)
    grouped_orders = orders.annotate(price=F("pk")).annotate(month=ExtractMonth("created_at")) \
        .values("month").annotate(average=Sum("pk")).values("month", "average").order_by("month")

    orders_dict = get_year_dict()

    for group in grouped_orders:
        orders_dict[months[group["month"] - 1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Orders in {year}",
        "data": {
            "labels": list(orders_dict.keys()),
            "datasets": [{
                "label": "NO. Of Orders",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(orders_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_per_customer_chart(request, year):
    orders = Order.objects.filter(created_at__year=year)
    grouped_orders = orders.annotate(price=F("paid_amount")).annotate(month=ExtractMonth("created_at")) \
        .values("month").annotate(average=Avg("paid_amount")).values("month", "average").order_by("month")

    spend_per_customer_dict = get_year_dict()

    for group in grouped_orders:
        spend_per_customer_dict[months[group["month"] - 1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(spend_per_customer_dict.keys()),
            "datasets": [{
                "label": "Amount (D)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(spend_per_customer_dict.values()),
            }]
        },
    })


@staff_member_required
def statistics_view(request):
    return render(request, "statistics.html", {})


@staff_member_required
def user_statistics_view(request):
    return render(request, "userstatistics.html", {})


@staff_member_required
def product_statistics_view(request):
    return render(request, "productstatistics.html", {})


@staff_member_required
def page_statistics_view(request):
    return render(request, "pagestatistics.html", {})
