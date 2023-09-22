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
from django.conf import settings


from django import forms
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template



def home(request):
    all_pages = Usercreatedpage.objects.all()
    return render(request, 'home.html', {'all_pages': all_pages})


def homeproducts(request):
    all_products = Product_info.objects.all()
    return render(request, 'products.html', {'all_products': all_products})


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
    return render(request, 'loginpage.html', {})


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

    return render(request, 'signuppage.html', {'form': form})


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
        return render(request, 'WriberAccount.html', {'accountprofile': accountprofile, 'pages': pages})
    else:
        return render(request, 'WriberAccount.html', {})


def account_page(request, pk=None):
    if request.user.is_authenticated:
        pages = Usercreatedpage.objects.filter(user_id=pk)
        orders = Order.objects.filter(created_by=request.user)
        return render(request, 'WriberPages.html', {'pages': pages, 'orders': orders})
    else:
        return render(request, 'WriberPages.html', {})


def orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(created_by=request.user)
        return render(request, 'Orders.html', {'orders': orders})
    else:
        return render(request, 'Orders.html', {})


def user_page(request, pk=None):
    view_page = User_Page.objects.get(page_id=pk)
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
        return render(request, 'DashBoardPage.html', {'product_page': product_page,
                                                      'service_page': service_page})
    else:
        return render(request, 'DashoardPage.html', {})


def perpage_product(request, pk):
    if request.user.is_authenticated:
        products = Product_info.objects.filter(user_id=pk)
        return render(request, 'DashboardProduct.html', {'products': products})
    else:
        return render(request, 'DashboardProduct.html', {})


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
            return render(request, 'WriberPageAdd.html', {'form': form})
    else:
        return render(request, 'WriberPageAdd.html', {})


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
        return render(request, 'WriberProductsAdd.html', {'form': form})
    else:
        return render(request, 'WriberProductsAdd.html', {})


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
    return render(request, 'WriberProductsUpdate.html', {'show_products': show_products, 'form': form})


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
    return render(request, 'WriberPageUpdate.html', {'view_page': view_page, 'form': form})


def delete_wriber_products_ondash(request, pk):
    show_products = Product_info.objects.get(id=pk)
    show_products.delete()
    return render(request, 'DashboardProduct.html')


def delete_wriber_services(request, pk):
    show_services = Service_info.objects.get(id=pk)
    show_services.delete()
    return redirect()


def delete_wriber_products_onpagemanage(request, pk):
    show_products = Product_info.objects.get(id=pk)
    show_products.delete()
    return render(request, 'DashBoardPage.html')


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

                    item_user = OrderItem.objects.get(order=order)

                    user_email = item_user.product.user.email

                    subject = "An order was made!!!"
                    from_email = settings.EMAIL_HOST_USER
                    to_email = [settings.EMAIL_RECIEVER, user_email]
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
        return render(request, 'orderdetail.html', {'order': order, 'items': items})
    else:
        return render(request, 'orderdetail.html', {})


def order_history(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(product__user=request.user).order_by('-id')
        return render(request, 'orderhistory.html', {'order_items': order_items})
    else:
        return render(request, 'orderhistory.html', {})


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
        return render(request, 'Dashboardtariff.html')
    return render(request, 'WriberTariffUpdate.html', {'locations': locations, 'form': form})


def update_tariff(request, pk):
    tariffs = Tariffs.objects.get(id=pk)
    form = TariffsForm(request.POST or None, request.FILES or None, instance=tariffs)
    form.fields["page_owner"].queryset = Usercreatedpage.objects.filter(user=request.user)
    if form.is_valid():
        form.save()
        return render(request, 'Dashboardtariff.html')
    return render(request, 'WriberTarifflistupdate.html', {'tariffs': tariffs, 'form': form})


def settings_dashboard(request, pk):
    if request.user.is_authenticated:
        accountprofile = UserProfile.objects.get(user_id=pk)
        return render(request, 'Settings.html', {'accountprofile': accountprofile})
    else:
        return render(request, 'Settings.html', {})


def update_account_profile(request):
    if request.user.is_authenticated:
        accountprofile = User.objects.get(id=request.user.id)
        form = SignupForm(request.POST or None, request.FILES or None, instance=accountprofile)
        if form.is_valid():
            form.save()
            login(request, accountprofile)
            messages.success(request, ("Congratulations, your profile is updated"))
            return render(request, 'accountupdatedalert.html')
        return render(request, 'WriberAccountUpdate.html', {'accountprofile': accountprofile, 'form': form})
    else:
        return render(request, 'WriberAccountUpdate.html', {})


# allow users to be able to view and see all there products on one page and allow them to be able to add products to the database without having a page

# allow users to choose their location choice for the delivery, from the options presented by the checkout
# page which can be done by query setting the checkout page just like i did in the update page
#sudo dscl . -create /Users/postgres UserShell /bin/sh

#sudo dscl . -create /Users/postgres NFSHomeDirectory /Library/PostgreSQL

