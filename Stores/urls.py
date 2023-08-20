from django.urls import path

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.homeproducts, name='products'),
    path('services', views.homeservices, name='services'),
    path('searched_pages', views.Search_page, name='searched-pages'),
    path('searched_products', views.Search_productpage, name='searched-products'),
    path('searched_services', views.Search_servicepage, name='searched-services'),
    path('login_in', views.login_account, name="login-user"),
    path('logout_account', views.logout_account, name="logout-user"),
    path('signup_account', views.signup_account, name="signup-user"),
    path('wriber/<int:pk>', views.account_profile, name="wriber-page"),
    path('update_account', views.update_account_profile, name="update-account"),
    path('wriber_page/<int:pk>', views.account_page, name="account-page"),
    path('page_view/<int:pk>', views.user_page, name="wriber"),
    path('wriber_viewproducts/<int:pk>', views.view_products, name="wriber-viewproducts"),
    path('wriber_viewservices/<int:pk>', views.view_services, name="wriber-viewservices"),
    path('dashboard_page/<int:pk>', views.page_dashboard, name="dashboard-page"),
    path('dashboard_product/<int:pk>', views.perpage_product, name="dashboard-product"),
    path('wriber_add_page', views.addnew_page, name="wriber-page-add"),
    path('wriber_add_products', views.addnew_product, name="wriber-products-add"),
    path('wriber_add_services', views.addnew_service, name="wriber-services-add"),
    path('wriber_updateproducts/<int:pk>', views.update_products, name="wriber-updateproducts"),
    path('wriber_updateservices/<int:pk>', views.update_services, name="wriber-updateservices"),
    path('wriber_updatepage/<int:pk>', views.update_page, name="wriber-updatepages"),
    path('delete_products/<int:pk>', views.delete_wriber_products_ondash, name="delete-wriber-products"),
    path('delete_services/<int:pk>', views.delete_wriber_services, name="delete-wriber-services"),
    path('delete_products_pagemanage/<int:pk>', views.delete_wriber_products_onpagemanage, name="delete-wriber-products-onpagemanage"),
    path('add_to_cart/<int:pk>', views.add_to_cart, name="add-to-cart"),
    path('view_cart/', views.cart_view, name="cart-view"),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name="remove-from-cart"),
    path('change_quantity/<str:pk>', views.change_quantity, name="change-quantity"),
    path('checkout', views.checkout, name="checkout"),
    path('order_history', views.order_history, name="orders"),
    path('order_detail/<int:pk>', views.order_items, name="order-detail"),
    path('orders', views.orders, name="orders-from-you"),
    path('dashboard_tariff', views.dashboard_tariff, name="dashboard-tariff"),
    path('view_tariff/<int:pk>', views.view_tariff, name="tariffs"),
    path('locations_view/<int:pk>', views.view_tariff_page, name="tariff-page"),
    path('detail_tariff/<int:pk>', views.tariff_detail, name="tariff-detail"),
    path('modify_tariff', views.addnew_tariff_location, name="add-new-tariff"),
    path('add_tariff', views.addnew_tariff, name="add-tariff"),
    path('update_tariff/<int:pk>', views.update_location, name="update-tariff"),
    path('modify_tariff/<int:pk>', views.update_tariff, name="modify-tariff"),
    path('settings_page/<int:pk>', views.settings_dashboard, name="settings"),
    #path('feedback', views.feedback_form, name="feedback" ),

    #path('reset_password', auth_views.PasswordResetView.as_view(), name="reset_password"),

    #path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    #path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    #path('reset_password/complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),



]