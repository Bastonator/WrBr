from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Usercreatedpage
from .models import Product_info
from .models import Service_info
from .models import User_Page
from .models import Order
from .models import OrderItem, Ordered, Tariffs, Tariff_query, location_gambia #, feedback


class location_gambiaInline(admin.StackedInline):
    model = location_gambia
    extra = 0


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class Product_infoInline(admin.StackedInline):
    model = Product_info
    extra = 0


class Service_infoInline(admin.StackedInline):
    model = Service_info
    extra = 0


class User_pageInline(admin.StackedInline):
    model = User_Page


class UsercreatedpageAdmin(admin.ModelAdmin):
    model = Usercreatedpage
    fields = ['id', 'page_name', 'page_description', 'theme_photo', 'location', 'user', 'business_name']
    inlines = [User_pageInline, Product_infoInline, Service_infoInline]


class OrderedInline(admin.StackedInline):
    model = Ordered


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'first_name', 'last_name', 'address', 'created_by')
    inlines = [OrderedInline, OrderItemInline]


#class feedbackAdmin(admin.ModelAdmin):
    #model = feedback
    #list_display = ('name', 'feedback')


class Tariff_queryInline(admin.StackedInline):
    model = Tariff_query


class TariffsAdmin(admin.ModelAdmin):
    model = Tariffs
    fields = ["name", "user", "page_owner"]
    inlines = [Tariff_queryInline, location_gambiaInline]


class location_gambiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tariff_owner')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'price')


class Product_infoAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_price', 'stock_available', 'user', 'page_owner')


class Service_infoAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'service_price', 'location', 'user', 'page_owner')


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "email", "first_name", "last_name"]
    inlines = [UserProfileInline]


admin.site.unregister(User)


admin.site.register(User, UserAdmin)
admin.site.register(Usercreatedpage, UsercreatedpageAdmin)
admin.site.register(Product_info, Product_infoAdmin)
admin.site.register(Service_info, Service_infoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Tariffs, TariffsAdmin)
admin.site.register(location_gambia, location_gambiaAdmin)
#admin.site.register(feedback, feedbackAdmin)
